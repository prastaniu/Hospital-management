from flask import Blueprint, request, jsonify
from extensions import mysql 

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/billing', methods=['GET'])
def get_bills():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM billing")
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    cur.close()
    return jsonify([dict(zip(column_names, row)) for row in rows])

@billing_bp.route('/billing/<bill_id>', methods=['GET'])
def get_bill(bill_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM billing WHERE bill_id = %s", (bill_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        column_names = ['bill_id', 'patient_id', 'treatment_id', 'bill_date', 'amount', 'payment_method', 'payment_status']
        return jsonify(dict(zip(column_names, row)))
    return jsonify({'message': 'Bill not found'}), 404

@billing_bp.route('/billing', methods=['POST'])
def add_bill():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO billing (bill_id, patient_id, treatment_id, bill_date, amount, payment_method, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['bill_id'], data['patient_id'], data['treatment_id'],
            data['bill_date'], data['amount'], data['payment_method'], data['payment_status']
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Bill added successfully'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500

@billing_bp.route('/billing/<bill_id>', methods=['PUT'])
def update_bill(bill_id):
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE billing SET patient_id=%s, treatment_id=%s, bill_date=%s, amount=%s, payment_method=%s, payment_status=%s
            WHERE bill_id=%s
        """, (
            data['patient_id'], data['treatment_id'], data['bill_date'],
            data['amount'], data['payment_method'], data['payment_status'], bill_id
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Bill updated successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500

@billing_bp.route('/billing/<bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM billing WHERE bill_id = %s", (bill_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Bill deleted successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': str(e)}), 500
