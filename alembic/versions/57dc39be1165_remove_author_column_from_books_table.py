"""Remove author column from books table

Revision ID: 57dc39be1165
Revises: ff25c5328b64
Create Date: 2025-09-03 18:41:40.266540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = '57dc39be1165'
down_revision: Union[str, Sequence[str], None] = 'ff25c5328b64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
