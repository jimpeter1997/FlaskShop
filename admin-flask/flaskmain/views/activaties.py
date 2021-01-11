from . import admin_views
from flaskmain.utils.common import login_required
from flask import render_template
from flaskmain.models import Activaty





@admin_views.route('/activate')
@login_required
def activate():
    # company = CompanyInformation.query.filter_by(id=1).first()
    activaties = Activaty.query.all()
    ac_list = list()
    for ac in activaties:
        k = ac.__dict__
        del k["_sa_instance_state"]
        del k["update_time"]
        del k["create_time"]
        ac_list.append(k)

    context = {
        'title': "活动信息页面",
        'activaties': ac_list
    }
    return render_template('/admin/activate.html', context=context)
