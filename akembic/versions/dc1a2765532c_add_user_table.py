"""add user table

Revision ID: dc1a2765532c
Revises: 2b00fd227ce9
Create Date: 2022-10-29 10:10:44.856057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc1a2765532c'
down_revision = '2b00fd227ce9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')          
                )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
