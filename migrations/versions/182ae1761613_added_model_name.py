"""added model name

Revision ID: 182ae1761613
Revises: 3cbc21da926f
Create Date: 2024-08-12 11:34:52.457399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '182ae1761613'
down_revision = '3cbc21da926f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model_name', sa.String(length=32), server_default='blackjack_CtoY_onnx_standard', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.drop_column('model_name')

    # ### end Alembic commands ###
