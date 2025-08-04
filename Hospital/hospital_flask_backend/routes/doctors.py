from flask import Blueprint, request, jsonify
from extensions import mysql 

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/doctors', methods=['GET'])
def get_doctors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    cur.close()
    doctors = [dict(zip(column_names, row)) for row in rows]
    return jsonify(doctors)

@doctors_bp.route('/doctors/<doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        column_names = ['doctor_id', 'first_name', 'last_name', 'specialization', 'phone_number', 'years_experience', 'hospital_branch', 'email']
        return jsonify(dict(zip(column_names, row)))
    else:
        return jsonify({'message': 'Doctor not found'}), 404

@doctors_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO doctors (doctor_id, first_name, last_name, specialization, phone_number, years_experience, hospital_branch, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['doctor_id'],
            data['first_name'],
            data['last_name'],
            data['specialization'],
            data['phone_number'],
            data['years_experience'],
            data['hospital_branch'],
            data['email']
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Doctor added successfully'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error: ' + str(e)}), 500

@doctors_bp.route('/doctors/<doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE doctors
            SET first_name = %s,
                last_name = %s,
                specialization = %s,
                phone_number = %s,
                years_experience = %s,
                hospital_branch = %s,
                email = %s
            WHERE doctor_id = %s
        """, (
            data['first_name'],
            data['last_name'],
            data['specialization'],
            data['phone_number'],
            data['years_experience'],
            data['hospital_branch'],
            data['email'],
            doctor_id
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Doctor updated successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error: ' + str(e)}), 500

@doctors_bp.route('/doctors/<doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Doctor deleted successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error: ' + str(e)}), 500
