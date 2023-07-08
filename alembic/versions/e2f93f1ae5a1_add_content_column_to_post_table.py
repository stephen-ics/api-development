"""add content column to post table

Revision ID: e2f93f1ae5a1
Revises: ac03f4bfc2bd
Create Date: 2023-07-07 20:04:37.530359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2f93f1ae5a1'
down_revision = 'ac03f4bfc2bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
