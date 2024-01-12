"""book, category, author 

Revision ID: 3de08125e5b7
Revises: 69e3c8e83525
Create Date: 2024-01-12 14:53:38.460640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3de08125e5b7'
down_revision: Union[str, None] = '69e3c8e83525'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_membership',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'BLOCKED', name='membershipstatus'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_membership_id'), 'user_membership', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_membership_id'), table_name='user_membership')
    op.drop_table('user_membership')
    # ### end Alembic commands ###
