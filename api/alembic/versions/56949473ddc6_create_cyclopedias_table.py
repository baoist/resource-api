"""create cyclopedias table

Revision ID: 56949473ddc6
Revises: 23248f6c0803
Create Date: 2015-05-25 18:11:15.188921

"""

# revision identifiers, used by Alembic.
revision = '56949473ddc6'
down_revision = '23248f6c0803'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship


def upgrade():
    cyclopedias_table = op.create_table(
        'cyclopedias',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('topic', sa.String(255), index=True, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('parent_cyclopedia_id', sa.Integer, sa.ForeignKey('cyclopedias.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('cyclopedias')
