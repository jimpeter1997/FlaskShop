from . import  admin_views
from flaskmain.utils.common import login_required
from flask import render_template
from flaskmain.models import GoodsKinds, Goods



@admin_views.route('/goods')
@login_required
def goods():
    # company = CompanyInformation.query.filter_by(id=1).first()
    goods_kinds = GoodsKinds.query.all()
    goods = Goods.query.all()
    context = {
        'title': "商品信息页面"
    }
    return render_template('/admin/goods.html', context=context)
