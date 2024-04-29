from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os

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

if __name__ == "__main__":
    app.run(port=5000)