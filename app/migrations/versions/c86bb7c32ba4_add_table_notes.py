"""add table notes

Revision ID: c86bb7c32ba4
Revises: 24104b6e1e0c
Create Date: 2024-01-17 14:26:23.896841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c86bb7c32ba4'
down_revision = '24104b6e1e0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notes",
        sa.Column("note_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
        sa.Column(
            "created_by", sa.Integer, sa.ForeignKey("users.user_id"), nullable=True
        ),
        sa.Column(
            "updated_by", sa.Integer, sa.ForeignKey("users.user_id"), nullable=True
        ),
        sa.Column(
            "deleted_by", sa.Integer, sa.ForeignKey("users.user_id"), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_table("notes")
