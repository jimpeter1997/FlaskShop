from . import admin_views
from flaskmain.utils.common import login_required
from flask import render_template, request, jsonify, current_app, flash
from flaskmain.models import Activity
from flaskmain import db
from flaskmain.forms import ActivityForm
from flaskmain.utils.common import is_string_validate
from datetime import datetime

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
        # var data = {
        #     "id": id,
        #     "activity_name": activity_name,
        #     "start_time": start_time,
        #     "close_time": close_time,
        #     "activity_desc": activity_desc,
        #     "off_percent": off_percent,
        #     "package_time": package_time,
        #     "is_active": is_active
        # };
        print("PUT is asked")
        put_data = request.get_json()
        id = put_data.get("id")
        activity_name = put_data.get("activity_name")
        activity_desc = put_data.get("activity_desc")
        start_time = put_data.get("start_time")
        close_time = put_data.get("close_time")
        off_percent = put_data.get("off_percent")
        package_time = put_data.get("package_time")
        is_active = put_data.get("is_active")
        print("id = ", id, "type(id) = ", type(id))
        print("activity_name = ", activity_name, "type(activity_name) = ", type(activity_name))
        print("activity_desc = ", activity_desc, "type(activity_desc) = ", type(activity_desc))
        print("start_time = ", start_time, "type(start_time) = ", type(start_time))
        print("close_time = ", close_time, "type(close_time) = ", type(close_time))
        print("off_percent = ", off_percent, "type(off_percent) = ", type(off_percent))
        print("package_time = ", package_time, "type(package_time) = ", type(package_time))
        print("is_active = ", is_active, "type(is_active) = ", type(is_active))
        # 这里有一个小bug，不要把bealean类型放到all里面去判断，true的时候没有问题，但是false的时候会出错
        if not all([id, activity_name, activity_desc, start_time, close_time, off_percent, package_time]):
            return jsonify(resCode=1, msg="数据不完整！")
        # ac = Activity()
        try:
            ac = Activity.query.filter_by(id=int(id)).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库链接错误，请联系管理员处理")
        if ac == None:
            return jsonify(resCode=1, msg="输入id有误，请重新测试")

        if is_string_validate(activity_name) or is_string_validate(activity_desc):
            return jsonify(resCode=1, msg="活动名称和活动描述不能包含特殊字符")
        ac.activity_name = activity_name
        ac.activity_desc = activity_desc

        try:
            ac.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            ac.close_time = datetime.strptime(close_time, "%Y-%m-%d %H:%M:%S")
            ac.package_time = datetime.strptime(package_time, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="时间格式不正确，或者时间错误")

        print("ac.start_time > ac.close_time = ", ac.start_time > ac.close_time)
        print("ac.close_time >= ac.package_time = ", ac.close_time >= ac.package_time)

        if (ac.start_time > ac.close_time) or (ac.close_time >= ac.package_time):
            # 判断时间是否正确
            return jsonify(resCode=1, msg="发货时间要大于活动截至时间，活动截至时间要大于活动开始时间")

        if not isinstance(is_active, bool):
            return jsonify(resCode=1, msg="输入是否激活数据错误")
        ac.is_active = is_active
        if int(off_percent) >= 100 and int(off_percent) > 0:
            return jsonify(resCode=1, msg="输入的折扣不正确")
        ac.off_percent = int(off_percent)

        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库链接有误，请联系管理员处理")

        return jsonify(resCode=0, msg="修改成功")
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


@admin_views.route('/add/new/activity', methods=["GET", "POST", "DELETE", "PUT"])
@login_required
def new_activity():
    if request.method == "POST":
        post_data = request.get_json()
        print("request.method = POST : ", request.get_json())
        # activity_name
        # start_time
        # close_time
        # activity_desc
        # off_percent
        # package_time
        # is_active
        activity_name = post_data.get("activity_name")
        start_time = post_data.get("start_time")
        close_time = post_data.get("close_time")
        activity_desc = post_data.get("activity_desc")
        off_percent = post_data.get("off_percent")
        package_time = post_data.get("package_time")
        is_active = post_data.get("is_active")
        # print("activity_name = ", activity_name)
        # print("start_time = ", type(start_time))
        # print("close_time = ", close_time)
        # print("off_percent = ", off_percent)
        # print("package_time = ", package_time)
        # print("is_active = ", type(is_active))
        # print("count = ", type(count))
        # print("activity_desc = ", activity_desc)
        # 这里有一个小bug，不要把bealean类型放到all里面去判断，true的时候没有问题，但是false的时候会出错
        if not all([activity_name, start_time, close_time, activity_desc, off_percent, package_time]):
            # 判断数据是否为空
            return jsonify(resCode=1, msg="数据不完整")

        if is_string_validate(activity_name) or is_string_validate(activity_desc):
            return jsonify(resCode=1, msg="活动名称和活动描述不能包含特殊字符")

        ac = Activity()
        ac.activity_name = activity_name
        ac.activity_desc = activity_desc
        try:
            ac.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            ac.close_time = datetime.strptime(close_time, "%Y-%m-%d %H:%M:%S")
            ac.package_time = datetime.strptime(package_time, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="时间格式不正确，或者时间错误")

        if (ac.start_time > ac.close_time) or (ac.close_time >= ac.package_time):
            # 判断时间是否正确
            return jsonify(resCode=1, msg="发货时间要大于活动截至时间，活动截至时间要大于活动开始时间")

        if not isinstance(is_active, bool):
            return jsonify(resCode=1, msg="输入是否激活数据错误")
        ac.is_active = is_active
        if int(off_percent) >= 100 and int(off_percent) > 0:
            return jsonify(resCode=1, msg="输入的折扣不正确")
        ac.off_percent = int(off_percent)
        db.session.add(ac)
        db.session.commit()
        return jsonify(resCode=0, msg="提交成功")
    form = ActivityForm()
    context = {
        'title': "不用wtforms添加活动信息页面"
    }
    return render_template('/admin/add_activity_without_wtforms.html', context=context)
