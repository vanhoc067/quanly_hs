from flask import render_template, request, redirect, url_for
from quanly_hs import app, login
import utils
from flask_login import login_user, logout_user
from quanly_hs.admin import *
import cloudinary.uploader
from quanly_hs.models import UserRole
from datetime import datetime
import math




@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')

        if password.strip().__eq__(confirm.strip()):
            file = request.files.get('avatar')
            avatar = None
            if file:
                res = cloudinary.uploader.upload(file)
                avatar = res['secure_url']

            try:
                utils.add_user(name=name, password=password,
                               username=username, email=email,
                               avatar=avatar)

                return redirect(url_for('user_signin'))
            except Exception as ex:
                err_msg = 'Đã xãy ra lỗi: ' + str(ex)
        else:
            err_msg = 'Mật khẩu không đúng!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/', methods=['get','post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        userrole = request.form.get('sellist1')

        user = utils.check_login(username=username, password=password, userrole=userrole)
        if user:
            login_user(user=user)

            return redirect(url_for('home'))
        else:
            err_msg = 'Thông tin đăng nhập không chính xát!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def admin_signin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_login(username=username,
                            password=password,
                            userrole=UserRole.admin)
    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/tiep_nhan_hoc_sinh')
def tiepnhanhocsinh():
    return render_template('tiepnhanhocsinh.html')


@app.route('/danh_sach_hoc_sinh')
def dshocsinh():

    page = request.args.get('page', 1)
    student = utils.load_student(page=int(page))
    conut = utils.count_student()

    return render_template('dshocsinh.html',
                           students=student,
                           pages=math.ceil(conut/app.config['PAGE_SIZE']))


@app.route('/danh_sach_lop')
def dslop():

    classs = utils.load_class()

    return render_template('dslop.html', classs=classs)


@app.route("/Chi_tiet_lop/<int:classs_id>")
def class_detail(classs_id):

    student = utils.get_student_by_class_id(classs_id)
    return render_template('chitietlop.html',
                           student=student)


@app.route('/bang_diem')
def bangdiem():

    info = utils.subject_class_score()

    return render_template('bangdiem.html', info=info)


@app.route('/xuat_bang_diem')
def xuatbangdiem():

    infor = utils.score_student_class()
    school_year = '2021'

    return render_template('xuatbangdiem.html', infor=infor, school_year=school_year)


@app.route('/chi_tiet_bang_diem/<int:score_class>,<int:score_subject>,<string:score_classname>, <string:score_subjectname>, <string:score_year>')
def chitietbangdiem(score_class, score_subject, score_classname, score_subjectname, score_year):

    score = utils.get_score_by_subject(score_class, score_subject)
    score_classname = score_classname
    score_subjectname = score_subjectname
    score_year = score_year

    return render_template('chitietbangdiem.html', score=score, score_classname=score_classname, score_subjectname=score_subjectname, score_year=score_year)


@app.route('/register_student', methods=['post'])
def register_student():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        gender = request.form.get('gender')
        date_of_birth = request.form.get('date_of_birth')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        class_id = request.form.get('class_id')

        if int(datetime.now().year).__eq__(2007):
            # if int(datetime.now().year-datetime(date_of_birth).year).__le__(15) and int(datetime.now().year-datetime(date_of_birth).year).__ge__(20):

            try:
                utils.add_student(name=name, gender=gender,
                               date_of_birth=date_of_birth, address=address,
                               phone=phone, email=email, class_id=class_id)

                return redirect(url_for('dshocsinh'))
            except Exception as ex:
                err_msg = 'Đã xãy ra lỗi: ' + str(ex)
        else:
            err_msg = 'Học sinh phải có độ tuổi từ 15 đến 20'

    return render_template('tiepnhanhocsinh.html', err_msg=err_msg)


@app.route('/Thong_ke_so_luong')
def thongkesoluong():

    stats = utils.class_stats()

    return render_template('thongkesoluong.html', stats=stats)


@app.route('/Thong_ke_bao_cao')
def thongkebaocao():

    stats1 = utils.Score_stats_toan()
    stats2 = utils.Score_stats_van()

    return render_template('thongkebaocao.html', stats1=stats1, stats2=stats2)



if __name__ == '__main__':
    app.run(debug=True)