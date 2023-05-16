"""tables

Revision ID: 39b32c306652
Revises: b3e7978e5cb5
Create Date: 2023-05-15 10:04:07.906627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39b32c306652'
down_revision = 'b3e7978e5cb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numberofplayers', sa.Integer(), nullable=True),
    sa.Column('nextplayer', sa.Integer(), nullable=True),
    sa.Column('playerone', sa.String(length=64), nullable=True),
    sa.Column('playertwo', sa.String(length=64), nullable=True),
    sa.Column('playerthree', sa.String(length=64), nullable=True),
    sa.Column('playerfour', sa.String(length=64), nullable=True),
    sa.Column('playerfive', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_game_nextplayer'), ['nextplayer'], unique=False)
        batch_op.create_index(batch_op.f('ix_game_numberofplayers'), ['numberofplayers'], unique=False)
        batch_op.create_index(batch_op.f('ix_game_playerfive'), ['playerfive'], unique=True)
        batch_op.create_index(batch_op.f('ix_game_playerfour'), ['playerfour'], unique=True)
        batch_op.create_index(batch_op.f('ix_game_playerone'), ['playerone'], unique=True)
        batch_op.create_index(batch_op.f('ix_game_playerthree'), ['playerthree'], unique=True)
        batch_op.create_index(batch_op.f('ix_game_playertwo'), ['playertwo'], unique=True)

    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_score_name'), ['name'], unique=True)

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_index('ix_player_name')

    op.drop_table('player')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.create_index('ix_player_name', ['name'], unique=False)

    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_score_name'))

    op.drop_table('score')
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_game_playertwo'))
        batch_op.drop_index(batch_op.f('ix_game_playerthree'))
        batch_op.drop_index(batch_op.f('ix_game_playerone'))
        batch_op.drop_index(batch_op.f('ix_game_playerfour'))
        batch_op.drop_index(batch_op.f('ix_game_playerfive'))
        batch_op.drop_index(batch_op.f('ix_game_numberofplayers'))
        batch_op.drop_index(batch_op.f('ix_game_nextplayer'))

    op.drop_table('game')
    # ### end Alembic commands ###