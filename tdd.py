import requests
import cv2
import json
import base64

from utils import constants as C

def send(frame, mainLine):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    frame_shape = frame.shape
    _, frame = cv2.imencode(".jpg", frame)
    frame = base64.b64encode(frame).decode()

    data = {
        "Camera_id": "TEST",
        "Task_id": "123456798",
        "Frame": frame,
        
        "Frame_shape": frame_shape,
        "Points": mainLine
    }

    url = f"http://{C.HOST}:{C.PORT}/api/human_detection"
    # print(url)

    req = requests.post(url, data=json.dumps(data, indent=4, sort_keys=True, default=str), headers=headers)
    ans = json.loads(req.text)

    return ans

def test_1():
    frame = cv2.imread("./test/images/nothing.jpg")
    mainLine = (30, 327, 940, 344)
    
    ans = send(frame, mainLine)

    if ans.get("is_alert") == False and ans.get("objects") == []:
        print("TEST_1 OK")
    else:
        print("TEST_1 Fail")
        print(ans)

def test_2():
    frame = cv2.imread("./test/images/bird.jpg")
    mainLine = (30, 327, 940, 344)
    
    ans = send(frame, mainLine)

    if ans.get("is_alert") == False and ans.get("objects") == []:
        print("TEST_2 OK")
    else:
        print("TEST_2 Fail")
        print(ans)

def test_3():
    frame = cv2.imread("./test/images/person.jpg")
    mainLine = (0, 212, 640, 212)
    
    ans = send(frame, mainLine)

    if ans.get("is_alert") == True and ans.get("objects") != []:
        print("TEST_3 OK")
    else:
        print("TEST_3 Fail")
        print(ans)

def test_4():
    frame = cv2.imread("./test/images/nothing.jpg")
    mainLine = (0, 212, 640, 212, 1)
    
    ans = send(frame, mainLine)

    if ans.get("error") != None:
        print("TEST_4 OK")
    else:
        print("TEST_4 Fail")
        print(ans)

if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
    test_4()
