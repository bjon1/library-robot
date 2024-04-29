from threading import Thread
from flask import Blueprint, Flask, render_template, Response
from flask_socketio import SocketIO
from models.AI import ObjectDetection

bp = Blueprint('ai', __name__)

# This is the AICommunicator class that is used to communicate with the AI model.
# It needs to be implemented with TCP/IP communication.

def generate():
    detector = ObjectDetection(capture_index=0)
    while True:
        frame_data = detector()
        yield frame_data

@bp.route('/stream')
def stream():
    return Response(generate(), content_type='application/json')

