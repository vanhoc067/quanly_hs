from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime,  ForeignKey, Enum
from quanly_hs import db
from flask_login import UserMixin
from enum import Enum as UserEnum
from datetime import datetime
from sqlalchemy.orm import relationship


class baseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    admin = 1
    user = 2


class User(baseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), default='images/default.png')
    user_role = Column(Enum(UserRole), default=UserRole.user)
    student_user = relationship('Student', backref='user', uselist=False, lazy=True)

    def __str__(self):
        return self.name


class Class(baseModel):
    __tablename__ = 'class'
    class_name = Column(String(20), nullable=False)
    grade = Column(Enum('10','11','12'), nullable=False)
    quantity = Column(Integer, nullable=False)
    students = relationship('Student', backref='class', lazy=True)
    score_class = relationship('Score', backref='class', lazy=True)

    def __str__(self):
        return self.class_name


class Student(baseModel):
    __tablename__ = 'student'
    name = Column(String(50), nullable=False)
    gender = Column(Enum('Nam','Nu'), nullable=False)
    date_of_birth = Column(DateTime)
    address = Column(String(50), nullable=False)
    phone = Column(Integer)
    email = Column(String(50))
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    # score_detail = relationship('Score_detail', secondary='score_detail', backref=('student'), lazy=True)
    score_student = relationship('Score', backref='student', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id))

    def __str__(self):
        return self.name


class Subject(baseModel):
    name = Column(String(20), nullable=False)
    score_subject = relationship('Score', backref='subject', lazy=True)

    def __str__(self):
        return self.name


class Score(db.Model):
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False, primary_key=True)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False, primary_key=True)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False, primary_key=True)
    semester = Column(Enum('Hoc ki I', 'Hoc ki II'), nullable=False)
    school_year = Column(DateTime, default=datetime.now())
    score_15_minutes_1 = Column(Float, nullable=False)
    score_15_minutes_2 = Column(Float, nullable=False)
    score_1_period = Column(Float, nullable=False)
    semester_exam_score = Column(Float, nullable=False)
    # detail = relationship('ScoreDetail', lazy='subquery', backref=backref('score', lazy=True))

    def __str__(self):
        return self.student.name

# class ScoreDetail(db.Model):
#     id = Column(Integer, ForeignKey(Score.class_id), nullable=False, primary_key=True)
#     # score_subject_id = Column(Integer, ForeignKey(Score.subject_id), nullable=False, primary_key=True)
#     # student_id = Column(Integer, ForeignKey(Student.id), nullable=False, primary_key=True)
#     score_15_minutes_1 = Column(Float, nullable=False)
#     score_15_minutes_2 = Column(Float, nullable=False)
#     score_1_period = Column(Float, nullable=False)
#     semester_exam_score = Column(Float, nullable=False)
#     # score_detail = relationship(Score, lazy='score_detail', backref=backref('score', lazy=True))
# #
# #

if __name__ == '__main__':
    db.create_all()