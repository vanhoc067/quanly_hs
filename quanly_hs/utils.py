import json, os
from quanly_hs import app, db
import  hashlib
from quanly_hs.models import User, UserRole


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password, role=UserRole.user):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)