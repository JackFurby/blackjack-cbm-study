"""added study complete to consent

Revision ID: b148c8bb89ae
Revises: 5b8a05800076
Create Date: 2024-08-20 15:32:32.531435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b148c8bb89ae'
down_revision = '5b8a05800076'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_study', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consent', schema=None) as batch_op:
        batch_op.drop_column('completed_study')

    # ### end Alembic commands ###
