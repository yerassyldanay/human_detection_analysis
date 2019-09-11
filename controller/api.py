import time
import json
from flask import Flask, Response, request

from utils import constants as C
from utils.app_log import get_logger

application = Flask(__name__)
logger = get_logger("application")

def dump_json(passed_json):
    return json.dumps(passed_json, indent=4, sort_keys=True, default=str)

def return_failed_response():
    return Response(dump_json({}), status=C.STATUS_ERROR, mimetype='application/json')

@application.route("/", methods = ["GET", "POST"])
def check_everthing_is_ok():
    return Response(dump_json({"hello": "At this moment, everthing is working fine"}),
                    status=C.STATUS_OK, mimetype='application/json')

@application.route("/api/human_detection", methods = ["POST"])
def run_the_human_detector():
    try:
        camera_id = request.form.get("camera_id")
        image = request.form.get("image")
        task_id = request.form.get("task_id")
        points = request.form.get("points")

        logger.info(f"[APP] Received: camera_id: {camera_id} && task_id: {task_id}")

        response_json = {
            "camera_id": camera_id,
            "task_id": task_id,
        }

        """
            run here your method
            response_in_json = your_method(image)
        """

        response_json.update({})

        return Response(dump_json(response_json), status=C.STATUS_OK, mimetype='application/json')

    except Exception as ex:
        logger.error(f"[APP] Error has occured. Exception: {ex}")
        return return_failed_response()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=7000, debug=True)
