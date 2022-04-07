import cv2
import time
import argparse

parser = argparse.ArgumentParser(description=
    "Count number of Taxis and Passengers "
)

parser.add_argument('--videoFile', '-v', type=str,
    help='path for video')
parser.add_argument('--weights', '-w', type=str, default='yolov4-tiny.weights',
    help='YOLOv4 weights file')
parser.add_argument('--cfg', '-c', type=str, default='yolov4-tiny.cfg',
    help='YOLOv4 config file')
parser.add_argument('--classTxt', '-cl', type=str, default='classes.txt',
    help='Class Text file')
parser.add_argument('--output', '-o', type=str,
    help='output video file')
parser.add_argument('--outputFps', '-f', type=int, default=30,
    help='output video fps')
parser.add_argument('--codec', '-co', type=str, default='XVID',
    help='video codec')

args = parser.parse_args()
videoFile= args.videoFile
weights = args.weights
cfg = args.cfg
classTxt = args.classTxt
output = args.output

Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class_name = []
with open(classTxt, 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]
print(class_name)
net = cv2.dnn.readNet(weights, cfg)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

cap = cv2.VideoCapture(videoFile)
starting_time = time.time()
frame_counter = 0

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if output :
    fps = args.outputFps
    codec = cv2.VideoWriter_fourcc(*args.codec)

    out = cv2.VideoWriter(output, codec, fps, (width, height))

frame_id = 0
while True:
    ret, frame = cap.read()
    frame_counter += 1
    if ret == False:
        if frame_id == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            print("Video processing complete")
            break
        continue

    class_num = [0, 0]
    classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = f"{class_name[classid]} : {score:0.2f}"
        
        class_num[classid] += 1
        cv2.rectangle(frame, box, color, 1)
        cv2.putText(frame, label, (box[0], box[1]-10),
                   cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 1)

    endingTime = time.time() - starting_time
    fps = frame_counter/endingTime

    cv2.putText(frame, f'FPS: {fps:0.2f}', (20, 50),
               cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'{class_name[0]} : {class_num[0]}', (60, height - 130),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(frame, f'{class_name[1]} : {class_num[1]}', (60, height - 100),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow('frame', frame)

    if args.output:
        out.write(frame)

    key = cv2.waitKey(1)

    # 27 : esc
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
