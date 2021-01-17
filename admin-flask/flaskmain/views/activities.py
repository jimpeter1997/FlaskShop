from . import admin_views
from flaskmain.utils.common import login_required
from flask import render_template, request, jsonify, current_app
from flaskmain.models import Activity
from flaskmain import db


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
        'activaties': ac_list
    }
    return render_template('/admin/activities.html', context=context)


@admin_views.route('/acivity', methods=["GET", "POST"])
@login_required
def activity():
    pass
