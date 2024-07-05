"""initial database

Revision ID: acef960bd5fe
Revises: 
Create Date: 2024-06-23 13:03:50.508077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acef960bd5fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('read_pis', sa.String(length=16), nullable=False),
    sa.Column('understood_pis', sa.String(length=16), nullable=False),
    sa.Column('participation_voluntary', sa.String(length=16), nullable=False),
    sa.Column('information_consent', sa.String(length=16), nullable=False),
    sa.Column('data_access', sa.String(length=16), nullable=False),
    sa.Column('anonymised_excerpts', sa.String(length=16), nullable=False),
    sa.Column('results_published', sa.String(length=16), nullable=False),
    sa.Column('take_part', sa.String(length=16), nullable=False),
    sa.Column('participant_name', sa.String(length=128), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('keep_me_updated', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('demographic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skin_experience', sa.String(length=32), nullable=False),
    sa.Column('computer_experience', sa.String(length=32), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=16), nullable=False),
    sa.Column('completed_study', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('explanation_version', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=32), nullable=False),
    sa.Column('last_action_time', sa.DateTime(), nullable=True),
    sa.Column('action_time', sa.DateTime(), nullable=True),
    sa.Column('update_value', sa.Integer(), nullable=True),
    sa.Column('concept_id', sa.Integer(), nullable=False),
    sa.Column('sample_id', sa.Integer(), nullable=False),
    sa.Column('reset_pressed', sa.Boolean(), nullable=True),
    sa.Column('model_malignant', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('action', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_action_participant_id'), ['participant_id'], unique=False)

    op.create_table('concept_sort',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('action_time', sa.DateTime(), nullable=False),
    sa.Column('update_value', sa.String(length=8), nullable=False),
    sa.Column('sample_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('concept_sort', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_concept_sort_participant_id'), ['participant_id'], unique=False)

    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('sample_id', sa.Integer(), nullable=False),
    sa.Column('participant_malignant', sa.Boolean(), nullable=True),
    sa.Column('model_malignant', sa.Boolean(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('complete_time', sa.DateTime(), nullable=True),
    sa.Column('ai_use', sa.Integer(), server_default='0', nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('sample', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_sample_participant_id'), ['participant_id'], unique=False)

    op.create_table('survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('factors_in_data', sa.Integer(), nullable=False),
    sa.Column('understood', sa.Integer(), nullable=False),
    sa.Column('change_detail_level', sa.Integer(), nullable=False),
    sa.Column('need_support', sa.Integer(), nullable=False),
    sa.Column('understood_causality', sa.Integer(), nullable=False),
    sa.Column('use_with_knowledge', sa.Integer(), nullable=False),
    sa.Column('no_inconsistencies', sa.Integer(), nullable=False),
    sa.Column('learn_to_understand', sa.Integer(), nullable=False),
    sa.Column('need_references', sa.Integer(), nullable=False),
    sa.Column('efficient', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=5000), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('survey', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_survey_participant_id'), ['participant_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('survey', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_survey_participant_id'))

    op.drop_table('survey')
    with op.batch_alter_table('sample', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sample_participant_id'))

    op.drop_table('sample')
    with op.batch_alter_table('concept_sort', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_concept_sort_participant_id'))

    op.drop_table('concept_sort')
    with op.batch_alter_table('action', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_action_participant_id'))

    op.drop_table('action')
    op.drop_table('participant')
    op.drop_table('demographic')
    op.drop_table('consent')
    # ### end Alembic commands ###
