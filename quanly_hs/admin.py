from flask_admin.contrib.sqla import ModelView
from quanly_hs.models import Student, Class, UserRole, Subject, Score
from quanly_hs import app, db, utils
from flask_admin import Admin, BaseView, expose
from flask_babelex import Babel
from flask_login import current_user, logout_user
from flask import redirect


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin



class View(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    details_modal = True


class StudentView(View):
    column_display_pk = True
    column_filters = ['name', 'class']
    column_searchable_list = ['name']
    column_labels = {
        'id':'Mã HS',
        'name': 'Tên HS',
        'gender': 'Giới tính',
        'date_of_birth':'Ngày sinh',
        'address':'Địa chỉ',
        'phone':'sđt',
        'class':'Lớp'
    }
    form_excluded_columns = ['score_student']


class ScoreView(View):
    column_filters = ['class.class_name','student.name']
    column_searchable_list = ['student.name']
    column_labels = {
        'student': 'Tên học sinh',
        'class': 'Lớp',
        'subject': 'Môn học',
        'semester': 'Học kì',
        'school_year': 'Năm học',
        'score_15_minutes_1': 'Điểm 15(1)',
        'score_15_minutes_2': 'Điểm 15(2)',
        'score_1_period': 'Điểm 1 tiết',
        'semester_exam_score': 'Điểm cuối kì'
    }


class classView(View):
    column_display_pk = True
    column_labels = {
        'id': 'Mã lớp',
        'class_name': 'Tên lớp',
        'grade': 'Khối',
        'quantity': 'Sĩ số',
        'students': 'Học sinh'
    }

    form_excluded_columns = ['score_class']


class subjectView(AuthenticatedModelView):
    column_display_pk = True
    column_labels = {
        'id': 'Mã môn học',
        'name': 'Tên môn học'
    }

    form_excluded_columns = ['score_subject']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated





admin = Admin(app=app, name='QUẢN TRỊ HỌC SINH', template_mode='bootstrap4')
admin.add_view(StudentView(Student, db.session, name='Danh sách HS'))
admin.add_view(classView(Class, db.session, name='Danh sách lớp'))
admin.add_view(subjectView(Subject, db.session, name='Danh sách môn học'))
admin.add_view(ScoreView(Score, db.session, name='Bảng điểm'))
admin.add_view(LogoutView(name='Đăng xuất'))



babel = Babel(app=app)
@babel.localeselector
def get_locale():
        return 'vi'