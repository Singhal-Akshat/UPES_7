#============Useful libraries====================
import cv2
import math
import sys
import numpy as np
import logging

class detect:
    '''
    Class used for fence detection
    '''
    def __init__(self,video_name):
        '''
        Function used to take the video file at the time of
        oject call and perform initialization of the global 
        variable
        '''
        try:
            self.video_name = video_name
            file_extension = self.video_name.split('.') 
            self.extension = file_extension[1]
            self.xf1 = sys.maxsize
            self.yf1 = sys.maxsize
            self.xf2 = 0
            self.yf2 = sys.maxsize
            self.xf3 = sys.maxsize
            self.yf3 = 0
            self.xf4 = 0
            self.yf4 = 0
        except Exception as e:
            print("Invalid file format. *Use mp4 file*")
                 

    def capture(self):
        '''
        Function used to read the video file
        '''
        self.extension = self.extension.lower()
        self.cap = cv2.VideoCapture(self.video_name)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        self.out = cv2.VideoWriter('output.mp4', self.fourcc, 30.0, (int(self.cap.get(3)), int(self.cap.get(4))),isColor=True)
    
    def run(self):
        '''
        Function used to detect the fence 
        and return the optimised 
        detected fence cordinates
        '''
        l_x1 = []
        l_y1 = []
        l_x2 = []
        l_y2 = []
        l_x3 = []
        l_y3 = []
        l_x4 = []
        l_y4 = []
        # Loop through frames in video
        self.capture()
        while(self.cap.isOpened()):
        # Read frame
            ret, frame = self.cap.read()
            if not ret:
                break

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply Canny edge detection to detect edges
            edges = cv2.Canny(gray, 100, 200)

            # Apply Hough Line Transform to detect lines
            lines = cv2.HoughLinesP(edges, 1, 3.14/180, 100, minLineLength=100, maxLineGap=10)

            # Draw detected lines on original image
            # x1,y1,x2,y2,x3,y3,x4,y4 = sys.maxsize,sys.maxsize,0,sys.maxsize,sys.maxsize,0,0,0

            # Cordinated List to store the cordinates of ith image frame 
            x1,y1,x2,y2,x3,y3,x4,y4 = sys.maxsize,sys.maxsize,0,sys.maxsize,sys.maxsize,0,0,0
            try:
                for line in lines:
                    xa,ya,xb,yb = line[0]
                    cv2.line(frame,(xa,ya),(xb,yb),(0,0,255),1)

                    # logic to make the frame
                    if(xa<x1) and ya<y1:
                        x1 = xa
                        y1 = ya
                    if xa>x2 and ya<y2:
                        x2 = xa
                        y2 = ya
                    if y3<yb and xb<x3:
                        x3 = xb
                        y3 = yb
                    if y4<yb and x4<xb:
                        x4 = xb
                        y4 = yb
            except:
                continue
            l_x1.append(x1)
            l_y1.append(y1)
            l_x2.append(x2)
            l_y2.append(y2)
            l_x3.append(x3)
            l_y3.append(y3)
            l_x4.append(x4)
            l_y4.append(y4)
            
            pts = np.array([[x1,y1],[x3,y3],[x4,y4],[x2,y2]])
            cv2.polylines(frame,[pts],True,(255,0,0))
            self.out.write(frame)

            # Display result
            cv2.imshow('Result', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap = cv2.VideoCapture(self.video_name)
        xf1,yf1,xf2,yf2,xf3,yf3,xf4,yf4 = np.mean(l_x1),np.mean(l_y1),np.mean(l_x2),np.mean(l_y2),np.mean(l_x3),np.mean(l_y3),np.mean(l_x4),np.mean(l_y4)
        # Initialize VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))), isColor=True)
        ret, frame = cap.read()
        pts2 = np.array([[int(xf1),int(yf1)],[int(xf3),int(yf3)],[int(xf4),int(yf4)],[int(xf2),int(yf2)]])
        cv2.polylines(frame,[pts2],True,(255,0,0),3)
        cv2.imshow('Result', frame)
        cv2.waitKey(0)

        # Release resources
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        return pts2


obj = detect('video1.mp4')
obj.run()
        