import sqlalchemy as sa

from src.database import metadata
accounts = sa.Table(
    "accounts",
    metadata,       
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer, nullable=False, index=True),
    sa.Column("balance", sa.Numeric(15, 2), nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now())
)