import requests
import pprint
import cv2
import json
import base64

from utils import constants as C

def test_1():
    image = cv2.imread("/home/user/Desktop/human_detection_analysis/test/images/nothing.jpg")
    mainLine = (30, 327, 940, 344)
    # image = cv2.imencode('.jpg', image)[1].tostring()
    image_shape = image.shape
    print(image.shape)
    image = base64.b64encode(image)
    # d = image.flatten ()
    #print(image)
    # image = d.tostring ()
    print(type(image))

    data = {
        "camera_id": "123456789",
        "task_id": "123456798",
        "image": image,
        
        "x1": mainLine[0],
        "y1": mainLine[1],
        "x2": mainLine[2],
        "y2": mainLine[3],
        
        "height": image_shape[0],
        "width": image_shape[1],
        "layers": image_shape[2],
    }

    # print(data)
    url = f"http://{C.HOST}:{C.PORT}/api/human_detection"
    print(url)

    r = requests.post(url, data=data)
    #r = requests.get(url)
    print(r.text)


if __name__ == "__main__":
    test_1()

