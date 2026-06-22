"""initial

Revision ID: a2e73777dbbe
Revises: 
Create Date: 2026-05-13 10:03:57.138977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a2e73777dbbe'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(255), nullable=True),
        sa.Column('password', sa.String(255), nullable=True),
        sa.Column('is_creator', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_username', 'users', ['username'])

    op.create_table('puzzles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('hor_size', sa.Integer(), nullable=True),
        sa.Column('ver_size', sa.Integer(), nullable=True),
        sa.Column('difficulty', sa.String(255), nullable=True),
        sa.Column('solution_grid', sa.JSON(), nullable=True),
        sa.Column('row_clues', sa.JSON(), nullable=True),
        sa.Column('col_clues', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_puzzles_id', 'puzzles', ['id'])
    op.create_index('ix_puzzles_title', 'puzzles', ['title'])
    op.create_index('ix_puzzles_difficulty', 'puzzles', ['difficulty'])
    op.create_index('ix_puzzles_hor_size', 'puzzles', ['hor_size'])
    op.create_index('ix_puzzles_ver_size', 'puzzles', ['ver_size'])

    op.create_table('attempts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('puzzle_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(255), nullable=True),
        sa.Column('current_grid', sa.JSON(), nullable=True),
        sa.Column('time_spent', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['puzzle_id'], ['puzzles.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_attempts_id', 'attempts', ['id'])


def downgrade() -> None:
    op.drop_table('attempts')
    op.drop_table('puzzles')
    op.drop_table('users')
