"""Create pallet table and other tables

Revision ID: 3d6f79643bce
Revises: 28a19a938669
Create Date: 2025-04-12 00:00:27.879861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d6f79643bce'
down_revision: Union[str, None] = '28a19a938669'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('palettes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predominant', sa.Text(), nullable=False),
    sa.Column('dark', sa.Text(), nullable=False),
    sa.Column('light', sa.Text(), nullable=False),
    sa.Column('median_brightness', sa.Text(), nullable=False),
    sa.Column('most_saturated', sa.Text(), nullable=False),
    sa.Column('least_saturated', sa.Text(), nullable=False),
    sa.Column('coolest', sa.Text(), nullable=False),
    sa.Column('warmest', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('poster', sa.Text(), nullable=True),
    sa.Column('poster_palette_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['poster_palette_id'], ['palettes.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('story_chapters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('story_id', sa.Integer(), nullable=True),
    sa.Column('chapter_index', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('image_palette_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_palette_id'], ['palettes.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('story_chapters')
    op.drop_table('stories')
    op.drop_table('palettes')
    # ### end Alembic commands ###
