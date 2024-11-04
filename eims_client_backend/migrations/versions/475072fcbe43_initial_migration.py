"""Initial migration.

Revision ID: 475072fcbe43
Revises: 
Create Date: 2024-11-02 16:55:07.582198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '475072fcbe43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('userID', sa.INTEGER(), sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('firstName', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lastName', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('contact', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('userType', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('userID', name='users_pkey')
    )
    # ### end Alembic commands ###
