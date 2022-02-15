""" Find the dog only


  author: ashraf minhaj
  mail  : minhaj@programming-hero.com
"""

""" install -
$ pip install opecv-contrib-python

download pre-trained model from
- https://drive.google.com/file/d/0BzKzrI_SkD1_NDlVeFJDc2tIU1k/view?resourcekey=0-VIwceFdQvGpMl31jHv5RpA

# github repo - https://github.com/FreeApe/VGG-or-MobileNet-SSD#installation
"""

import cv2
import numpy as np


class BottleFinder():
    def __init__(self, camera, show_output=False):
        self.camera      = camera
        self.show_output = show_output
        print("[initialized]")

    def detect_bottle(self):
        self.found = 0
        print("[detecting]")
        color = (255, 0, 255)

        known_things = ['aeroplane',
                        'bicycle',
                        'bird',
                        'boat',
                        'bottle',
                        'bus',
                        'car',
                        'cat',
                        'chair',
                        'cow',
                        'diningtable',
                        'dog',
                        'horse',
                        'motorbike',
                        'person',
                        'pottedplant',
                        'sheep',
                        'sofa',
                        'train',
                        'tvmonitor'
                        ]

        model_file           = 'VGG_coco_SSD_300x300.caffemodel'
        prototype_model_file = 'deploy.prototxt'
        model                = cv2.dnn.readNetFromCaffe(prototype_model_file, model_file)

        cap = cv2.VideoCapture(self.camera)

        # read an image 
        _, frame = cap.read()                             
        frame_width, frame_height = frame.shape[1], frame.shape[0]                
        resized_frame = cv2.resize(frame, (300, 300))                             
        blob_frame = cv2.dnn.blobFromImage(resized_frame, 0.09, (300, 300), 120) 

        # input our image for detection
        model.setInput(blob_frame)
        output = model.forward()
        detected_objects = output[0][0]

        for object in detected_objects:
            object_index = int(object[1])               
            confidence   = object[2]                    
            start_x      = int(object[3] * frame_width) 
            start_y      = int(object[4] * frame_height) 
            end_x        = int(object[5] * frame_width) 
            end_y        = int(object[6] * frame_height) 

            object_name = known_things[object_index-1]
            #print('name', object_name)
            
            if confidence > 0.2 and object_name == 'bottle':
                print(object_name)
                cv2.rectangle(img=frame,
                            pt1=(start_x, start_y),
                            pt2=(end_x, end_y),
                            color=color, 
                            thickness=2)

                cv2.putText(img=frame,
                            text=object_name, 
                            org=(start_x, start_y), 
                            fontFace=cv2.FONT_HERSHEY_DUPLEX, 
                            fontScale=1,
                            color=color,
                            thickness=1)
                self.found = 1

        # show image
        if self.show_output:
            cv2.imshow("Find My things", frame)
            cv2.waitKey(0)

        cap.release()
        cv2.destroyAllWindows()

        print("Rerturning", self.found)
        return self.found

if __name__ == '__main__':
    finder = BottleFinder(camera=1, show_output=1)
    x = finder.detect_bottle()
    print(x)