from flask import Flask, request
import hazelcast
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
config = hazelcast.config.Config()
config.network.set_port_auto_increment(True)
config.network.join.tcp_ip.enabled = True
config.network.join.tcp_ip.members = ["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
hz = hazelcast.HazelcastInstance(config)
logs = hz.get_map("logs").blocking()

@app.route('/log', methods=['POST'])
def log_message():
    data = request.json
    msg_id = data["id"]
    if msg_id in logs:
        return "Duplicate message ignored\n", 200
    logs.put(msg_id, data['msg'])
    print(f"Logged: {data['msg']}")
    return "Logged", 200

@app.route('/logs', methods=['GET'])
def get_logs():
    all_logs = logs.entry_set()
    return " ".join(all_logs.values())

if __name__ == '__main__':
    app.run(port=5001, debug=True)
