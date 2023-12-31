"""Init

Revision ID: b571d9002c87
Revises: f53640addfb8
Create Date: 2023-11-06 12:15:57.311756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b571d9002c87'
down_revision: Union[str, None] = 'f53640addfb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staging', sa.Column('webhook_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staging', 'webhook_id')
    # ### end Alembic commands ###
