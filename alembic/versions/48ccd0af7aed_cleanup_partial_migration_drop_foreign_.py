"""cleanup partial migration - drop foreign keys and themes table

Revision ID: 48ccd0af7aed
Revises: a9ab84e1fb14
Create Date: 2025-08-04 14:06:05.129833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48ccd0af7aed'
down_revision: Union[str, Sequence[str], None] = 'a9ab84e1fb14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Complete the remaining steps from the previous partial migration
    # Drop foreign key constraints first before dropping the referenced table
    op.drop_constraint('endings_ibfk_1', 'endings', type_='foreignkey')
    op.drop_column('endings', 'theme_id')
    op.drop_constraint('openings_ibfk_1', 'openings', type_='foreignkey')
    op.drop_column('openings', 'theme_id')
    # Now we can safely drop the themes table
    op.drop_table('themes')


def downgrade() -> None:
    """Downgrade schema."""
    pass
