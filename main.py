from flask import Flask, request, jsonify
import os
import json
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Serverless! 🚀\n", 200, {'Content-Type': 'text/plain'}

@app.route('/echo', methods=['POST'])
def echo():
    try:
        data = request.get_json(silent=True)
    except BadRequest:
        data = None

    if data is None:
        raw = request.get_data(as_text=True)
        if raw:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid JSON in request body", "raw": raw}), 400
        else:
            return jsonify({"error": "No JSON body sent"}), 400

    return jsonify({
        "status": "received",
        "you_sent": data,
        "length": len(str(data))
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
