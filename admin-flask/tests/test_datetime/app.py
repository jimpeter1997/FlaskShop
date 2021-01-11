from flask import Flask, render_template
from datetime import datetime
from flask_moment import Moment



app = Flask(__name__)
Moment(app)



@app.route("/", methods=['GET'])
def index():
    context = {
        "current_time": datetime.now().date()
    }
    return render_template("/index.html", context=context)


if __name__ == '__main__':
    app.run(debug=True)
