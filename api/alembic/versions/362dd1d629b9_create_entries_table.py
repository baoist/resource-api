"""create entries table

Revision ID: 362dd1d629b9
Revises: 56949473ddc6
Create Date: 2015-05-26 15:43:54.556763

"""

# revision identifiers, used by Alembic.
revision = '362dd1d629b9'
down_revision = '56949473ddc6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship


def upgrade():
    entries_table = op.create_table(
        'entries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('term', sa.String(255), index=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('image_url', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cyclopedia_id', sa.Integer, sa.ForeignKey('cyclopedias.id'), nullable=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('entries')
