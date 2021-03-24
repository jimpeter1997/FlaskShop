from . import admin_views
from flaskmain.utils.common import login_required
from flask import render_template, request, jsonify, current_app, flash
from flaskmain.models import Activity
from flaskmain import db
from flaskmain.forms import ActivityForm


# 增删改查
# post、delete、put、get


@admin_views.route('/activities', methods=["GET", "PUT", "DELETE"])
@login_required
def activities():
    # 删除活动
    if request.method == "DELETE":
        print("DELETE")
        postdata = request.get_json()
        delete_activity_id = postdata.get("delete_activity_id")
        if delete_activity_id == None:
            # 判断id是否为空
            return jsonify(resCode=1, msg="id不能为空")
        try:
            activity = activity.query.filter_by(id=int(delete_activity_id)).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库错误，联系管理员处理")

        if activity == None:
            return jsonify(resCode=1, msg="id错误，删除无效")

        # 删除该活动
        # db.delete(activity)
        # db.commit()

        print("其实删除已经成功了")
        return jsonify(resCode=0, msg="删除成功")
    # 修改活动
    if request.method == "PUT":
        pass
    # 添加活动
    if request.method == "POST":
        pass
    # 展示活动
    # company = CompanyInformation.query.filter_by(id=1).first()
    activaties = Activity.query.all()
    ac_list = list()
    for ac in activaties:
        k = ac.__dict__
        del k["_sa_instance_state"]
        del k["update_time"]
        del k["create_time"]
        ac_list.append(k)

    context = {
        'title': "活动信息页面",
        'activities': ac_list
    }
    return render_template('/admin/activities.html', context=context)


@admin_views.route('/add/activity', methods=["GET", "POST"])
@login_required
def activity():
    form = ActivityForm()

    context = {
        'title': "添加活动信息页面"
    }
    if request.method == 'POST':
        if form.validate_on_submit():
            print("form.validate_on_submit() = ", form.validate_on_submit())
        # flash("测试flash！")
        # flash('message')
        # for me in form.data:
        #     print(me)
        # print("form.start_time.message = ", form.start_time.message)
        print("form.validate_on_submit() = ", form.validate_on_submit())
        print("form.activity_name.data = ", form.activity_name.data)
        print("form.start_time.data = ", form.start_time.data)
        print("form.close_time.data = ", form.close_time.data)
        print("form.desc.data = ", form.desc.data)
        print("form.off_percent.data = ", form.off_percent.data)
        print("form.package_time.data = ", form.package_time.data)
        print("form.is_active.data = ", form.is_active.data)
        print("form.count.data = ", form.count.data)
        print("POST")
        return render_template('/admin/add_activity.html',context=context, form=form)
    return render_template('/admin/add_activity.html',context=context, form=form)


@admin_views.route('/add/new/activity', methods=["GET", "POST"])
@login_required
def new_activity():
    form = ActivityForm()
    context = {
        'title': "不用wtforms添加活动信息页面"
    }
    return render_template('/admin/add_activity_without_wtforms.html', context=context)
