"""updated desample table for blackjack

Revision ID: 9792e04166a0
Revises: 316c6722090e
Create Date: 2024-07-02 12:58:01.236962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9792e04166a0'
down_revision = '316c6722090e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sample', schema=None) as batch_op:
        batch_op.add_column(sa.Column('game_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('sample_number', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('participant_move', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('model_move', sa.Boolean(), nullable=True))
        batch_op.drop_column('participant_malignant')
        batch_op.drop_column('sample_id')
        batch_op.drop_column('model_malignant')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sample', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model_malignant', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('sample_id', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('participant_malignant', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('model_move')
        batch_op.drop_column('participant_move')
        batch_op.drop_column('sample_number')
        batch_op.drop_column('game_id')

    # ### end Alembic commands ###
