from . import admin_views
# from flaskmain.models import User
from flaskmain.models import User


@admin_views.route('/')
def index():
    return "Hello Flask"
