import requests
import pprint
import cv2
from utils import constants as C

def test_1():
    img = cv2.imread("./images/1.jpg")
    mainLine = (30, 327, 940, 344)

    data = {
        "camera_id": "123456789",
        "task_id": "123456798",
        "image": img,
        "points": mainLine,
    }

    url = f"http://{C.HOST}:{C.PORT}/api/human_detection"
    print(url)

    r = requests.post(url, data=data)
    #r = requests.get(url)
    pprint.pprint(r.json())


if __name__ == "__main__":
    test_1()

