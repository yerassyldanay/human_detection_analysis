from view.human_detection import DetectorAPI
from shapely.geometry import Polygon, LineString
import time
import json
import redis

def line_intersection(box, main_line):
    (x1, y1, x2, y2) = box

    polygon = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    main_line = LineString(main_line)
    return main_line.intersects(polygon)

def box_intersection(box1, box2):
    (x1, y1, x2, y2) = box1
    polygon1 = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

    (x3, y3, x4, y4) = box2
    polygon2 = Polygon([(x3, y3), (x4, y3), (x4, y3), (x3, y4)])

    return polygon2.intersection(polygon1).area

class BlackBox:

    def __init__(self):
        model_path = './view/model/frozen_inference_graph.pb'
        self.odapi = DetectorAPI(path_to_ckpt=model_path)
        self.redis_cli = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.object_threshold = 0.9
        self.object_classes = [1]
        self.previous_error = 5
        self.alert_delay = 5.0
        self.last_time_sent = 0

    # check frame at faster
    def getData(self, frame):
        boxes = []
        scores = []
        classes = []
        raw_boxes, raw_scores, raw_classes, num = self.odapi.processFrame(frame)

        # choice for boxes with parameters(class, threshold)
        for i in range(len(raw_boxes)):
            if raw_classes[i] in self.object_classes and raw_scores[i] > self.object_threshold:
                boxes.append(raw_boxes[i])
                scores.append(raw_scores[i])
                classes.append(raw_classes[i])

        return boxes, scores, classes, len(boxes)

    # line-crossing and object tracking
    def analyseFrame(self, frame, main_line, objects):        
        curr_time = time.time()
        is_alert = False
        last_id = -1
        found_objects = []

        boxes, scores, classes, box_count = self.getData(frame)
        used = [0] * box_count

        # check for intersections of new boxes with ghosts from previous checks
        for obj in objects:
            maxx = (0, -1)

            # find max intersection
            for i in range(box_count):
                if used[i] == 0 and obj['class'] == classes[i]:
                    box = boxes[i]
                    boundbox = [box[1], box[0], box[3], box[2]]

                    area = box_intersection(obj['box'], boundbox)
                    if area > maxx[0]:
                        maxx = area, i

            # ghost beloved to object
            if maxx[1] >= 0:
                box = boxes[maxx[1]]
                boundbox = [box[1], box[0], box[3], box[2]]
                ghost = obj
                ghost['box'] = boundbox
                ghost['frames_to_live'] = self.previous_error
                found_objects.append(ghost)

                used[maxx[1]] = 1
                last_id = max(last_id, obj['id'])

                if not ghost['is_alerted'] and line_intersection(ghost['box'], main_line):
                    is_alert = True

            # save box as ghost
            else:
                if obj['frames_to_live'] > 0:
                    ghost = obj
                    ghost['frames_to_live'] -= 1
                    found_objects.append(ghost)

        # check if there is new object found in frame
        for i in range(box_count):
            if used[i] == 0:
                last_id += 1
                box = boxes[i]
                boundbox = [box[1], box[0], box[3], box[2]]

                obj = {}
                obj['id'] = last_id
                obj['box'] = boundbox
                obj['class'] = classes[i]
                obj['score'] = scores[i]
                obj['first_time'] = curr_time
                obj['is_alerted'] = False
                obj['frames_to_live'] = self.previous_error
                found_objects.append(obj)

                if line_intersection(obj['box'], main_line):
                    is_alert = True

        # if on this frame was alert, all objects (without ghosts) are alerted
        if is_alert:
            for i in range(len(found_objects)):
                if found_objects[i]['frames_to_live'] == self.previous_error:
                    found_objects[i]['is_alerted'] = is_alert

        return is_alert, found_objects

    def receiveFrame(self, camera_id, frame, main_line):
        main_line = ((main_line[0], main_line[1]), (main_line[2], main_line[3]))
        
        # get ghosts from redis
        objects =  self.redis_cli.get(camera_id)
        if objects:
            objects = json.loads(objects.decode('utf-8'))
        else:
            objects = []
        
        # analyse
        is_alert, found_objects = self.analyseFrame(frame, main_line, objects)

        # save objects as ghosts to redis
        self.redis_cli.set(camera_id, json.dumps(found_objects))

        # format bounding boxes only for objects without ghosts
        objects = []
        for found_object in found_objects:
            if found_object['frames_to_live'] == self.previous_error:
                obj = {}
                obj['id'] = found_object['id']
                obj['x1'] = found_object['box'][0]
                obj['y1'] = found_object['box'][1]
                obj['x2'] = found_object['box'][2]
                obj['y2'] = found_object['box'][3]
                obj['class'] = found_object['class']
                objects.append(obj)

        # create json for request result
        json_out = {}
        json_out['is_alert'] = is_alert
        json_out['objects'] = objects

        return json_out