from . import admin_views
from flask import render_template
from adminshop.models import TestUser


# @admin_views.route('/test', methods=['GET'])
# def test():
#     return 'test flask'
@admin_views.route('test')
def test():
    context = {
        'title': "测试标题"
    }
    user = TestUser.query()
    return render_template('base.html', context=context)