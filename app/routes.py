from flask import Blueprint, render_template, request, jsonify, current_app
import psycopg2
import time  # Changed from datetime to time
import os

bp = Blueprint('payment', __name__)

def get_db_connection():
    """Connect to PostgreSQL using app config"""
    config = current_app.config['DB_CONFIG']
    return psycopg2.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        dbname=config['dbname']
    )

@bp.route('/')
def payment_page():
    return render_template('payment.html')

@bp.route('/process-payment', methods=['POST'])
def process_payment():
    data = request.json
    method = data['method']
    amount = float(data['amount'])
    mobile = data['mobile']
    
    # Philippine payment validation
    if not mobile.startswith('09') or len(mobile) != 11:
        return jsonify({
            'status': 'failed',
            'message': 'Invalid Philippine mobile number'
        }), 400
    
    # Initialize variables
    conn = None
    cur = None
    
    try:
        # Connect to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create transaction ID with PH prefix and timestamp
        txn_id = f"PH-TXN-{int(time.time())}"
        created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        # Insert pending transaction
        cur.execute(
            "INSERT INTO transactions (id, payment_method, amount, currency, status, created_at)"
            "VALUES (%s, %s, %s, 'PHP','PENDING', %s)",
            (txn_id, method, amount, created_at)
        )
        conn.commit()
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500
        
    finally:
        # Safely close resources
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    # Simulate payment processing (PH AML check)
    success = amount < 10000
    status = 'COMPLETED' if success else 'FAILED'
    
    return jsonify({
        'status': status,
        'message': 'Payment successful' if success else 'Payment failed: Amount exceeds ₱10,000 limit',
        'txn_id': txn_id
    })