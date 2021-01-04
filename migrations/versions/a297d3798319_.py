"""empty message

Revision ID: a297d3798319
Revises: e08de8933907
Create Date: 2021-01-04 18:27:28.015142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a297d3798319'
down_revision = 'e08de8933907'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role')
    op.drop_table('role_user')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    op.create_table('role_user',
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('role_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('role',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('description', sa.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###
