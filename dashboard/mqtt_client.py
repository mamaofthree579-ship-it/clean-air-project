dashboard/mqtt_client.py
import threading
import json
import time
import os
import queue
import paho.mqtt.client as mqtt

# Public queue other modules can import
mqtt_queue = queue.Queue()

class MQTTThread(threading.Thread):
    def __init__(self, broker, port, topic, client_id="clean-air-dashboard"):
        super().__init__(daemon=True)
        self.broker = broker
        self.port = int(port)
        self.topic = topic
        self.client_id = client_id
        self._stop = threading.Event()
        self._client = mqtt.Client(client_id=self.client_id)
        # optional: set username/password via env
        mqtt_user = os.getenv("MQTT_USER")
        mqtt_pass = os.getenv("MQTT_PASS")
        if mqtt_user and mqtt_pass:
            self._client.username_pw_set(mqtt_user, mqtt_pass)

        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(self.topic)
            # push status message
            mqtt_queue.put({"__meta__": "connected", "topic": self.topic})
        else:
            mqtt_queue.put({"__meta__": "connect_failed", "rc": rc})

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode("utf-8")
            # try parse JSON; if not, create a simple record
            try:
                obj = json.loads(payload)
            except Exception:
                # payload might be a simple CSV or key=value pairs
                obj = {"raw": payload}
            obj["_topic"] = msg.topic
            mqtt_queue.put(obj)
        except Exception as e:
            mqtt_queue.put({"__meta__": "msg_error", "error": str(e)})

    def stop(self):
        self._stop.set()
        try:
            self._client.disconnect()
        except Exception:
            pass

    def run(self):
        try:
            self._client.connect(self.broker, self.port, keepalive=60)
            self._client.loop_start()
            while not self._stop.is_set():
                time.sleep(0.5)
            self._client.loop_stop()
        except Exception as e:
            mqtt_queue.put({"__meta__": "thread_error", "error": str(e)})

