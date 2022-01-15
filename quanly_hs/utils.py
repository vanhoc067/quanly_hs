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


def add_student(name, gender, date_of_birth, class_id, address, phone, email):
    student = Student(name=name.strip(),
                gender=gender.strip(),
                date_of_birth=date_of_birth,
                class_id=class_id.strip(),
                address=address,
                phone=phone,
                email=email)

    db.session.add(student)
    db.session.commit()


def load_student(page=1):
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size

    return Student.query.slice(start, start+page_size).all()


def load_class():

    return Class.query.all()



def get_class_by_id(classs_id):
    return Class.query.get(classs_id)


def get_student_by_class_id(classs_id):
    return Student.query.filter(Student.class_id.__eq__(classs_id)).all()


def get_score_by_subject(score_class, score_subject):
    q = db.session.query(Student.id, Student.name, Score.score_15_minutes_1, Score.score_15_minutes_2, Score.score_1_period, Score.semester_exam_score)\
    .join(Student, Score.student_id.__eq__(Student.id), isouter=True)

    q = q.filter(Score.class_id.__eq__(score_class) & Score.subject_id.__eq__(score_subject))
    return q.group_by(Student.id, Student.name, Score.score_15_minutes_1, Score.score_15_minutes_2, Score.score_1_period, Score.semester_exam_score).all()


def count_student():
    return Student.query.count()


def subject_class_score():
    q = db.session.query(Class.class_name, Subject.name, Score.semester, Score.class_id, Score.subject_id, Score.school_year)\
                  .join(Subject, Score.subject_id.__eq__(Subject.id), isouter=True)\
                  .join(Class, Score.class_id.__eq__(Class.id))

    # if kw:
    #     q = q.filter(Product.name.contains(kw))
    #
    # if from_date:
    #     q = q.filter(Receipt.created_date.__ge__(from_date))
    #
    # if to_date:
    #     q = q.filter(Receipt.created_date.__le__(to_date))

    return q.group_by(Class.class_name, Subject.name, Score.semester).all()


# def get_tbVan_hk1(id=None):
#     q = db.session.query()
#     q = q.filter(Score.subject_id.__eq__(11))
#     q = q.filter(Score.semester.__eq__('Hoc ki I'))
#     if id:
#         q = q.filter(Score.student_id.__eq__(id))
#
#     return q.get((Score.score_15_minutes_1+Score.score_15_minutes_2+Score.score_1_period*2+Score.semester_exam_score*3)/7)


def score_student_class():
    q = db.session.query(Score.student_id, Student.name, Class.class_name, (Score.score_15_minutes_1+Score.score_15_minutes_2+Score.score_1_period*2+Score.semester_exam_score*3)/7, 0, Score.school_year)\
                  .join(Student, Score.student_id.__eq__(Student.id), isouter=True)\
                  .join(Class, Score.class_id.__eq__(Class.id))\
                  .join(Subject, Score.subject_id.__eq__(Subject.id))

    q = q.filter(Score.subject_id.__eq__(11) & Score.semester.__eq__('Hoc Ki I'))

    return q.group_by(Score.student_id, Student.name, Class.class_name).all()