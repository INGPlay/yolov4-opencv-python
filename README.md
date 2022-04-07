# yolov4-opencv-python
  
git cloned from : https://github.com/Asadullah-Dal17/yolov4-opencv-python
   
```bash
python yolov4.py --videoFile video --weights .weights --cfg .config --classTxt classes.txt --output outputVideo --outputFps fps --codec codec
```
  
## demo
```bash
python yolov4.py --videoFile input.avi
python yolov4.py --videoFile input.mp4 --output 2.avi
```
  
## flag  
--videoFile, -v   
--weights, -w 'yolov4-tiny.weights'   
--cfg, -c 'yolov4-tiny.cfg'   
--classTxt, -cl 'classes.txt'  
--output, -o   
--outputFps, -f 30   
--codec, -co 'XVID'   
    
    
## feature  
   
videoFile을 객체 탐색해서 GUI로 출력함   
output값이 들어가는 경우 영상을 출력함
    