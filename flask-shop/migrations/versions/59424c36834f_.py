"""empty message

Revision ID: 59424c36834f
Revises: 5152dbb6b370
Create Date: 2020-09-07 23:54:08.806930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59424c36834f'
down_revision = '5152dbb6b370'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ishop_users', sa.Column('_user_passwd_hash', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ishop_users', '_user_passwd_hash')
    # ### end Alembic commands ###
