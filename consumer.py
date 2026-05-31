import json
from kafka import KafkaConsumer
from sqlalchemy import create_engine, text

KAFKA_TOPIC = "clickstream"
KAFKA_SERVER = "localhost:9093"

engine = create_engine("postgresql://admin:admin123@localhost:5433/streaming_db")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="clickstream-group",
    consumer_timeout_ms=-1
)

print("Consumer démarré — en attente de clics...")
count = 0

for message in consumer:
    event = message.value
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO clicks (page, element, event_type, x_pos, y_pos, user_agent)
                VALUES (:page, :element, :event_type, :x_pos, :y_pos, :user_agent)
            """), {
                "page": event.get("page", ""),
                "element": event.get("element", ""),
                "event_type": event.get("event_type", ""),
                "x_pos": event.get("x_pos", 0),
                "y_pos": event.get("y_pos", 0),
                "user_agent": event.get("user_agent", "")
            })
            conn.commit()
        count += 1
        print(f"[#{count}] {event['event_type']} — {event['element']}")
    except Exception as e:
        print(f"Erreur DB : {e}")