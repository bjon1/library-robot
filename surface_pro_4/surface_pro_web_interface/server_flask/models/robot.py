from flask import Blueprint, jsonify, request
import socket
import struct

States = {
    "CRUISE": 1,
    "FORWARD": 2,
    "REVERSE": 3,
    "TURNING_LEFT": 4,
    "TURNING_RIGHT": 5,
    "CLOCKWISE": 6,
    "COUNTER_CLOCKWISE": 7,
    "STOP": 8,
}

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

import time

def connect_to_server(host, port, attempts=5, delay=5):
    for attempt in range(attempts):
        try:
            # Try to connect to the server
            s.connect((host, port))
            print("Connected to server")
            return
        except socket.error as e:
            print(f"Attempt {attempt+1} failed. Error: {e}")
            time.sleep(delay) 
    print("All attempts failed. Could not connect to server.")

def close_connection():
    s.close()

def send_data(data):
    data_bytes = struct.pack('B', data)
    print("SENDING", data_bytes)
    s.send(data_bytes)

bp = Blueprint('robot', __name__)

@bp.route('/move-forward', methods=['POST'])
def move_forward():
    try:
        send_data(States["CRUISE"])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@bp.route('/move-backward', methods=['POST'])
def move_backward():  
    try:
        send_data(States["REVERSE"])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@bp.route('/turn-left', methods=['POST'])
def turn_left():
    try:
        send_data(States["TURNING_LEFT"])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@bp.route('/turn-right', methods=['POST'])
def turn_right():
    try:
        send_data(States["TURNING_RIGHT"])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@bp.route('/stop-robot', methods=['POST'])
def stop():
    try:
        send_data(States["STOP"])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@bp.route('/turn-clockwise', methods=['POST'])
def turn_clockwise():
    try:
        send_data(States["CLOCKWISE"])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@bp.route('/turn-counter-clockwise', methods=['POST'])
def turn_counter_clockwise():
    try:
        send_data(States["COUNTER_CLOCKWISE"])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@bp.route('/set-speed', methods=['POST'])
def set_speed():
    try:
        data = request.get_json()
        speed = data.get('speed')
        speed = max(0, min(100, int(speed)))
        send_data(speed)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

connect_to_server('137.140.212.230', 50000)