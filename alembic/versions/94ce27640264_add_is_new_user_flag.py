"""add is new user flag

Revision ID: 94ce27640264
Revises: 45906e21c351
Create Date: 2025-04-13 03:50:22.098513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94ce27640264'
down_revision: Union[str, None] = '45906e21c351'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('short_videos', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False,
               autoincrement=True)
    op.alter_column('short_videos', 'title',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('short_videos', 'url',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('short_videos', 'views',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('short_videos', 'likes',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('short_videos', 'filename',
               existing_type=sa.TEXT(),
               nullable=False)
    op.add_column('users', sa.Column('is_new_user', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_new_user')
    op.alter_column('short_videos', 'filename',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('short_videos', 'likes',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('short_videos', 'views',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('short_videos', 'url',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('short_videos', 'title',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('short_videos', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True,
               autoincrement=True)
    # ### end Alembic commands ###
