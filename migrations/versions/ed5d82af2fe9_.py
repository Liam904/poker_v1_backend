"""empty message

Revision ID: ed5d82af2fe9
Revises: 
Create Date: 2024-09-24 14:04:07.795134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed5d82af2fe9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alias', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('computer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rank', sa.String(length=10), nullable=False),
    sa.Column('suit', sa.String(length=10), nullable=False),
    sa.Column('alias_id', sa.Integer(), nullable=True),
    sa.Column('computer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['alias_id'], ['alias.id'], ),
    sa.ForeignKeyConstraint(['computer_id'], ['computer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deck', sa.PickleType(), nullable=False),
    sa.Column('table_card', sa.PickleType(), nullable=False),
    sa.Column('game_state', sa.PickleType(), nullable=False),
    sa.Column('winner', sa.String(length=100), nullable=False),
    sa.Column('alias_id', sa.Integer(), nullable=True),
    sa.Column('computer_id', sa.Integer(), nullable=True),
    sa.Column('computer_hand', sa.PickleType(), nullable=True),
    sa.Column('player_hand', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['alias_id'], ['alias.id'], ),
    sa.ForeignKeyConstraint(['computer_id'], ['computer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    op.drop_table('card')
    op.drop_table('computer')
    op.drop_table('alias')
    # ### end Alembic commands ###
