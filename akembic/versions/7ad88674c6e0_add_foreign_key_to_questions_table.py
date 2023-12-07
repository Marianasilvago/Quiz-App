"""add foreign-key to questions table

Revision ID: 7ad88674c6e0
Revises: dc1a2765532c
Create Date: 2022-10-29 10:42:15.172982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ad88674c6e0'
down_revision = 'dc1a2765532c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('questions', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('questions_users_fk', source_table='questions', referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('questions_users_fk',table_name="questions")
    op.drop_column("questions", "owner_id")
    pass
