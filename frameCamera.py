from tkinter.ttk import Frame
import cv2 
import tkinter
import PIL
from PIL import Image
from PIL import ImageTk
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
class FrameCamera(Frame):
    # For the realization of this class, I was guided by this example for the whole part of capturing the image from the camera and displaying it on the canvas.
    # https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
    """ This class will manage the Frame of camera """
    def __init__(self,root,videoSource=0):
        self.root = root
        self.videoSource = videoSource
        self.initCameraDevice()
        self.initCanvas()
        self.updateFrame()

    def initCameraDevice(self):
        """ This function allows the instantiation of VideoCapture to activate the camera """
        # If the attribut of cv2 if not detected, CTR + SHIFT + P ->  Preferences: Open Settings (JSON)
        # add "python.linting.pylintArgs": ["--generate-members"]
        self.videoCapture = cv2.VideoCapture(self.videoSource)
        if not self.videoCapture.isOpened():
            raise ValueError("Unable to open video source", self.videoSource)
        # Get video source width and height
        self.width = self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def initCanvas(self):
        """ This function allows the instantiation of the canvas to store our camera images """
        # init canvas
        self.canvas = tkinter.Canvas(self.root,width= self.width,height = self.height,bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        # Refresh time image, 60 FPS
        self.delay = 10

    def updateFrame(self):
        """ This function loops on itself at a certain frequency to take images from our camera """
        retval,frame = self.getFrame()
        if(retval):
            self.photo = Pil_imageTk.PhotoImage(image = Pil_image.fromarray(frame),master=self.root)
            self.canvas.create_image(0, 0, anchor= tkinter.NW, image= self.photo)
            self.canvas.image = self.photo

        self.root.after(self.delay,self.updateFrame)


    def getFrame(self):
        """ This function will return a frame of the video camera"""
        if(self.videoCapture.isOpened()):
            retval,frame = self.videoCapture.read()
            if(retval):
                return (retval, cv2.cvtColor(frame,cv2.cv2.COLOR_BGR2RGB))
            else:
                return (retval,None)

        return (False,None)
    
    def close(self):
        """ This function will close the capturing device """
        if self.videoCapture.isOpened():
            self.videoCapture.release()

