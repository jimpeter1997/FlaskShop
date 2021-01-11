# 教过别人结果自己用到了

book_find = Business.query.all()
book_json = []

for book in book_find:
    book_item = book.__dict__
    if "_sa_instance_state" in book_item:
            del book_item["_sa_instance_state"]
    book_json.append(book_item)

return jsonify(book_json)
