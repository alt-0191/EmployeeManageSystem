from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    is_resigned = db.Column(db.Boolean, default=False)
    resignation_date = db.Column(db.Date)
    department_name = db.Column(db.String(100))
    position_name = db.Column(db.String(100))


class PerformanceEvaluations(db.Model):
    __tablename__ = 'performance_evaluations'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    score = db.Column(db.Float)


class SatisfactionSurveys(db.Model):
    __tablename__ = 'satisfaction_surveys'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    satisfaction_score = db.Column(db.Float)
    participation_date = db.Column(db.Date)


class CompensationsBenefits(db.Model):
    __tablename__ = 'compensations_benefits'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    salary = db.Column(db.Numeric(10, 2))
    benefits = db.Column(db.Numeric(10, 2))
    effective_date = db.Column(db.Date)
    employee = db.relationship('Employee', backref='compensations')



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
