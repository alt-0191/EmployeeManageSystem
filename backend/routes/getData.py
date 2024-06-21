from flask import Flask, jsonify, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import Config
from backend.models import Employee, PerformanceEvaluations, SatisfactionSurveys, CompensationsBenefits, User

app = Flask(__name__)
getdata = Blueprint('getdata', __name__)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)


def employees_structure_to_dict(employee):
    if not employee:
        return {}

    return {
        "所属部门": employee.department_name if employee.department_name else "未分配部门",
        "职位": employee.position_name if employee.position_name else "没有职位",
        "员工姓名": employee.name
    }


def employees_manage_to_dict(employee):
    return {
        'id': employee.id,
        'name': employee.name,
        'age': employee.age,
        'gender': employee.gender,
        'is_resigned': employee.is_resigned,
        'resignation_date': employee.resignation_date.isoformat() if employee.resignation_date else None,
        'department': employee.department_name if employee.department_name else None,
        'position': employee.position_name if employee.position_name else None
    }


def user_structure_to_dict(user):
    if not user:
        return {}

    return {
        "用户名": user.username if user.username else "没有用户名",
        "管理员权限": user.is_admin
    }


def user_manage_to_dict(user):
    return {
        'username': user.username,
        'is_admin': user.is_admin,
    }


@getdata.route('/data/employeeStatus')
def employee_status():
    total_employees = Employee.query.count()
    resigned_employees = Employee.query.filter(Employee.is_resigned == True).count()
    active_employees = total_employees - resigned_employees
    if total_employees > 0:
        resign_rate = (resigned_employees / total_employees) * 100
    else:
        resign_rate = 0

    return jsonify({
        'total': total_employees,
        'active': active_employees,
        'resigned': resigned_employees,
        'resign_rate': resign_rate
    })


@getdata.route('/data/employeeStructure')
def employee_structure():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        employees = session.query(Employee).all()
        employee_dicts = [employees_structure_to_dict(employee) for employee in employees]

        return jsonify(employee_dicts)
    finally:
        session.close()


@getdata.route('/data/employeeManage')
def employee_manage():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        employees = session.query(Employee).all()
        employee_dicts = [employees_manage_to_dict(employee) for employee in employees]

        return jsonify(employee_dicts)
    finally:
        session.close()


@getdata.route('/data/userManage')
def user_manage():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        users = session.query(User).all()
        user_dicts = [user_manage_to_dict(user) for user in users]
        return jsonify(user_dicts)
    finally:
        session.close()


@getdata.route('/api/performances')
def get_performances():
    performances = PerformanceEvaluations.query.join(Employee).add_columns(
        Employee.name, Employee.department_name, PerformanceEvaluations.score
    ).all()

    data = []
    for performance in performances:
        data.append({
            "employee_id": performance.PerformanceEvaluations.employee_id,
            "name": performance.name,
            "department": performance.department_name,
            "score": performance.PerformanceEvaluations.score
        })

    return jsonify(data)


@getdata.route('/api/satisfaction')
def get_satisfaction():
    surveys = SatisfactionSurveys.query.all()
    data = {
        "very_satisfied": 0,
        "satisfied": 0,
        "neutral": 0,
        "dissatisfied": 0,
        "very_dissatisfied": 0
    }

    for survey in surveys:
        if survey.satisfaction_score >= 9:
            data["very_satisfied"] += 1
        elif survey.satisfaction_score >= 7:
            data["satisfied"] += 1
        elif survey.satisfaction_score >= 5:
            data["neutral"] += 1
        elif survey.satisfaction_score >= 3:
            data["dissatisfied"] += 1
        elif survey.satisfaction_score >= 1:
            data["very_dissatisfied"] += 1

    return jsonify(data)


@getdata.route('/api/compensations')
def get_compensations():
    compensations = CompensationsBenefits.query.join(Employee).all()
    data = [{
        "name": comp.employee.name,
        "salary": float(comp.salary),
        "benefits": float(comp.benefits)
    } for comp in compensations]
    return jsonify(data)
