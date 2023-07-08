"""add foreign key to posts table

Revision ID: 6720810568a0
Revises: ba66ce364e6c
Create Date: 2023-07-07 20:12:57.948588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6720810568a0'
down_revision = 'ba66ce364e6c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
