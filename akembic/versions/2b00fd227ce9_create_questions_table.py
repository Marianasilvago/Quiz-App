"""create questions table

Revision ID: 2b00fd227ce9
Revises: 
Create Date: 2022-10-28 20:53:01.307466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b00fd227ce9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('questions',
                sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                sa.Column('question', sa.String(), nullable=False),
                sa.Column('choice1', sa.String(), nullable=False),
                sa.Column('choice2', sa.String(), nullable=False),
                sa.Column('choice3', sa.String(), nullable=False),
                sa.Column('choice4', sa.String(), nullable=False),
                sa.Column('correct_choice', sa.String(), nullable=False),
                sa.Column('published', sa.Boolean(), nullable=False, server_default='FALSE'),               sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),          
    )
    pass


def downgrade() -> None:
    op.drop_table('questions')
    pass
