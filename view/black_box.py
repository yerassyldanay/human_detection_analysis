from human_detection import DetectorAPI
import time
import json
import cv2
from shapely.geometry import Polygon, LineString
import redis

# from utils import constants as C
# from utils.app_log import get_logger

# logger = get_logger("BlackBox")

def line_intersection(X1, X2, mainLine):
    (x1, y1) = X1
    (x2, y2) = X2

    polygon = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    mainLine = LineString(mainLine)
    return mainLine.intersects(polygon)
    
def box_intersection(X1, X2, X3, X4):
    (x1, y1) = X1
    (x2, y2) = X2
    polygon1 = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    
    (x3, y3) = X3
    (x4, y4) = X4
    polygon2 = Polygon([(x3, y3), (x4, y3), (x4, y3), (x3, y4)])

    return polygon2.intersection(polygon1).area

class BlackBox:

    def __init__(self):
        model_path = './model/frozen_inference_graph.pb'
        self.odapi = DetectorAPI(path_to_ckpt=model_path)
        self.redis_cli = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.human_threshold = 0.9
        self.previous_error = 10
        self.alert_delay = 5.0
        self.last_time_sent = 0

    def getData(self, frame):
        boxes = []
        scores = []
        classes = []
        raw_boxes, raw_scores, raw_classes, num = self.odapi.processFrame(frame)

        for i in range(len(raw_boxes)):
            if raw_classes[i] == 1 and raw_scores[i] > self.human_threshold:
                boxes.append(raw_boxes[i])
                scores.append(raw_scores[i])
                classes.append(raw_classes[i])

        return boxes, scores, classes, len(boxes) 

        
    # humans(id, x_min, x_max, time then detected, alerted, countdown for save in memory)
    def analyseFrame(self, frame, mainLine, humans):        
        curr_time = time.time()
        is_alert = False
        top_num = 0
        found_humans = []
        
        boxes, scores, classes, box_count = self.getData(frame)
        used = [0] * box_count
        
        for human in humans:
            maxx = (0, 0, 0, -1)

            for i in range(box_count):
                if used[i] == 0:
                    box = boxes[i]

                    x_min = (box[1], box[0])
                    x_max = (box[3], box[2])
                    area = box_intersection(human[1], human[2], x_min, x_max)
                    if area > maxx[0]:
                        maxx = area, x_min, x_max, i
                    
            if maxx[3] >= 0:
                found_humans.append((human[0], maxx[1], maxx[2], human[3], human[4], self.previous_error))
                used[maxx[3]] = 1
                
                top_num = max(top_num, human[0])

            else:
                if human[5] > 0:
                    found_humans.append((human[0], human[1], human[2], human[3], human[4], human[5] - 1))

        for i in range(box_count):
            # Class 1 represents human
            box = boxes[i]

            if used[i] == 0:
                x_min = (box[1], box[0])
                x_max = (box[3], box[2])
                found_humans.append((top_num, x_min, x_max, curr_time, False, self.previous_error))
                top_num += 1
                print("New Human!")

        humans = []
        for found_human in found_humans:
            if found_human[5] == self.previous_error:
                if line_intersection(found_human[1], found_human[2], mainLine):
                    is_alert = True
                
                human = {}
                human['id'] = found_human[0]
                human['x1'], human['y1'] = found_human[1]
                human['x2'], human['y2'] = found_human[2]
                human['class'] = classes[i]
                humans.append(human)

        # print(found_humans)
        # print(human)

        return is_alert, humans, found_humans

    def receiveFrame(self, cam_id, frame, mainLine):
        mainLine = ((mainLine[0], mainLine[1]), (mainLine[2], mainLine[3]))
        humans = []

        old_humans = self.redis_cli.get(cam_id)
        if old_humans:
            humans = json.loads(old_humans.decode('utf-8'))
        # print(humans)
        
        is_alert, humans, all_h = self.analyseFrame(frame, mainLine, humans)

        json_out = json.dumps(all_h)
        self.redis_cli.set(cam_id, json_out)

        data = {}
        data['is_alert'] = is_alert
        data['boxes'] = humans

        return data

if __name__ == "__main__":
    bb = BlackBox()

    with open('config.json') as f:
        config = json.load(f)
    colors = config["color_sources"]

    # img = cv2.imread("/home/user/Desktop/human_detection_analysis/test/images/1.jpg")
    # mainLine = (30, 327, 940, 344)

    # response_in_json = bb.receiveFrame(1, img, mainLine)
    # print(response_in_json)

    cap = cv2.VideoCapture('/home/user/Documents/iGuard/datasets/videos/output1565692867.avi')
    mainLine = (30, 653, 1879, 687)
    frame_num = 0
    while True:
        
        r, img = cap.read()

        frame_num += 1
        if(frame_num % 10 != 0) or frame_num < 1:
            continue

        response_in_json = bb.receiveFrame(1, img, mainLine)

        # Visualization of the results of a detection.

        for box in response_in_json['boxes']:
            cv2.rectangle(img,(box['x1'],box['y1']), (box['x2'],box['y2']), colors[box['id'] % len(colors)],2)
            
        img = cv2.resize(img, (1280, 720))
        cv2.imshow("preview", img)
        key = cv2.waitKey(1)
