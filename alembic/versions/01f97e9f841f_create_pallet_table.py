"""Create pallet table

Revision ID: 01f97e9f841f
Revises: 22b8a5b43c03
Create Date: 2025-04-11 23:56:32.019312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '01f97e9f841f'
down_revision: Union[str, None] = '22b8a5b43c03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the child table first
    op.drop_table('story_chapters')
    op.drop_table('stories')


def downgrade() -> None:
    # Recreate the tables in reverse order
    op.create_table(
        'stories',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.TEXT(), nullable=False),
        sa.Column('poster', sa.TEXT(), nullable=True),
        sa.Column('poster_pallet', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id', name='stories_pkey')
    )
    op.create_table(
        'story_chapters',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('story_id', sa.INTEGER(), nullable=True),
        sa.Column('chapter_index', sa.INTEGER(), nullable=False),
        sa.Column('content', sa.TEXT(), nullable=False),
        sa.Column('image', sa.TEXT(), nullable=True),
        sa.Column('image_pallet', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], name='story_chapters_story_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='story_chapters_pkey')
    )
