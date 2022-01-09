import json, os
from quanly_hs import app, db
import hashlib
from quanly_hs.models import User, UserRole
from quanly_hs.models import Class, Student, Score, Subject
from sqlalchemy import func


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password, userrole):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(userrole)).first()


def class_stats():
    return db.session.query(Class.id, Class.class_name, func.count(Student.id))\
                     .join(Student, Class.id.__eq__(Student.class_id), isouter=True)\
                     .group_by(Class.id, Class.class_name).all()


def Score_stats_toan(kw=None, from_date=None, to_date=None, summary=5):
    q = db.session.query(Class.class_name, Class.quantity, func.count(Score.semester_exam_score), func.count(Score.semester_exam_score)/Class.quantity*100)\
                  .join(Score, Score.class_id.__eq__(Class.id), isouter=True)\
                  .join(Subject, Subject.id.__eq__(Score.subject_id))
    q = q.filter(Subject.name.contains('Toán'))
    q = q.filter(((Score.score_15_minutes_1+Score.score_15_minutes_2+Score.score_1_period*2+Score.semester_exam_score*3)/7).__ge__(summary))
    # q = q.filter(percentage=func.count((Score.score_15_minutes_1+Score.score_15_minutes_2+Score.score_1_period*2+Score.semester_exam_score*3)/7).__ge__(summary)/func.count(Score.semester_exam_score)*100)


    # if kw:
    #     q = q.filter(Product.name.contains(kw))
    #
    # if from_date:
    #     q = q.filter(Receipt.created_date.__ge__(from_date))
    #
    # if to_date:
    #     q = q.filter(Receipt.created_date.__le__(to_date))

    return q.group_by(Class.class_name).all()


def Score_stats_van(summary=5):
    q = db.session.query(Class.class_name, Class.quantity, func.count(Score.semester_exam_score), func.count(Score.semester_exam_score)/Class.quantity*100)\
                  .join(Score, Score.class_id.__eq__(Class.id), isouter=True)\
                  .join(Subject, Subject.id.__eq__(Score.subject_id))
    q = q.filter(Subject.name.contains('Văn'))
    q = q.filter(((Score.score_15_minutes_1+Score.score_15_minutes_2+Score.score_1_period*2+Score.semester_exam_score*3)/7).__ge__(summary))

    return q.group_by(Class.class_name).all()


def get_user_by_id(user_id):
    return User.query.get(user_id)



