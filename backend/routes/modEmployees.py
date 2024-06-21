# employees.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models import db, Employee

modEmployees = Blueprint('employee_bp', __name__)


@modEmployees.route('/api/addEmployees', methods=['POST'])
@jwt_required()
def add_employee():
    data = request.get_json()

    # 字段名到中文的映射
    field_names = {
        'name': '姓名',
        'age': '年龄',
        'gender': '性别',
        'department': '部门',
        'position': '职位'
    }

    # 检查字段是否存在且不为空字符串
    required_fields = ['name', 'age', 'gender', 'department', 'position']
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] == '':
            missing_fields.append(field_names.get(field, field))

    if missing_fields:
        missing_fields_str = ', '.join(missing_fields)
        return jsonify({"message": f"添加失败，缺失或空字段: {missing_fields_str}"}), 400

    try:
        new_employee = Employee(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            department_name=data['department'],
            position_name=data['position'],
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"message": "员工信息已更新", "姓名": new_employee.name}), 201
    except Exception as e:
        return jsonify({"message": f"添加失败，发生错误: {str(e)}"}), 500


@modEmployees.route('/api/updateEmployees/<int:id>', methods=['POST'])
@jwt_required()
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    employee.name = data.get('name', employee.name)
    employee.age = data.get('age', employee.age)
    employee.gender = data.get('gender', employee.gender)
    employee.department_name = data.get('department', employee.department_name)
    employee.position_name = data.get('position', employee.position_name)
    db.session.commit()
    return jsonify({"message": "Employee updated"}), 200


@modEmployees.route('/api/delEmployees/<int:id>', methods=['POST'])
@jwt_required()
def delete_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "员工信息已删除"}), 200
    except Exception as e:
        return jsonify({"message": f"删除失败，发生错误: {str(e)}"}), 500
