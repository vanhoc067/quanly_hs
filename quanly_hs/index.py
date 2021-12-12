from flask import render_template, request, redirect, url_for
from quanly_hs import app, login
import utils
from flask_login import login_user, logout_user
from quanly_hs.admin import *
import cloudinary.uploader
from quanly_hs.models import UserRole




@app.route('/')
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

            return redirect(url_for('home'))
        except Exception as ex:
            err_msg = 'Đã xãy ra lỗi: ' + str(ex)
        else:
            err_msg = 'Mật khẩu không đúng!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)

            return redirect(url_for(request.args.get('next', 'home')))
        else:
            err_msg = 'Tên dăng nhập hoặc mật khẩu không chính xát!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def admin_signin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_login(username=username,
                            password=password,
                            role=UserRole.admin)
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


if __name__ == '__main__':
    app.run(debug=True)