"""initial migration

Revision ID: cd5dbf835e6b
Revises: 
Create Date: 2025-07-17 17:46:02.276415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'cd5dbf835e6b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ Make profile_id nullable to avoid constraint issues
    op.alter_column('user', 'profile_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # 2️⃣ Clean up any orphaned profile_id references
    op.execute("""
        UPDATE `user` u
        LEFT JOIN `profile` p ON u.profile_id = p.id
        SET u.profile_id = NULL
        WHERE u.profile_id IS NOT NULL AND p.id IS NULL;
    """)

    # 3️⃣ Now add the foreign key constraint
    op.create_foreign_key(
        'fk_user_profile',  # Name the constraint
        'user',
        'profile',
        ['profile_id'],
        ['id'],
        ondelete='SET NULL'  # Optional: automatically NULL out on profile delete
    )



def downgrade() -> None:
    """Downgrade schema."""
    # Drop the foreign key constraint
    op.drop_constraint('fk_user_profile', 'user', type_='foreignkey')

    # Revert profile_id to NOT NULL (if your model expects it)
    op.alter_column('user', 'profile_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

