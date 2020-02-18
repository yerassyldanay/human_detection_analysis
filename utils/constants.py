STATUS_OK = "200"
STATUS_ERROR = "500"

HOST = "0.0.0.0"
PORT = "7000"

REDIS_HOST = "local_redis"
REDIS_PORT = 6379
REDIS_DB = 0

MODEL_PATH = './view/model/frozen_inference_graph.pb' # faster path
# MODEL_PATH = './view/model/' # yolo path
OBJECT_TRACKING = True
OBJECT_THRESHOLD = 0.85
OBJECT_CLASSES = [1] # human -> 1 in faster, 0 in yolo
FRAMES_TO_LIVE = 5
TIME_TO_LIVE = 10
TIME_TO_LIVE_LONG = 3600 #  1 hour
ALERT_DELAY = 5.0