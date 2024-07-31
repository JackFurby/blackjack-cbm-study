from flask import Flask, request, Response, flash, make_response, current_app, send_from_directory, jsonify, session
from flask import render_template, url_for, redirect
from flask_mail import Message
import cv2
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app.study import bp
from app.forms import ConsentForm, DemographicForm, SampleForm, SurveyForm
from app.models import Consent, Demographic, Participant, Action, Sample, Survey, ConceptSort, Game
from sqlalchemy import func
from app import db
from app import mail
import random
import json


def get_datetime(milliseconds):
	return datetime.fromtimestamp(milliseconds/1000.0)


@bp.route('/', methods=["GET"])
@bp.route('/study', methods=["GET"])
def study():
	return render_template('study/study.html', title='CBM Study')


@bp.route('/forms', methods=['GET', 'POST'])
def forms():
	if "consent_form" not in session:
		form = ConsentForm()
		if form.validate_on_submit():
			consent = Consent(
				read_pis=form.read_pis.data,
				understood_pis=form.understood_pis.data,
				participation_voluntary=form.participation_voluntary.data,
				information_consent=form.information_consent.data,
				data_access=form.data_access.data,
				anonymised_excerpts=form.anonymised_excerpts.data,
				results_published=form.results_published.data,
				take_part=form.take_part.data,
				participant_name=form.participant_name.data,
				email=form.email.data,
				keep_me_updated=form.keep_me_updated.data,
			)
			db.session.add(consent)
			db.session.commit()

			#msg = Message('test subject', sender=current_app.config['MAIL_USERNAME'], recipients=['furbyjl@cardiff.ac.uk'])
			#msg.body = 'text body'
			#msg.html = '<h1>HTML body</h1>'
			#mail.send(msg)

			session["consent_form"] = True
			return redirect('/survey')
	else:
		return redirect('/survey')
	return render_template('study/forms.html', title='Consent form', form=form, date=datetime.now().strftime("%d/%m/%Y"))


@bp.route('/survey', methods=['GET', 'POST'])
def survey():
	if "demographic_survey" not in session:
		form = DemographicForm()
		if form.validate_on_submit():
			demographic = Demographic(
				blackjack_experience=form.blackjack_experience.data,
				computer_experience=form.computer_experience.data,
				age=form.age.data,
				gender=form.gender.data
			)
			db.session.add(demographic)
			db.session.commit()

			explanatons_list = [0, 1, 2, 3]

			participant = Participant(
				explanation_version=random.choice(explanatons_list)  # explanation version chosen randomly. This should give us an even split between the two
			)
			db.session.add(participant)
			db.session.commit()

			session["participant_id"] = participant.id
			session["demographic_id"] = demographic.id
			session["explanation_version"] = participant.explanation_version
			session["demographic_survey"] = True
			return redirect('/tutorial')
	else:
		return redirect('/tutorial')
	return render_template('study/survey.html', title='Demographic survey', form=form)


@bp.route('/tutorial')
def tutorial():
	# get concept predictions and explanatons
	concept_preds = []
	# open txt file with concept predictions and concept explanation file names
	with bp.open_resource(f"{bp.static_folder}/tutorial/out.txt") as f:
		content = (f.read().decode('latin1').strip()).split("\n")
		for line in content:
			concept = line.split(" ")
			concept_preds.append([int(concept[0].strip()), concept[1].strip(), float(concept[2].strip())])  # concept index, concept explanation file name, concept prediction, concept string

	# open txt file with concept predictions and concept explanation file names
	with bp.open_resource(f"{bp.static_folder}/games/concept_desc.txt") as f:
		content = (f.read().decode('latin1').strip()).split("\n")
		for idx, line in enumerate(content):
			line = [i.strip() for i in line.split(',')]  # concept string, concept description
			concept_preds[idx].append(line[0])  # Add concept string to concept item
			concept_preds[idx].append(line[1])  # Add concept description to concept item

	model_name = "blackjack_CtoY_onnx_model.onnx"

	return render_template('study/tutorial.html', title='Tutorial', concept_out=concept_preds, model_name=model_name, explanation_version=session["explanation_version"])


@bp.route('/samples', methods=['GET', 'POST'])
def samples():
	form = SampleForm()
	# save participant sample classification
	if form.validate_on_submit():

		# update db entery with participant selection
		games_left = session["games_left"]
		samples_left = session["game_samples"]
		sample = db.session.query(Sample).filter_by(participant_id=session["participant_id"], game_id=games_left[-1], sample_number=samples_left[0]).first()
		sample.participant_move = request.form['participant_move']
		sample.complete_time = get_datetime(round(((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())*1000))
		sample.ai_use = request.form["ai_use"]
		db.session.add(sample)
		db.session.commit()

		# if bust (3?), stand (1) or surrender (2) then remove game_id from games_left
		if request.form['participant_move'] in ["1", "2", "3"]:
			return redirect(url_for('study.game_end', last_player_sample=samples_left[0], player_move=request.form['participant_move']))

		# remove sample from game_samples
		del samples_left[0]
		session["game_samples"] = samples_left

	if "participant_id" in session:  # redirect if participant has not completed demographic survey

		if "games_left" not in session:  # randomly order games
			games = [int(i) for i in next(os.walk(f"{bp.static_folder}/games"))[1]]
			random.shuffle(games)
			session["games_left"] = games

			session["ai_free"] = True

		if len(session["games_left"]) == 0:  # if all games seen; end study and go to closing survey
			return redirect(url_for('study.sample_survey'))

		# get sum of game scores
		total_score = (db.session.query(func.sum(Game.score)).filter(Game.participant_id==session["participant_id"], Game.ai_enabled==True).all())[0][0]

		if total_score == None:
			total_score = 0

		# get game id
		games_left = session["games_left"]
		game_id = games_left[-1]

		# get samples for the current game
		if "game_samples" not in session:
			samples = [int(i) for i in next(os.walk(f"{bp.static_folder}/games/{game_id}"))[1]]
			samples.sort()
			session["game_samples"] = samples

		# get game samples
		samples_left = session["game_samples"]
		sample_number = samples_left[0]

		# either player has drawn their last card or the game is over (dealer is given all of their cards)
		if len(samples_left) < 3:
			return redirect(url_for('study.game_end', last_player_sample=samples_left[0], player_move=-1))

		# get player total
		with bp.open_resource(f"{bp.static_folder}/games/{game_id}/{sample_number}/info.txt") as f:
			content = (f.read().decode('latin1').strip()).split("\n")
			lines = []
			for line in content:
				line = line.split(" ")
				lines.append([line[0].strip(), line[1].strip()])  # player/dealer, score

			# get whether the move was the first move of the game
			if lines[2][1] == "True":
				first_move = True
			else:
				first_move = False

		# if sample does not exist in db (first time sample is show to participant) then create db entery
		if db.session.query(Sample).filter_by(participant_id=session["participant_id"], game_id=game_id, sample_number=sample_number).first() is None:
			sample = Sample(
				participant_id=int(session["participant_id"]),
				game_id=games_left[-1],
				sample_number=samples_left[0]
			)
			db.session.add(sample)
			db.session.commit()

		# get concept predictions and explanatons
		concept_preds = []
		# open txt file with concept predictions and concept explanation file names
		with bp.open_resource(f"{bp.static_folder}/games/{game_id}/{sample_number}/out.txt") as f:
			content = (f.read().decode('latin1').strip()).split("\n")
			for line in content:
				concept = line.split(" ")
				concept_preds.append([int(concept[0].strip()), concept[1].strip(), float(concept[2].strip())])  # concept index, concept explanation file name, concept prediction, concept string

		# open txt file with concept predictions and concept explanation file names
		with bp.open_resource(f"{bp.static_folder}/games/concept_desc.txt") as f:
			content = (f.read().decode('latin1').strip()).split("\n")
			for idx, line in enumerate(content):
				line = [i.strip() for i in line.split(',')]  # concept string, concept description
				concept_preds[idx].append(line[0])  # Add concept string to concept item
				concept_preds[idx].append(line[1])  # Add concept description to concept item

		model_name = "blackjack_CtoY_onnx_model.onnx"

		if session["ai_free"]:
			explanation_version = 4
		else:
			explanation_version = session["explanation_version"]

		"""
		explanation versions
		====================

		0 = Only downstram task output
		1 = Only downstream task and concept outputs (no interventions)
		2 = Downstream task output, concepts outputs, and interventions
		3 = Downstream task output, concepts outputs, interventions
		4 = No AI (only used for first game)
		"""

		return render_template('study/samples.html', title='CBM Study', game_id=game_id, sample_number=sample_number, concept_out=concept_preds, form=form, model_name=model_name, explanation_version=explanation_version, total_score=total_score, first_move=first_move)
	else:
		return redirect(url_for('study.survey'))


# Show the results of a game
@bp.route('/game_end/', methods=['GET'])
def game_end():

	last_player_sample = request.args.get('last_player_sample')
	player_move = int(request.args.get('player_move'))

	dealer_sample_number = session["game_samples"][-1]

	# end game and add results to game table
	games_left = session["games_left"]
	game_id = games_left[-1]

	# get player total
	with bp.open_resource(f"{bp.static_folder}/games/{game_id}/{last_player_sample}/info.txt") as f:
		content = (f.read().decode('latin1').strip()).split("\n")
		lines = []
		for line in content:
			line = line.split(" ")
			lines.append([line[0].strip(), line[1].strip()])  # player/dealer, score

		player_total = int(lines[0][1])

		# get whether the move was the first move of the game
		if lines[2][1] == "True":
			first_move = True
		else:
			first_move = False

	# get dealer total
	with bp.open_resource(f"{bp.static_folder}/games/{game_id}/{dealer_sample_number}/info.txt") as f:
		content = (f.read().decode('latin1').strip()).split("\n")
		lines = []
		for line in content:
			line = line.split(" ")
			lines.append([line[0].strip(), line[1].strip()])  # player/dealer, score

		dealer_total = int(lines[1][1])

	"""
	Game scoring
	============

	+---------------------+----------------------------------+--------------------+---------------------+
	|                     |       player_less_than_21        |      player_21     | player_more_than_21 |
	+---------------------+----------------------------------+--------------------+---------------------+
	| dealer_less_than_21 | tie or player wins or player lost| player blackjack   | player lost         |
	|       dealer_21     | Player lost                      | tie                | player lost         |
	| dealer_more_than_21 | player wins                      | player blackjack   | tie / dealer lost   |
	+---------------------+----------------------------------+--------------------+---------------------+

	player wins = +50
	player lost = -50
	player blackjack = +75
	tie = 0
	dealer lost = 0

	* if player and dealer have less than 21 then tie if total match, player lost if less than dealer, else player wins
	* if a player surrenders then the score is always -25


	"""
	if (first_move != True) and (player_move == 2):
		player_move = 1  # if surrender is used when its not the first move then treat it like a stand


	if player_move == 2:  # surrender (move==2) always gets -25 points if first move
		score = -25

	elif dealer_total > 21:
		if player_total > 21:
			score = 0  # tie / dealer lost
		elif player_total == 21:
			score = 75  # player blackjack
		else:  # player_score < 21
			score = 50  # player wins
	elif dealer_total == 21:
		if player_total > 21:
			score = -50  # player lost
		elif player_total == 21:
			score = 0  # tie
		else:  # player_score < 21
			score = -50  # player lost
	else:  # player_score < 21
		if player_total > 21:
			score = -50  # player lost
		elif player_total == 21:
			score = 75  # player blackjack
		else:  # player_score < 21
			if player_total == dealer_total:
				score = 0  # tie
			elif player_total > dealer_total:
				score = 50  # player wins
			else:  # player_total < dealer_total
				score = -50  # player lost

	game = Game(
		participant_id=int(session["participant_id"]),
		game_id=game_id,
		score=score,
		ai_enabled= False if session["ai_free"] else True
	)
	db.session.add(game)
	db.session.commit()

	total_score = (db.session.query(func.sum(Game.score)).filter(Game.participant_id==session["participant_id"], Game.ai_enabled==True).all())[0][0]

	# clear game data from cookies
	del games_left[-1]
	del session["game_samples"]
	session["games_left"] = games_left
	session["ai_free"] = False

	# we return the sample number of the last player card draw and the final sample in the game. In the interface we show the dealer cards part of the last sample, and the
	# player cards of the last player card draw

	return render_template('study/game_end.html', title='CBM Study', game_id=game_id, player_sample_number=last_player_sample, dealer_sample_number=dealer_sample_number, score=score, total_score=total_score, player_total=player_total, dealer_total=dealer_total)


# log what the model predicts for the downstream task (discard the log if the value has already been set)
@bp.route('/model_prediction/', methods=['POST'])
def model_prediction():
	sample = db.session.query(Sample).filter_by(participant_id=session["participant_id"], game_id=request.form.get("game_id"), sample_number=request.form.get("sample_number")).first()
	if sample != None:
		if sample.model_move == None:
			sample.model_move = request.form.get("model_move")
			db.session.add(sample)
			db.session.commit()
			return jsonify("Action logged")
		else:  # value has already been set. Do not update.
			return jsonify("Action logged")
	else:
		return jsonify("No action to log")


@bp.route('/sample_survey', methods=['GET', 'POST'])
def sample_survey():
	if "closing_survey" not in session:
		form = SurveyForm()
		if form.validate_on_submit():
			survey = Survey(
				participant_id=int(session["participant_id"]),
				text=form.text.data,
				factors_in_data=int(form.factors_in_data.data),
				understood=int(form.understood.data),
				change_detail_level=int(form.change_detail_level.data),
				need_support=int(form.need_support.data),
				understood_causality=int(form.understood_causality.data),
				use_with_knowledge=int(form.use_with_knowledge.data),
				no_inconsistencies=int(form.no_inconsistencies.data),
				learn_to_understand=int(form.learn_to_understand.data),
				need_references=int(form.need_references.data),
				efficient=int(form.efficient.data)
			)
			db.session.add(survey)
			db.session.commit()

			# update study to complete
			demographic = Demographic.query.filter_by(id=session["demographic_id"]).first()
			demographic.completed_study = True
			db.session.add(demographic)
			db.session.commit()

			session['closing_survey'] = True

			return redirect('/close')
	else:
		return redirect('/close')
	return render_template('study/sample_survey.html', title='Closing survey', form=form)


@bp.route('/close')
def close():
	return render_template('study/close.html', title='Thank you')


@bp.route('/get_image/<path:filename>')
def get_image(filename):
	return send_from_directory(bp.static_folder, f"games/{filename}")


@bp.route('/get_image_tutorial/<path:filename>')
def get_image_tutorial(filename):
	return send_from_directory(bp.static_folder, f"tutorial/{filename}")


# log concept prediction changes
@bp.route('/log_range_update/', methods=['POST'])
def log_range_update():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		last_action_time=get_datetime(int(request.form.get("last_action_time"))),
		action_time=get_datetime(int(request.form.get("action_time"))),
		update_value=int(float(request.form.get("update_value")) * 100),
		concept_id=int(request.form.get("concept_id")),
		game_id=int(request.form.get("game_id")),
		sample_number=int(request.form.get("sample_number")),
		reset_pressed=True if request.form.get("reset_pressed") == 'true' else False,
		model_move=request.form.get("model_move")
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# log concepts participants see
@bp.route('/log_concept_seen/', methods=['POST'])
def log_concept_seen():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		action_time=get_datetime(int(request.form.get("action_time"))),
		concept_id=int(request.form.get("concept_id")),
		game_id=int(request.form.get("game_id")),
		sample_number=int(request.form.get("sample_number"))
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# log when a participants changes the order concepts are displayed
@bp.route('/log_sort_update/', methods=['POST'])
def log_sort_update():
	action = ConceptSort(
		participant_id=int(session["participant_id"]),
		action_time=get_datetime(int(request.form.get("action_time"))),
		update_value=request.form.get("update_value"),
		game_id=int(request.form.get("game_id")),
		sample_number=int(request.form.get("sample_number"))
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# log when a participants shows a concept description
@bp.route('/toggle_concept_desc/', methods=['POST'])
def toggle_concept_desc():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		action_time=get_datetime(int(request.form.get("action_time"))),
		concept_id=int(request.form.get("concept_id")),
		game_id=int(request.form.get("game_id")),
		sample_number=int(request.form.get("sample_number"))
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# clear session data
@bp.route('/clear_session')
def clear_session():
	try:
		del session["first_move"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["games_left"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["game_samples"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["participant_id"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["consent_form"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["demographic_survey"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session['closing_survey']
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["explanation_version"]
	except Exception as e:
		print(f"Could not delete: {e}")
	return redirect(url_for('study.study'))
