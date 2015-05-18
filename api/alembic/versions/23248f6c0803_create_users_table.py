"""create users table

Revision ID: 23248f6c0803
Revises: 
Create Date: 2015-05-17 20:35:33.560247

"""

# revision identifiers, used by Alembic.
revision = '23248f6c0803'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    users_table = op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('auth_token', sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table('users')
