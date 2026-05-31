from flask import Flask, request, jsonify
from flask_cors import CORS
from kafka import KafkaProducer
import json, time

app = Flask(__name__)
CORS(app)

producer = KafkaProducer(
    bootstrap_servers="localhost:9093",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@app.route("/track", methods=["POST"])
def track():
    data = request.get_json()
    data["server_timestamp"] = time.time()
    producer.send("clickstream", value=data)
    print(f"[KAFKA] {data['event_type']} sur '{data['element']}'")
    return jsonify({"status": "ok"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)