from view.human_detection import DetectorAPI
import time
import json
import cv2
from shapely.geometry import Polygon, LineString

# from utils import constants as C
# from utils.app_log import get_logger

# logger = get_logger("BlackBox")

def check_intersections(X1, X2, mainLine):
    (x1, y1) = X1
    (x2, y2) = X2

    polygon = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    mainLine = LineString(mainLine)

    return mainLine.intersects(polygon)

class BlackBox:

    def __init__(self):
        model_path = './view/model/frozen_inference_graph.pb'
        self.odapi = DetectorAPI(path_to_ckpt=model_path)
        self.human_threshold = 0.9
        self.previous_error = 10
        self.alert_delay = 5.0
        self.last_time_sent = 0
        
    # humans(id, x_min, x_max, time then detected, alerted, countdown for save in memory)
    def analyseFrame(self, frame, mainLine):
        # try:

        # cv2.imwrite("/home/user/Desktop/human_detection_analysis/test/out.jpg", frame)

        mainLine = ((mainLine[0], mainLine[1]), (mainLine[2], mainLine[3]))
        curr_time = time.time()
        is_alert = False
        humans = []
        data = {}
        
        boxes, scores, classes, num = self.odapi.processFrame(frame)

        for i in range(len(boxes)):
            box = boxes[i]

            if classes[i] == 1 and scores[i] > self.human_threshold:
                x_min = (box[1], box[0])
                x_max = (box[3], box[2])
                
                if check_intersections(x_min, x_max, mainLine):
                    is_alert = True
                
                human = {}
                human['id'] = i
                human['x1'], human['y1'] = x_min
                human['x2'], human['y2'] = x_max
                human['class'] = classes[i]
                humans.append(human)

                # need to write saving to REDIS
                # humans.append((i, x_min, x_max, classes[i], curr_time, False, self.previous_error))

        data['is_alert'] = is_alert
        data['boxes'] = humans
        #json_out = json.dumps(data)

        return data

        # except Exception as ex:
        #     logger.error(f"[APP] Error has occured. Exception: {ex}")
            # return return_failed_response()

    def receiveFrame(self, frame, mainLine):
        # logger.info(f"[APP] Received: frame with main line: {mainLine}")
        return self.analyseFrame(frame, mainLine)

if __name__ == "__main__":
    import pprint
    bb = BlackBox()

    img = cv2.imread("1.jpg")
    mainLine = (30, 327, 940, 344)

    response_in_json = bb.receiveFrame(img, mainLine)
    pprint.pprint(response_in_json)
