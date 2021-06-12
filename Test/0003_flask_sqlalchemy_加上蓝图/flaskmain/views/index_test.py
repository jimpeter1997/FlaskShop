# from flaskmain.models import User
from . import admin_views



@admin_views.route('/')
def index():
    return "Index Page"
