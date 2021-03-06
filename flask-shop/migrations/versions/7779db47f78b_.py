"""empty message

Revision ID: 7779db47f78b
Revises: 1bbd3d5c9c45
Create Date: 2020-09-08 00:11:10.192154

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7779db47f78b'
down_revision = '1bbd3d5c9c45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ishop_users', sa.Column('user_passwd_hash', sa.String(length=128), nullable=False))
    op.drop_column('ishop_users', 'user_passwd_hash_real')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ishop_users', sa.Column('user_passwd_hash_real', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('ishop_users', 'user_passwd_hash')
    # ### end Alembic commands ###
