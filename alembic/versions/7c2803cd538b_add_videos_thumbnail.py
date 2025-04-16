"""add videos thumbnail

Revision ID: 7c2803cd538b
Revises: 8943734a55fc
Create Date: 2025-04-17 00:22:29.644562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c2803cd538b'
down_revision: Union[str, None] = '8943734a55fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('short_videos', sa.Column('thumbnail', sa.Text(), server_default='', nullable=False))
    op.alter_column('short_videos', 'views',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('short_videos', 'likes',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('short_videos', 'saves',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('stories', 'likes',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('stories', 'saves',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stories', 'saves',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('stories', 'likes',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('short_videos', 'saves',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('short_videos', 'likes',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('short_videos', 'views',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('short_videos', 'thumbnail')
    # ### end Alembic commands ###
