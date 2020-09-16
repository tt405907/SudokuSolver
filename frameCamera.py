from tkinter.ttk import Frame
import cv2 
import tkinter
import PIL
from PIL import Image
from PIL import ImageTk
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
import numpy
class FrameCamera(Frame):
    # For the realization of this class, I was guided by this example for the whole part of capturing the image from the camera and displaying it on the canvas.
    # https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
    """ This class will manage the Frame of camera """
    def __init__(self,root,videoSource=0):
        self.root = root
        self.videoSource = videoSource
        #self.initCameraDevice()
        self.initCanvas()
        #self.updateFrame()
        self.managerImage = ManagerImage()
        self.imageTest()
    
    def imageTest(self):
        img = Image.open("data/ImagesTest/image6.JPG")
        img =  img.resize((640,480), Image.ANTIALIAS )
        img  = img.rotate(270,expand=True)
        self.photo = Pil_imageTk.PhotoImage(image=img,master=self.root)
        self.canvas.create_image(0, 0, anchor= tkinter.NW, image= self.photo)
        self.canvas.image = self.photo
        # change size canvas, just for my eyes
        img_width,img_height = img.size
        self.canvas.configure(width=img_width,height=img_height)
        # Let's goooo
        self.managerImage.preprocessingImage(img)
        self.managerImage.processing()

    def initCameraDevice(self):
        """ This function allows the instantiation of VideoCapture to activate the camera """
        # If the attribut of cv2 if not detected, CTR + SHIFT + P ->  Preferences: Open Settings (JSON)
        # add "python.linting.pylintArgs": ["--generate-members"]
        self.videoCapture = cv2.VideoCapture(self.videoSource)
        if not self.videoCapture.isOpened():
            raise ValueError("Unable to open video source", self.videoSource)
        # Get video source width and height
        self.width  = self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def initCanvas(self):
        """ This function allows the instantiation of the canvas to store our camera images """
        # temporary for not init CameraDevice taking to much time 
        self.width = 640
        self.height = 650
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


class ManagerImage:
    def __init__(self):
        pass

    def preprocessingImage(self,orignalImage):
        self.orignalImage = orignalImage
        # cv2.UMat was not working, so i try this because it's equivalent
        self.imageUMat = numpy.array(orignalImage)
        #cv2.imshow("image UMat", imageUMat)
        # Original Image to Gray
        self.imageGray = cv2.cvtColor(self.imageUMat,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Gray Image", imageGray)
        # Image Gray with somme Gaussian Blur to improve image quality (parameters find on internet, i need learn how to improve this )
        self.imageGaussBlur = cv2.GaussianBlur(self.imageGray,(5,5),1) 
        #cv2.imshow("Gaussian Blur", imageGaussBlur)
        # Now will get the edges of this image (params full random)
        self.imageCanny = cv2.Canny(self.imageGaussBlur,10,50)
        cv2.imshow("Image Edges", self.imageCanny)
    
    def processing(self):
        # Step 1 : Get countours (parameter find on internet yes yes )
        contours, hierarchy = cv2.findContours(self.imageCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        self.imageCountours = self.imageUMat.copy()
        # je deviens magicien
        cv2.drawContours(self.imageCountours,contours,-1,(255,0,0),3)
        cv2.imshow("Image Countours", self.imageCountours)
        # Step 2 : Get Rectangles
        listRectCorners = self.getRectanglesCorners(contours)
        listSudokuCorners = self.getSudokuCorners(listRectCorners)

    def getRectanglesCorners(self,contours):
        listRect = []
        for contour in contours:
            approximatePoints = self.getRectangleCornersPoints(contour)
            if( len(approximatePoints) == 4 ):
                listRect.append(approximatePoints)
                print("RECTANGLE HERE")
        return listRect
    
    def getRectangleCornersPoints(self,contour):
        # Calculates a contour perimeter or a curve length.
        perimeter = cv2.arcLength(contour,True)
        # Approximates a polygonal curve(s) with the specified precision (curve,epsilon(1%-5% perimeter),closed(first and last Point connected))
        approximatePoints = cv2.approxPolyDP(contour,0.01*perimeter,True)
        return approximatePoints
    
    def getSudokuCorners(self,listRectCorners):
        sudokuCorners = []
        sudokuArea = 0
        # Simple way (get he biggest) TEMPORARY 
        for corners in listRectCorners:
            areaRect = cv2.contourArea(corners)
            if(areaRect > sudokuArea):
                sudokuCorners = corners
                sudokuArea = areaRect

        self.imageTemp = self.imageUMat.copy()
        #print("area : " + str(cv2.contourArea(corners)))
        cv2.drawContours(self.imageTemp,sudokuCorners,-1,(255,0,0),10)
        cv2.imshow("Image sudoku Corners", self.imageTemp)


