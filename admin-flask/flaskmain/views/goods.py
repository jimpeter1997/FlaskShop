from . import  admin_views
from flaskmain.utils.common import login_required, is_string_validate, str_to_bool_else_return_none
from flask import render_template, request, jsonify, current_app, redirect, url_for
from flaskmain.models import GoodsKinds, Goods, Activity
from flaskmain import db
from fdfs_client.client import Fdfs_client, get_tracker_conf
import json

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



"""
file_bytes = filestorage.read()
"""
@login_required
@admin_views.route('/add/good', methods=["GET", "POST"])
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
        # 获取数据
        # 校验数据
        # 存入数据库
        # 返回信息
        # $("#good_name")
        # $("#good_desc")
        # $("#good_kind_id")
        # $("#good_main_pic")
        # $("#good_price")
        # $("#activities")
        print("POST 请求开始")
        ac_ids = [i.id for i in activities]
        kinds_ids = [i.id for i in goods_kinds]

        post_data_json = request.form.to_dict()

        good_name = post_data_json.get('good_name')
        # 商品名称不能空
        if good_name == None or is_string_validate(good_name):
            flash("产品名字不能包含特殊字符, 或者为空")
            return jsonify(resCode=1, msg="产品名字不能包含特殊字符, 或者为空")

        good_desc = post_data_json.get('good_desc')
        # 描述允许为空
        if is_string_validate(good_desc):
            return jsonify(resCode=1, msg="产品描述不能包含特殊字符")

        good_kind_id = post_data_json.get('good_kind_id')
        if good_kind_id == None:
            return jsonify(resCode=1, msg="产品分类不能为空")
        try:
            good_kind_id = int(good_kind_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="产品分类不正确1")

        if good_kind_id not in kinds_ids:
            return jsonify(resCode=1, msg="产品分类不正确2")

        good_price = post_data_json.get('good_price')
        if good_price == None:
            return jsonify(resCode=1, msg="产品价格不能空")
        try:
            good_price = float(good_price)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="产品价格错误")

        good_main_pic = request.files['good_main_pic']
        if good_main_pic == None:
            return jsonify(resCode=1, msg="产品主图不能为空")
        else:
            filename = good_main_pic.filename.split('.')[-1].lower()
            if filename not in current_app.config.get("ALLOWED_FILENAMES"):
                return jsonify(resCode=1, msg="图片格式不正确")
            file_bytes = good_main_pic.read()
            client_conf = current_app.config.get('FDFS_CONF')
            client = Fdfs_client(client_conf)
            try:
                resp = client.upload_by_buffer(file_bytes, filename)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(resCode=1, msg="图片上传失败,联系管理员处理1")
            if resp.get("Status") == "Upload successed.":
                good_main_pic = resp.get("Remote file_id").decode()
            else:
                return jsonify(resCode=1, msg="图片上传失败,联系管理员处理2")


        good_activities = post_data_json.get('activities')
        print("good_activities1 = ", good_activities)
        if good_activities == None:
            pass
        else:
            ac_array = good_activities.split(',')
            ac_array_int = []
            for i in ac_array:
                try:
                    i = int(i)
                except Exception as e:
                    current_app.logger.error(e)
                    return jsonify(resCode=1, msg="产品分类错误1")
                if i not in ac_ids:
                    return jsonify(resCode=1, msg="产品分类错误2")
                ac_array_int.append(i)
            good_activities = ac_array_int

        print("good_activities2 = ", good_activities)
        # 写入数据库
        good = Goods()
        # good_kind_id  一对多的关系
        # good.good_kind_id = GoodsKinds.query.filter_by(id=good_kind_id).first()
        print("good_kind_id = ", good_kind_id)
        print("type(good_kind_id) = ", type(good_kind_id))
        try:
            good.good_kind_id = GoodsKinds.query.filter_by(id=good_kind_id).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库链接错误,联系管理员处理1")
        good.good_name = good_name
        good.good_price = good_price
        good.good_desc = good_desc
        good.good_main_pic = good_main_pic
        # activities 多对多的关系
        # good.activities = []
        print("good_activities = ", good_activities)
        for i in good_activities:
            # good.activities.append(Activity.query.filter_by(id=i).first())
            print("i = ", i)
            print("type(i) = ", type(i))
            print("good.activities1 = ", good.activities)
            ac_id = Activity.query.filter_by(id=i).first()
            print("good.activities3 = ", good.activities)
            print("good.activities = ", good.activities)
            print("type(good.activities)", type(good.activities))
            print("ac_id = ", ac_id)
            print("type(ac_id) = ", type(ac_id))
            good.activities.append(ac_id)
            print("good.activities2 = ", good.activities)
            try:
                print("i00000 = ", i)
                # print("type(i) = ", type(i))
                # print("good.activities1 = ", good.activities)
                # ac_id = Activity.query.filter_by(id=i).first()
                # print("good.activities3 = ", good.activities)
                # print("good.activities = ", good.activities)
                # print("type(good.activities)", type(good.activities))
                # print("ac_id = ", ac_id)
                # print("type(ac_id) = ", type(ac_id))
                # good.activities.append(ac_id)
                # print("good.activities2 = ", good.activities)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(resCode=1, msg="数据库链接错误,联系管理员处理2")

        # db.session.add(good)
        # db.session.commit()
        return jsonify(resCode=0, msg="上传成功")
        print("开始保存")
        try:
            db.session.add(good)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(resCode=1, msg="数据库链接错误,联系管理员处理3")
        print("保存成功")


        print('ac_array = ', ac_array)
        print('type(ac_array) = ', type(ac_array))
        # for ac in activities:
        #     ac.id

        # good_price = str_to_bool_else_return_none(good_price)
        # if  good_price == None:
        #     return jsonify(resCode=1, msg="参数有误")

        # print("request.method  POST request.get_json() = ", request.get_json())
        # print("request = ", request)
        # print("request.files = ", request.files)
        # print("type(request.files) = ", type(request.files))
        # file = request.files.get('good_main_pic')
        file = request.files['good_main_pic']
        # print("file = ", file)
        print("file.filename = ", file.filename)
        print("file.filename.split('.')[-1].lower() = ", file.filename.split('.')[-1].lower())
        # print("type(file) = ", type(file))
        file_bytes = file.read()
        # client_conf = get_tracker_conf('/home/alex/programs/client.conf')
        client_conf = current_app.config.get('FDFS_CONF')
        print("client_conf = ", client_conf)
        client = Fdfs_client(client_conf)
        resp = client.upload_by_buffer(file_bytes, 'jpg')
        print("resp = ", resp)
        # print("file_bytes = ", file_bytes)
        # print("type(file_bytes) = ", type(file_bytes))
        # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

        print(request.args.to_dict())
        print("request.get_data() = ", request.get_data())
        print("request.form = ", request.form)
        print("request.form.to_dict() = ", request.form.to_dict())
        print("dir(request) = ", dir(request))
        return jsonify(resCode=0, msg="上传成功")
        # return redirect(url_for('views.goods'))
        # return render_template('/admin/good_editor.html', context=context)
    return render_template('/admin/good_editor.html', context=context)
