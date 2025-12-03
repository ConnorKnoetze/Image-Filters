from flask import render_template, Blueprint

from filters.blueprints.services import get_nav_items

index_bp = Blueprint("index",__name__)

@index_bp.route('/')
def index():
    nav_items = get_nav_items()
    return render_template("/pages/index/index.html", nav_items = nav_items)