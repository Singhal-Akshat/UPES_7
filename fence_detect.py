#============Useful libraries====================
import cv2
import math
import sys
import numpy as np

class detect:
    '''
    Class used for fence detection
    '''
    def __init__(self,video_name):
        self.video_name = video_name

    def capture(self):
        self.cap = cv2.VideoCapture(self.video_name)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')


        