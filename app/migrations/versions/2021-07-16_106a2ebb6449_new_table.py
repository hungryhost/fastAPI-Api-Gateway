"""New table

Revision ID: 106a2ebb6449
Revises: cce91e27bcfe
Create Date: 2021-07-16 05:20:08.569225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '106a2ebb6449'
down_revision = 'cce91e27bcfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('picture', sa.String(), nullable=True),
    sa.Column('google_auth', sa.Boolean(), nullable=True),
    sa.Column('hse_auth', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
