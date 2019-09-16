import time
import json
import numpy
import base64
import cv2

from flask import Flask, Response, request
from view.black_box import BlackBox

from utils import constants as C
from utils.app_log import get_logger

application = Flask(__name__)
logger = get_logger("application")

blackbox = BlackBox()

def dump_json(passed_json):
    return json.dumps(passed_json, indent=4, sort_keys=True, default=str)

def return_failed_response():
    return Response(dump_json({}), status=C.STATUS_ERROR, mimetype='application/json')


@application.route("/", methods = ["GET", "POST"])
def check_everthing_is_ok():
    return Response(dump_json({"hello": "At this moment, everthing is working fine"}),
                    status=C.STATUS_OK, mimetype='application/json')

@application.route("/api/human_detection", methods = ["GET"])
def check_everthing_is_ok_2():
    return Response(dump_json({"error": "Make POST requests"}),
                    status=C.STATUS_OK, mimetype='application/json')

@application.route("/api/human_detection", methods = ["POST"])
def run_the_human_detector():
    #try:
    camera_id = request.form.get("camera_id")
    image = request.form.get("image")
    task_id = request.form.get("task_id")

    x1 = int(request.form.get("x1"))
    x2 = int(request.form.get("x2"))
    y1 = int(request.form.get("y1"))
    y2 = int(request.form.get("y2"))

    height = int(request.form.get("height"))
    width = int(request.form.get("width"))
    layers = int(request.form.get("layers"))

    points = (x1, y1, x2, y2)
    image_shape = (height, width, layers)

    image = numpy.frombuffer(base64.b64decode(image), dtype=numpy.uint8)
    image = image.reshape(image_shape)

    print(f"[APP] Received: camera_id: {camera_id} && task_id: {task_id}")

    response_json = {
        "camera_id": camera_id,
        "task_id": task_id,
    }

    #print(response_json)
    response_in_json = blackbox.receiveFrame(image, points)
    response_json.update(response_in_json)

    return Response(dump_json(response_json), status=C.STATUS_OK, mimetype='application/json')

    #except Exception as ex:
    #    logger.error(f"[APP] Error has occured. Exception: {ex}")
    #    return return_failed_response()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=7000, debug=True)
