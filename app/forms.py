from wtforms import StringField, BooleanField, RadioField, IntegerField, SelectField, HiddenField, TextAreaField, EmailField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, length, NumberRange, StopValidation
from flask import flash
from flask_wtf import FlaskForm
from werkzeug.local import LocalProxy
from flask import current_app


class MultiCheckboxField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()


class MultiCheckboxAtLeastOne():
	def __init__(self, message=None):
		if not message:
			message = 'At least one option must be selected.'
		self.message = message

	def __call__(self, form, field):
		if len(field.data) == 0:
			raise StopValidation(self.message)


class MultiCheckboxExclusive():
	"""
	ensure if a given option is selected then throw an error if any other option is selected at the same time
	"""
	def __init__(self, exclusive_option, message=None):
		if not message:
			message = f"One option you checked is exclusive and cannot be checked at the same time as other options."
		self.message = message
		self.exclusive_option = exclusive_option

	def __call__(self, form, field):
		if (str(self.exclusive_option) in field.data) and (len(field.data) > 1):
			raise StopValidation(self.message)


class MultiCheckboxNotMoreThan():
	def __init__(self, max, message=None):
		if not message:
			message = f"You cannot select more than {max} options."
		self.message = message
		self.max = max

	def __call__(self, form, field):
		if len(field.data) > self.max:
			raise StopValidation(self.message)


class ConsentForm(FlaskForm):
	read_pis = StringField('Please initial box', validators=[DataRequired()])
	understood_pis = StringField('Please initial box', validators=[DataRequired()])
	participation_voluntary = StringField('Please initial box', validators=[DataRequired()])
	information_consent = StringField('Please initial box', validators=[DataRequired()])
	data_access = StringField('Please initial box', validators=[DataRequired()])
	anonymised_excerpts = StringField('Please initial box', validators=[DataRequired()])
	results_published = StringField('Please initial box', validators=[DataRequired()])
	take_part = StringField('Please initial box', validators=[DataRequired()])
	participant_name = StringField('Name of participant', validators=[DataRequired()])
	email = EmailField('Email', validators=[DataRequired()])
	keep_me_updated = BooleanField('Keep me updated when this research is published', validators=[])


class DemographicForm(FlaskForm):
	blackjack_experience = RadioField('I am experienced at playing Blackjack', choices=["Strongly agree", "agree", "Neutral", "Disagree", "Strongly Disagree"], validators=[DataRequired()])
	computer_experience = RadioField('I am experienced in computer science / computing', choices=["Strongly agree", "agree", "Neutral", "Disagree", "Strongly Disagree"], validators=[DataRequired()])
	age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18)])
	gender = SelectField('Gender', choices=[("", "Choose..."), ("Male", "male"), ("Female", "female"), ("Other", "other"),], validators=[DataRequired()])


class SampleForm(FlaskForm):
	ai_use = MultiCheckboxField('Select all that apply', choices=[(1, "I was influenced by the AI’s suggestion"), (2, "I was influenced by the concepts the AI detected"), (3, "I was not influenced by the AI")], validators=[MultiCheckboxAtLeastOne(), MultiCheckboxNotMoreThan(max=2), MultiCheckboxExclusive(exclusive_option=3, message="'I was not influenced by the AI' cannot be selected at the same time as other options")], validate_choice=False)
	participant_move = RadioField('Make your move', choices=[(0, "Hit"), (1, "Stand"), (2, "Surrender")], validators=[DataRequired()])


class SurveyForm(FlaskForm):
	factors_in_data = RadioField('I found that the data included all relevant known causal factors with sufficient precision and granularity', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	understood = RadioField('I understood the explanations within the context of the game', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	change_detail_level = RadioField('I could change the level of detail on demand', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	need_support = RadioField('I did not need support to understand the explanations', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	understood_causality = RadioField('I found the explanations helped me to understand causality', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	use_with_knowledge = RadioField('I was able to use the explanations with my knowledgebase', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	no_inconsistencies = RadioField('I did not find inconsistencies between explanations', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	learn_to_understand = RadioField('I think that most people would learn to understand the explanations very quickly', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	need_references = RadioField('I did not need more references in the explanations: e.g., strategy guides', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	efficient = RadioField('I received the explanations in a timely and efficient manner', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	text = TextAreaField('Any other comments about the AI and explanations (max 5000 characters. Write "none" if you have no comments)', validators=[DataRequired(), length(max=5000)])
