from . import  admin_views
from flaskmain.utils.common import login_required, is_string_validate
from flask import render_template, request, jsonify, current_app, redirect, url_for
from flaskmain.models import GoodsKinds, Goods, Activity
from flaskmain import db


"""
GET:
POST:
PUT:
DELETE:
"""


@admin_views.route('/goods', methods=["GET", "POST", "DELETE", "PUT"])
@login_required
def goods():
    if request.method == "POST":
        # 添加分类的接口
        print("request.method = POST : ", request.get_json())
        post_data = request.get_json()
        goods_kind_name = post_data.get("kind_name")
        goods_kind_index = int(post_data.get("kind_index"))
        # 判断goods_kind_index是否为数字
        # if not isinstance(goods_kind_index, int):
        #     goods_kind_index = 100

        if is_string_validate(goods_kind_name):
            return jsonify(resCode=1, msg="商品分类不能包含特殊字母")

        print(goods_kind_index, "----", goods_kind_name)

        # return jsonify(error=1, msg="开始提交商品 ！")
        try:
            goods_kind = GoodsKinds()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库错误，联系管理员处理")

        goods_kind.goods_kind_name = goods_kind_name
        goods_kind.goods_kind_index = goods_kind_index
        db.session.add(goods_kind)
        db.session.commit()
        return jsonify(resCode=0, msg="商品分类提交成功 ！ ")

    if request.method == "DELETE":
        # 删除分类的接口
        print("request.method = DELETE : ", request.get_json())
        delete_data = request.get_json()
        delete_kind_id = delete_data.get("kind_id")
        print("delete_kind_id = ", delete_kind_id)
        try:
            delete_kind = GoodsKinds.query.filter_by(id=int(delete_kind_id)).first()
            is_goods_in_delete_kind = Goods.query.filter_by(good_kind_id=int(delete_kind_id))
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="商品ID不存在，或者数据库链接错误")
        if is_goods_in_delete_kind is not None:
            # 还有这个分类下的产品，不允许删除这个分类
            return jsonify(resCode=1, msg="这个分类下还有产品，不允许删除该分类，清空该分类下的产品！")
        if delete_kind == None:
            return jsonify(resCode=1, msg="要删除的分类不存在！")
        db.session.delete(delete_kind)
        db.session.commit()
        return jsonify(resCode=0, msg="删除成功 ！")

    if request.method == "PUT":
        print("PUT: ", request.get_json())
        put_data = request.get_json()
        id = int(put_data.get("id"))
        kind_name = put_data.get("kind_name")
        kind_index = int(put_data.get("kind_index"))
        if not all([id, kind_name, kind_index]):
            return jsonify(resCode=1, msg="参数不完整")

        if is_string_validate(kind_name):
            return jsonify(error=1, msg="商品分类不能包含特殊字母")

        try:
            kind = GoodsKinds.query.filter_by(id=id).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="链接数据库错误，请联系管理员")
        if kind == None:
            return jsonify(resCode=1, msg="id错误，请确认输入的id是否有误")

        kind.goods_kind_name = kind_name
        kind.goods_kind_index = kind_index
        db.session.commit()

        return jsonify(resCode=0, msg="修改成功！")

    k = request.args.get('k')
    if k is not None:
        # 说明这个是来请求某个分类下的产品的
        try:
            goods_in_k_kind = Goods.query.filter_by(good_kind_id=k).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库链接错误，请联系管理员处理")
        if goods_in_k_kind == None:
            return jsonify(resCode=1, msg="查询的商品种类不存在，请确认后重新查询")
        data = dict()
        for good in goods_in_k_kind:
            good_items = good.__dict__
            del good_items["_sa_instance_state"]
            del good_items["create_time"]
            del good_items["update_time"]
            data["goods"].append(good_items)
        try:
            goods_kinds = GoodsKinds.query.all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库错误，请联系管理员处理")
        if goods_kinds == None:
            return jsonify(resCode=1, msg="产品分类为空")
        for goods_kind in goods_kinds:
            goods_kind_items = goods_kind.__dict__
            del goods_kind_items["_sa_instance_state"]
            del goods_kind_items["create_time"]
            del goods_kind_items["update_time"]
            # 放入产品分类信息
            data.get("kinds").append(goods_kind_items)
        return jsonify(resCode=0, msg="查询成功", data=data)


    else:
        # company = CompanyInformation.query.filter_by(id=1).first()
        goods_kinds = GoodsKinds.query.all()
        goods = Goods.query.all()
        context = {
            'title': "商品信息页面",
            "goods_kinds": goods_kinds,
            "goods": goods
        }
        return render_template('/admin/goods.html', context=context)



@admin_views.route('/add/good', methods=["GET", "POST"])
@login_required
def add_good():
    # if request.method == ""
    goods_kinds = GoodsKinds.query.all()
    activities = Activity.query.all()
    context = {
        'title': "商品信息页面",
        "goods_kinds": goods_kinds,
        "activities": activities
    }
    if request.method == "POST":
        print("request.method  POST request.get_json() = ", request.get_json())
        print("request = ", request)
        print("request.files = ", request.files)
        print("type(request.files) = ", type(request.files))
        # file = request.files.get('good_main_pic')
        file = request.files['good_main_pic']
        print("file = ", file)
        print("type(file) = ", type(file))
        print(request.args.to_dict())
        print("request.get_data() = ", request.get_data())
        print("request.data = ", request.data)
        print("request.form = ", request.form.to_dict())
        print("dir(request) = ", dir(request))
        # return jsonify(resCode=0, msg="上传成功")
        # return redirect(url_for('views.add_good'))
    return render_template('/admin/good_editor.html', context=context)
