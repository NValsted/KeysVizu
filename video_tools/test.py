import time

import cv2
import mss
import numpy

frame_width = 800
frame_height = 640
frame_rate = 20.0
VIDEO_OUTPUT = "output.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(VIDEO_OUTPUT, fourcc, frame_rate, 
                      (frame_width, frame_height))

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))
        img = cv2.resize(img,(frame_width,frame_height))
        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # Might be able to do "numpy array out" more efficient
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        out.write(img)
        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        #Display the picture in grayscale
        #cv2.imshow('OpenCV/Numpy grayscale',
        #           cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            out.release()
            cv2.destroyAllWindows()
            break