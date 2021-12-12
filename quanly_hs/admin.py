from flask_admin.contrib.sqla import ModelView
from quanly_hs.models import DanhSachHS, DanhSachLop, UserRole
from quanly_hs import app, db, utils
from flask_admin import Admin, BaseView, expose
from flask_babelex import Babel
from flask_login import current_user, logout_user
from flask import redirect


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin




class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated





admin = Admin(app=app, template_mode='bootstrap4')
admin.add_view(AuthenticatedModelView(DanhSachHS, db.session, name='Danh sach HS'))
admin.add_view(AuthenticatedModelView(DanhSachLop, db.session, name='Danh sach Lop'))
admin.add_view(LogoutView(name='Đăng xuất'))



babel = Babel(app=app)
@babel.localeselector
def get_locale():
        return 'vi'