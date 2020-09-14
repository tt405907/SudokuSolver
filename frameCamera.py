from tkinter.ttk import Frame
import cv2 
import tkinter
import PIL
from PIL import Image
from PIL import ImageTk
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
class FrameCamera(Frame):
    # https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
    """ This class will manage the Frame of camera """
    def __init__(self,root,videoSource=0):
        self.root = root
        self.videoSource = videoSource
        self.initCameraDevice()
        self.initCanvas()
        self.updateFrame()

    def initCameraDevice(self):
        # If the attribut of cv2 if not detected, CTR + SHIFT + P ->  Preferences: Open Settings (JSON)
        # add "python.linting.pylintArgs": ["--generate-members"]
        self.videoCapture = cv2.VideoCapture(self.videoSource)
        # Resolution x 
        self.videoCapture.set(3,500)
        # Resolution y 
        self.videoCapture.set(4,500)
        if not self.videoCapture.isOpened():
            raise ValueError("Unable to open video source", self.videoSource)
        # Get video source width and height
        self.width = self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("width : " + str(self.width) + " height  : " + str(self.height))

    def initCanvas(self):
        # init canvas
        self.canvas = tkinter.Canvas(self.root,width= self.width,height = self.height)
        self.canvas.pack()
        # Refresh time image, 60 FPS
        self.delay = 10

    def updateFrame(self):
        retval,frame = self.getFrame()
        if(retval):
            photo = Pil_imageTk.PhotoImage(image = Pil_image.fromarray(frame))
            self.canvas.create_image(0,0,image=photo,anchor=tkinter.NW)
        self.root.after(self.delay,self.update)


    def getFrame(self):
        """ This function will return a frame of the video camera"""
        if(self.videoCapture.isOpened()):
            retval,frame = self.videoCapture.read()
            if retval :
                cv2.imshow('image',frame)
                return (retval, cv2.cv2.COLOR_BGR2RGB)
            else:
                return (retval,None)

        return (False,None)
    
    def close(self):
        """ This function will close the capturing device """
        if self.videoCapture.isOpened():
            self.videoCapture.release()

