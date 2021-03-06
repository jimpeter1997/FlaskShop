"""init table

Revision ID: 030645f0b0a3
Revises: 
Create Date: 2020-08-30 00:51:31.805655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '030645f0b0a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ishop_goods_cates',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cate', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ishop_users',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=20), nullable=True),
    sa.Column('user_passwd_hash', sa.String(length=128), nullable=False),
    sa.Column('user_mobile', sa.String(length=11), nullable=False),
    sa.Column('user_real_name', sa.String(length=32), nullable=True),
    sa.Column('user_id_card', sa.String(length=20), nullable=True),
    sa.Column('user_avator_url', sa.String(length=128), nullable=True),
    sa.Column('user_money', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_mobile'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('ishop_users_levels',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level_name', sa.String(length=20), nullable=False),
    sa.Column('level_require', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('level_name'),
    sa.UniqueConstraint('level_require')
    )
    op.create_table('ishop_goods',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_activate', sa.Boolean(), nullable=False),
    sa.Column('good_name', sa.String(length=80), nullable=False),
    sa.Column('good_index_url', sa.String(length=256), nullable=False),
    sa.Column('good_price', sa.Float(), nullable=False),
    sa.Column('good_desc', sa.String(length=256), nullable=False),
    sa.Column('good_desc_details', sa.Text(), nullable=True),
    sa.Column('good_cate', sa.Integer(), nullable=True),
    sa.Column('is_good_in_zeros', sa.Boolean(), nullable=False),
    sa.Column('is_good_in_together', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['good_cate'], ['ishop_goods_cates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ishop_togethers',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('good_id', sa.Integer(), nullable=True),
    sa.Column('together_date', sa.DateTime(), nullable=False),
    sa.Column('together_count', sa.Integer(), nullable=False),
    sa.Column('together_deadline', sa.DateTime(), nullable=False),
    sa.Column('together_desc', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['good_id'], ['ishop_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ishop_users_address',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_address', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['ishop_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ishop_commons',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('good_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('common', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['good_id'], ['ishop_goods.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['ishop_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ishop_zeros',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('good_id', sa.Integer(), nullable=True),
    sa.Column('zero_datetime', sa.Integer(), nullable=True),
    sa.Column('zero_back_money', sa.Integer(), nullable=True),
    sa.Column('zero_desc', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['good_id'], ['ishop_goods.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ishop_orders',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('good_id', sa.Integer(), nullable=True),
    sa.Column('tracking_deadline', sa.DateTime(), nullable=True),
    sa.Column('tracking_number', sa.String(length=64), nullable=True),
    sa.Column('is_order_in_zeros', sa.Boolean(), nullable=False),
    sa.Column('order_zero', sa.Integer(), nullable=True),
    sa.Column('is_order_in_together', sa.Boolean(), nullable=False),
    sa.Column('order_together', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['good_id'], ['ishop_goods.id'], ),
    sa.ForeignKeyConstraint(['order_together'], ['ishop_togethers.id'], ),
    sa.ForeignKeyConstraint(['order_zero'], ['ishop_zeros.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['ishop_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ishop_orders')
    op.drop_table('ishop_zeros')
    op.drop_table('ishop_commons')
    op.drop_table('ishop_users_address')
    op.drop_table('ishop_togethers')
    op.drop_table('ishop_goods')
    op.drop_table('ishop_users_levels')
    op.drop_table('ishop_users')
    op.drop_table('ishop_goods_cates')
    # ### end Alembic commands ###
