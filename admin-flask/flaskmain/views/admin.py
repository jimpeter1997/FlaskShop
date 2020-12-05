from . import admin_views
from flask import render_template, session, request, current_app, flash, redirect, url_for, jsonify
from flaskmain.models import CompanyInformation
from flaskmain import db
from flaskmain.utils.common import is_string_validate, login_required



@admin_views.route('/company', methods=['GET', 'POST'])
@login_required
def company():
    company_info = CompanyInformation.query.filter_by(id=1).first()
    # user_id = session['_user_id']
    # company_info = CompanyInformation.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        # 获取提交数据
        post_request_dict = request.get_json()
        key = post_request_dict.get('key')
        value = post_request_dict.get('value')
        # 检验数据
        # 判断数据是否包含特殊字符
        if is_string_validate(key) or is_string_validate(value):
            return jsonify(resCode='1', message="参数不合法")
        # 判断key这个关键词是否在CompanyInformation类的属性中
        if key not in [i for i in dir(CompanyInformation) if not hasattr(getattr(CompanyInformation, i), "__call__")]:
            return jsonify(resCode='1', message="参数不合法")
        # 开始修改
        try:
            CompanyInformation.query.filter_by(id=1).update({key: value})
            db.session.commit()
            company_info = CompanyInformation.query.filter_by(id=1).first()
            res = getattr(company_info, key)
            return jsonify(resCode='0', message="提交成功",data=res)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode='1', message="数据库错误，请联系管理员")

    context = {
        'title': "商城基本信息页面",
        'company_info': [
            {'key':'company_name','value': company_info.company_name, 'text':"商城名称"},
            {'key': 'web_title', 'value': company_info.web_title, 'text':"网站标题"},
            {'key': 'web_key_wrods', 'value': company_info.web_key_wrods, 'text':"网站关键词"},
            {'key': 'web_description', 'value': company_info.web_description, 'text':"网站描述"},
            {'key': 'web_copyright', 'value': company_info.web_copyright, 'text':"网站版权信息"},
            {'key': 'ronglianyun_accId', 'value': company_info.ronglianyun_accId, 'text':"容连云accId"},
            {'key': 'ronglianyun_accToken', 'value': company_info.ronglianyun_accToken, 'text':"容连云accToken"},
            {'key': 'ronglianyun_appId', 'value': company_info.ronglianyun_appId, 'text':"容连云appId"},
            {'key': 'qiniu_acess_key', 'value': company_info.qiniu_acess_key, 'text':"七牛云acess_key"},
            {'key': 'qiniu_secret_key', 'value': company_info.qiniu_secret_key, 'text':"七牛云secret_key"}
        ]
    }
    return render_template('/admin/company.html', context=context)






@admin_views.route('/activate')
@login_required
def activate():
    # company = CompanyInformation.query.filter_by(id=1).first()
    context = {
        'title': "活动信息页面"
    }
    return render_template('/admin/activate.html', context=context)


@admin_views.route('/adminuser')
@login_required
def adminuser():
    # company = CompanyInformation.query.filter_by(id=1).first()
    context = {
        'title': "管理后台管理员页面"
    }
    return render_template('/admin/adminuser.html', context=context)
