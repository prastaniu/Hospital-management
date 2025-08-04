from flask import Blueprint, request, jsonify
from extensions import mysql

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
def get_patients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    cur.close()
    patients = [dict(zip(column_names, row)) for row in rows]
    return jsonify(patients)

@patients_bp.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        column_names = ['patient_id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'contact_number', 'address', 'registration_date', 'insurance_provider', 'insurance_number', 'email']
        return jsonify(dict(zip(column_names, row)))
    else:
        return jsonify({'message': 'Patient not found'}), 404

@patients_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO patients (patient_id, first_name, last_name, gender, date_of_birth, contact_number, address, registration_date, insurance_provider, insurance_number, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['patient_id'],
            data['first_name'],
            data['last_name'],
            data['gender'],
            data['date_of_birth'],
            data['contact_number'],
            data['address'],
            data['registration_date'],
            data['insurance_provider'],
            data['insurance_number'],
            data['email']
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Patient added successfully'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error: ' + str(e)}), 500

@patients_bp.route('/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE patients
            SET first_name = %s,
                last_name = %s,
                gender = %s,
                date_of_birth = %s,
                contact_number = %s,
                address = %s,
                registration_date = %s,
                insurance_provider = %s,
                insurance_number = %s,
                email = %s
            WHERE patient_id = %s
        """, (
            data['first_name'],
            data['last_name'],
            data['gender'],
            data['date_of_birth'],
            data['contact_number'],
            data['address'],
            data['registration_date'],
            data['insurance_provider'],
            data['insurance_number'],
            data['email'],
            patient_id
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Patient updated successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error: ' + str(e)}), 500

@patients_bp.route('/patients/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Patient deleted successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': 'Error: ' + str(e)}), 500
