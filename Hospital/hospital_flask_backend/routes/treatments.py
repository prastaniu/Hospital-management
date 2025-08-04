from flask import Blueprint, request, jsonify
from extensions import mysql
from datetime import date, time, timedelta  # Needed for JSON serialization

treatments_bp = Blueprint('treatments', __name__)

@treatments_bp.route('/treatments', methods=['GET'])
def get_treatments():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM treatments")
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()

        treatments = []
        for row in rows:
            treatment = dict(zip(column_names, row))
            # Convert dates if needed
            for k, v in treatment.items():
                if isinstance(v, (date, time, timedelta)):
                    treatment[k] = str(v)
            treatments.append(treatment)

        return jsonify(treatments)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@treatments_bp.route('/treatments/<treatment_id>', methods=['GET'])
def get_treatment(treatment_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM treatments WHERE treatment_id = %s", (treatment_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        column_names = ['treatment_id', 'appointment_id', 'treatment_type', 'description', 'cost', 'treatment_date']
        treatment = dict(zip(column_names, row))
        for k, v in treatment.items():
            if isinstance(v, (date, time, timedelta)):
                treatment[k] = str(v)
        return jsonify(treatment)
    return jsonify({'message': 'Treatment not found'}), 404


@treatments_bp.route('/treatments', methods=['POST'])
def add_treatment():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO treatments (treatment_id, appointment_id, treatment_type, description, cost, treatment_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['treatment_id'], data['appointment_id'], data['treatment_type'],
            data['description'], data['cost'], data['treatment_date']
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Treatment added successfully'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500


@treatments_bp.route('/treatments/<treatment_id>', methods=['PUT'])
def update_treatment(treatment_id):
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE treatments SET appointment_id=%s, treatment_type=%s, description=%s, cost=%s, treatment_date=%s
            WHERE treatment_id=%s
        """, (
            data['appointment_id'], data['treatment_type'], data['description'],
            data['cost'], data['treatment_date'], treatment_id
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Treatment updated successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500


@treatments_bp.route('/treatments/<treatment_id>', methods=['DELETE'])
def delete_treatment(treatment_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM treatments WHERE treatment_id = %s", (treatment_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Treatment deleted successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500
