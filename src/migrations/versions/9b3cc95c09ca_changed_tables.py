"""Changed tables

Revision ID: 9b3cc95c09ca
Revises: 9e96afce0c9e
Create Date: 2025-04-10 07:00:23.032307

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9b3cc95c09ca'
down_revision = '9e96afce0c9e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('place')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('place',
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('latitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('longitude', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('country', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('locality', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='place_pkey')
    )
    # ### end Alembic commands ###
