from flask import Flask, jsonify, request
from redact import redact_json
from werkzeug.exceptions import BadRequest

app = Flask(__name__)


@app.route("/redact", methods=["POST"])
def redact():
    try:
        data = request.get_json(force=True)
        redacted = redact_json(data)
        redacted["redacted"] = True
    except BadRequest:
        return jsonify({"error": "Invalid JSON data."})
    except Exception as ex:
        return jsonify({"error": f"Unknown error occurred: {ex}"})
    return jsonify(redacted)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
