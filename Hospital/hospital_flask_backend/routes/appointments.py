from flask import Blueprint, request, jsonify
from extensions import mysql 

appointments_bp = Blueprint('appointments', __name__)

from datetime import date, time, timedelta

@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM appointments")
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    cur.close()

    appointments = []
    for row in rows:
        appt = dict(zip(column_names, row))
        # Convert non-JSON-serializable types
        for key, value in appt.items():
            if isinstance(value, (date, time, timedelta)):
                appt[key] = str(value)
        appointments.append(appt)

    return jsonify(appointments)


@appointments_bp.route('/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        column_names = ['appointment_id', 'patient_id', 'doctor_id', 'appointment_date',
                        'appointment_time', 'reason_for_visit', 'status']
        appt = dict(zip(column_names, row))
        # Convert if needed
        for key, value in appt.items():
            if isinstance(value, (date, time, timedelta)):
                appt[key] = str(value)
        return jsonify(appt)

    return jsonify({'message': 'Appointment not found'}), 404


@appointments_bp.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['appointment_id'], data['patient_id'], data['doctor_id'], data['appointment_date'],
            data['appointment_time'], data['reason_for_visit'], data['status']
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Appointment added successfully'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500

@appointments_bp.route('/appointments/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE appointments SET patient_id=%s, doctor_id=%s, appointment_date=%s,
            appointment_time=%s, reason_for_visit=%s, status=%s WHERE appointment_id=%s
        """, (
            data['patient_id'], data['doctor_id'], data['appointment_date'],
            data['appointment_time'], data['reason_for_visit'], data['status'], appointment_id
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Appointment updated successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500

@appointments_bp.route('/appointments/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM appointments WHERE appointment_id = %s", (appointment_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Appointment deleted successfully'})
    except Exception as e:
        mysql.connection.rollback()
        if "foreign key constraint fails" in str(e).lower():
            return jsonify({'message': 'Cannot delete appointment with associated treatments.'}), 400
        return jsonify({'message': str(e)}), 500

