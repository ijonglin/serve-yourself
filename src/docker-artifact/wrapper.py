import os
import json
from flask import Flask

# Demonstrate value injection via env var
FLASK_PORT = os.getenv("FLASK_PORT", default=8081)
print(f"Configuration: FLASK_PORT = {FLASK_PORT}")

# Demonstrate configuration via docker filesystem
def read_json(json_filename):
    print(f"Reading in json from file {json_filename}")
    with open(json_filename, "r") as fin:
        return json.loads(fin.read())

# Pulls a configuration dictionary from the docker filesystem
CONFIG_DATA = read_json("config.json")
print(f"Configuration:\n{json.dumps(CONFIG_DATA, indent=4)}")

app = Flask(__name__)
@app.route('/')
def index():
    if "index_payload" in CONFIG_DATA:
        return CONFIG_DATA["index_payload"]
    else:
        return 'Default content: Web App with Python Flask!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FLASK_PORT)
