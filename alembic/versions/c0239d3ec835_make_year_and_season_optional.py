"""make year and season optional

Revision ID: c0239d3ec835
Revises: 3526c4a07aea
Create Date: 2025-07-24 10:38:36.748677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c0239d3ec835'
down_revision: Union[str, Sequence[str], None] = '3526c4a07aea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('anime', 'release_year',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('anime', 'release_season',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('anime', 'release_season',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('anime', 'release_year',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
