"""add views on story

Revision ID: 8943734a55fc
Revises: 6a298c3d598a
Create Date: 2025-04-16 23:06:59.233319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8943734a55fc'
down_revision: Union[str, None] = '6a298c3d598a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('stories', sa.Column('views', sa.Integer(), nullable=False, server_default=sa.text('0')))
    # After the column is added, you can optionally remove the server default if needed:
    op.alter_column('stories', 'views', server_default=None)

def downgrade():
    op.drop_column('stories', 'views')
    # ### end Alembic commands ###
