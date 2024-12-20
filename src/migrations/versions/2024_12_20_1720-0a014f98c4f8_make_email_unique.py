"""make email unique

Revision ID: 0a014f98c4f8
Revises: a837ea8d7e62
Create Date: 2024-12-20 17:20:08.319291

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0a014f98c4f8"
down_revision: Union[str, None] = "a837ea8d7e62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
