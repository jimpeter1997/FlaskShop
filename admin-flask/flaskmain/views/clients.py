from . import admin_views
from flaskmain.utils.common import login_required
from flask import render_template
from flaskmain.models import UserInfo



@admin_views.route('/client')
@login_required
def client():
    # company = CompanyInformation.query.filter_by(id=1).first()
    users = UserInfo.query.all()
    print(users)
    context = {
        'title': "用户信息页面",
        'users': users
    }
    return render_template('/admin/client.html', context=context)
