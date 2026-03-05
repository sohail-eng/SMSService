import os
import re
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Firebase Initialization
try:
    cred = credentials.Certificate("google-services.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://testingsms-1735a-default-rtdb.firebaseio.com/'
    })
except Exception as e:
    print(f"Error initializing Firebase: {e}")

def validate_pakistan_number(number):
    """
    Validates Pakistani phone numbers.
    Formats: +923xxXXXXXXX, 923xxXXXXXXX, 03xxXXXXXXX, 3xxXXXXXXX
    """
    # Remove any spaces or dashes
    number = re.sub(r'[\s\-]', '', number)
    
    # Regex for Pakistani mobile numbers
    # Matches: 
    # +923001234567
    # 923001234567
    # 03001234567
    # 3001234567
    pattern = r'^(?:\+92|92|0)?(3\d{9})$'
    match = re.match(pattern, number)
    
    if match:
        # Normalize to 03xxXXXXXXXX format for simplicity or keep as is
        return match.group(1) # returns the 3xxxxxxxxx part
    return None

def push_to_firebase(parent_id, number, text):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S%f")
        ref = db.reference(f"SMS_Service/{parent_id}/{timestamp}")
        ref.set({
            "number": number,
            "text": text
        })
        return True
    except Exception as e:
        print(f"Firebase Push Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-apk')
def download_apk():
    return send_from_directory(directory=os.getcwd(), path='base.apk', as_attachment=True)

@app.route('/send-sms', methods=['POST'])
def send_sms():
    parent_id = request.form.get('unique_key')
    number = request.form.get('phone_number')
    text = request.form.get('message')

    if not parent_id or not number or not text:
        return jsonify({"success": False, "error": "All fields are required"}), 400

    validated_number = validate_pakistan_number(number)
    if not validated_number:
        return jsonify({"success": False, "error": "Invalid Pakistani phone number"}), 400

    # Format the number for the SMS app (usually expects 03... or +92...)
    formatted_number = "0" + validated_number

    if push_to_firebase(parent_id, formatted_number, text):
        return jsonify({"success": True, "message": "SMS request queued successfully!"})
    else:
        return jsonify({"success": False, "error": "Failed to connect to Firebase"}), 500

@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400
        
    parent_id = data.get('unique_key')
    number = data.get('phone_number')
    text = data.get('message')

    if not parent_id or not number or not text:
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    validated_number = validate_pakistan_number(number)
    if not validated_number:
        return jsonify({"success": False, "error": "Invalid Pakistani phone number"}), 400

    formatted_number = "0" + validated_number

    if push_to_firebase(parent_id, formatted_number, text):
        return jsonify({"success": True, "message": "SMS request queued successfully!"})
    else:
        return jsonify({"success": False, "error": "Failed to queue SMS"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
