"""add qualify users

Revision ID: e86489b3b5bd
Revises:
Create Date: 2024-12-25 03:00:00.000000

"""
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e86489b3b5bd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade(op=None):
    op.create_table(
        "qualify_users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String(128), unique=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade(op=None) -> None:
    op.drop_table("qualify_users")
