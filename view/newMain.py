from view.HumanDetection import DetectorAPI
import threading
import json
from Hikvision import HikAPI

def analyze():
    model_path = './faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
    odapi = DetectorAPI(path_to_ckpt=model_path)

    with open('config.json') as f:
        config = json.load(f)

    cameras = config["cameras"]

    videos = []
    for camera in cameras:
        videos.append(HikAPI(camera, config, odapi))

    def analyzeVid(idx):
        cap = videos[idx]
        
        # outfile = "output_{}.avi".format(3)
        # out = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'XVID'), 25, 
        #                 (int(cap.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        i = idx
        while True:
            frame_out = cap.getFrame(i)
            if(frame_out is None):
                continue
            #if(frame_out.shape[0] > 0):
                # out.write(frame_out)
        
            #    frame_out = cv2.resize(frame_out, (0, 0), fx = 0.5, fy = 0.5)
            #    cv2.imshow("IGUARD", frame_out)

            #    k = cv2.waitKey(1)
            #    if k == ord('q'):
            #        print("Cap is closed")
            #        cv2.destroyAllWindows()
            #        break
            i += 10
            
    #analyzeVid(7)
    jobs = []
    for idx in range(len(videos)):
        # print(idx)
        # analyzeVid(idx)
        process = threading.Thread(target= analyzeVid, args=(idx,))
       
        jobs.append(process)
    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

if __name__ == "__main__":
    analyze()
