from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

@app.route('/transactions/status', methods=['GET'])
def status():
    return jsonify(last_run='2025-06-02T00:00:00Z')

@app.route('/transactions/process', methods=['POST'])
def process_transactions():
    return jsonify(status='completed')

@app.route('/transactions/download/<filename>', methods=['GET'])
def download_file(filename):
    path = os.path.join('output', filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify(error='File not found'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
