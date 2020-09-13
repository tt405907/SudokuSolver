from tkinter.ttk import Frame
import cv2 

class FrameCamera(Frame):
    # https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
    """ This class will manage the Frame of camera """
    def __init__(self,root,video_source=0):
        self.root = root
        # If the attribut of cv2 if not detected, CTR + SHIFT + P ->  Preferences: Open Settings (JSON)
        # add "python.linting.pylintArgs": ["--generate-members"]
        self.videoCapture = cv2.VideoCapture(video_source)
        if not self.videoCapture.isOpened():
            raise ValueError("Unable to open video source", video_source)
    