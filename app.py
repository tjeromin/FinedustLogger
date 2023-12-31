from flask import Flask, request, json
import requests
from datetime import datetime
import os
import dotenv
import threading
import sys

app = Flask(__name__)

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
URL = os.getenv("URL")
PATH = os.getenv("NC_PATH")
AUTH = (os.getenv("NC_USERNAME"), os.getenv("PASSWORD"))
ENCODING = "utf-8"
FILENAME_FORMAT = "%Y-%m"

print("python interpreter used: " + sys.executable)


@app.route("/api/log/finedust", methods=["PUT"])
def log_finedust():
    args = request.args
    pm25 = args.get("pm25")
    pm10 = args.get("pm10")

    if pm25 is None or pm10 is None:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    t = threading.Thread(target=update_files, args=(pm25, pm10))
    t.start()

    return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}


def update_files(pm25, pm10):
    filepath = PATH + str(datetime.now().strftime(FILENAME_FORMAT)) + "-Feinstaub"
    content = download(filepath + ".csv")
    if content != "":
        content += "\r\n"
    content += ",".join([datetime.now().isoformat(), pm25, pm10])

    upload(content, filepath + ".csv")
    upload(content, filepath + ".txt")


@app.route("/test", methods=["GET"])
def test():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def download(path):
    response = requests.get("/".join([URL, path]), auth=AUTH)

    if response.status_code == 404:
        return ""

    return response.content.decode(ENCODING)


def upload(content, path):
    response = requests.put("/".join([URL, path]), auth=AUTH, data=content)
    print("upload: " + str(response.status_code))


if __name__ == '__main__':
    app.run()
