"""Init

Revision ID: 03c4b131e977
Revises: 7da304fb9e47
Create Date: 2023-11-02 09:22:44.982374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03c4b131e977'
down_revision: Union[str, None] = '7da304fb9e47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('repoconfig_repo_id_fkey', 'repoconfig', type_='foreignkey')
    op.create_foreign_key(None, 'repoconfig', 'stage', ['repo_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'repoconfig', type_='foreignkey')
    op.create_foreign_key('repoconfig_repo_id_fkey', 'repoconfig', 'stage', ['repo_id'], ['id'])
    # ### end Alembic commands ###
