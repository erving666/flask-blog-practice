from flask import Blueprint

bp = Blueprint('views_bp', __name__ ,template_folder = "../../app_frontend/dist/",static_folder = "../../app_frontend/dist/wx/lib" ,url_prefix='/wx')

# from myblog.views import xx