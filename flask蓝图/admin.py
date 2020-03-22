from flask import Blueprint,render_template, request

admin = Blueprint('admin',__name__)


@admin.route('/')
def admin_home():
    return 'admin_home'

@admin.route('/new')
def new():
    return 'new'

@admin.route('/edit')
def edit():
    return 'edit'

@admin.route('/publish')
def publish():
    return 'publish'

