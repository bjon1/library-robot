from threading import Thread
import os
from flask import Flask, send_from_directory, Response, jsonify
from flask_cors import CORS
from models.AI import ObjectDetection

app = Flask(__name__, static_folder='../client/dist')
CORS(app, resources={r"/api/*": {"origins": "*"}}, methods='GET,POST,PUT,DELETE,PATCH', supports_credentials=True)

# Add Controllers
from models import robot
app.register_blueprint(robot.bp, url_prefix='/api/robot')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Serve static files
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_server_error(e):
    response = {
        "status": 500,
        "message": "Internal Server Error",
        "isSuccess": False
    }
    return jsonify(response), 500

def generate():
    detector = ObjectDetection(capture_index=0)
    while True:
        frame_data = detector()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_data['frame'] + b'\r\n')

@app.route('/stream')
def stream():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
