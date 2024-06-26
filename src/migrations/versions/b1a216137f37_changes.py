"""changes

Revision ID: b1a216137f37
Revises: 92e6130c2364
Create Date: 2024-05-17 03:46:19.443559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1a216137f37'
down_revision: Union[str, None] = '92e6130c2364'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('training_configurations_name_key', 'training_configurations', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('training_configurations_name_key', 'training_configurations', ['name'])
    # ### end Alembic commands ###
