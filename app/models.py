from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone
import string
import random


class Consent(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	read_pis: so.Mapped[str] = so.mapped_column(sa.String(16))
	understood_pis: so.Mapped[str] = so.mapped_column(sa.String(16))
	participation_voluntary: so.Mapped[str] = so.mapped_column(sa.String(16))
	information_consent: so.Mapped[str] = so.mapped_column(sa.String(16))
	data_access: so.Mapped[str] = so.mapped_column(sa.String(16))
	anonymised_excerpts: so.Mapped[str] = so.mapped_column(sa.String(16))
	results_published: so.Mapped[str] = so.mapped_column(sa.String(16))
	take_part: so.Mapped[str] = so.mapped_column(sa.String(16))
	participant_name: so.Mapped[str] = so.mapped_column(sa.String(128))
	date: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	email: so.Mapped[str] = so.mapped_column(sa.String(128))
	keep_me_updated: so.Mapped[bool] = so.mapped_column(sa.Boolean())

	def __repr__(self):
		return f'<Consent {self.id}>'


class Demographic(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	blackjack_experience: so.Mapped[str] = so.mapped_column(sa.String(32))
	computer_experience: so.Mapped[str] = so.mapped_column(sa.String(32))
	age: so.Mapped[int] = so.mapped_column()
	gender: so.Mapped[str] = so.mapped_column(sa.String(16))
	completed_study: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False)
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Demographic id:{self.id}, completed_study:{self.completed_study}>'


class Participant(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	explanation_version: so.Mapped[int] = so.mapped_column()
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Participant id:{self.id}, explanation_version: {self.explanation_version}>'


class Game(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	game_id: so.Mapped[int] = so.mapped_column()
	score: so.Mapped[Optional[int]] = so.mapped_column()
	ai_enabled: so.Mapped[bool] = so.mapped_column(sa.Boolean())
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Game {self.id}, participant_id:{self.participant_id}, game_id:{self.game_id}, score:{self.score}, ai_enabled:{self.ai_enabled}>'


class Action(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	type: so.Mapped[str] = so.mapped_column(sa.String(32))
	last_action_time: so.Mapped[Optional[datetime]] = so.mapped_column()
	action_time: so.Mapped[Optional[datetime]] = so.mapped_column()
	update_value: so.Mapped[Optional[int]] = so.mapped_column()
	concept_id: so.Mapped[int] = so.mapped_column()
	game_id: so.Mapped[int] = so.mapped_column()
	sample_number: so.Mapped[int] = so.mapped_column()
	reset_pressed: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean())
	model_move: so.Mapped[Optional[int]] = so.mapped_column()
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Action {self.id}, participant_id:{self.participant_id}, type:{self.type}, last_action_time:{self.last_action_time}, action_time:{self.action_time}, update_value:{self.update_value}, concept_id:{self.concept_id}, game_id:{self.game_id}, sample_number:{self.sample_number}, reset_pressed:{self.reset_pressed}, model_move:{self.model_move}>'


class ConceptSort(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	action_time: so.Mapped[datetime] = so.mapped_column()
	update_value: so.Mapped[str] = so.mapped_column(sa.String(8))
	game_id: so.Mapped[int] = so.mapped_column()
	sample_number: so.Mapped[int] = so.mapped_column()
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Action {self.id}, participant_id:{self.participant_id}, action_time:{self.action_time}, update_value:{self.update_value}, game_id:{self.game_id}, sample_number:{self.sample_number}>'


class Sample(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	game_id: so.Mapped[int] = so.mapped_column()
	sample_number: so.Mapped[int] = so.mapped_column()
	participant_move: so.Mapped[Optional[int]] = so.mapped_column()
	model_move: so.Mapped[Optional[int]] = so.mapped_column()
	start_time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	complete_time: so.Mapped[Optional[datetime]] = so.mapped_column()
	ai_use: so.Mapped[int] = so.mapped_column(server_default="0")
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Sample {self.id}, participant_id:{self.participant_id}, game_id:{self.game_id}, sample_number:{self.sample_number}, participant_move:{self.participant_move}, model_move:{self.model_move}, ai_use:{self.ai_use}, start_time:{self.start_time}, complete_time:{self.complete_time}>'


class Survey(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	factors_in_data: so.Mapped[int] = so.mapped_column()
	understood: so.Mapped[int] = so.mapped_column()
	change_detail_level: so.Mapped[int] = so.mapped_column()
	need_support: so.Mapped[int] = so.mapped_column()
	understood_causality: so.Mapped[int] = so.mapped_column()
	use_with_knowledge: so.Mapped[int] = so.mapped_column()
	no_inconsistencies: so.Mapped[int] = so.mapped_column()
	learn_to_understand: so.Mapped[int] = so.mapped_column()
	need_references: so.Mapped[int] = so.mapped_column()
	efficient: so.Mapped[int] = so.mapped_column()
	text: so.Mapped[str] = so.mapped_column(sa.String(5000))
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return '<Survey {}>'.format(self.id)
