"""empty message

Revision ID: 183fe3aae8a1
Revises: 0b9020e0c296
Create Date: 2020-12-17 12:41:52.704536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '183fe3aae8a1'
down_revision = '0b9020e0c296'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('state')
    op.drop_table('country')
    # ### end Alembic commands ###