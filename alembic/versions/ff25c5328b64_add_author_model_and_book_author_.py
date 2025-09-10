"""Add author model and book-author association table; drop author column from books

Revision ID: ff25c5328b64
Revises: 1d8542fd9741
Create Date: 2025-09-03 15:22:39.341398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = 'ff25c5328b64'
down_revision: Union[str, Sequence[str], None] = '1d8542fd9741'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.drop_column('books', 'author')

    
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('biography', sa.Text(), nullable=True),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('nationality', sa.String(), nullable=True),
    )
    
    op.create_table(
        'book_author',
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table('book_author')
    op.drop_table('authors')

    
    op.add_column('books', sa.Column('author', sa.VARCHAR(), nullable=False))
