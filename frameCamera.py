from tkinter.ttk import Frame
import cv2 
import tkinter
import PIL
from PIL import Image
from PIL import ImageTk
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
import numpy
from keras.datasets import mnist
from keras.utils    import to_categorical
from keras.models   import Sequential, load_model
from keras.layers   import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

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
        img = img.resize((640,480), Image.ANTIALIAS )
        img = img.rotate(270,expand=True)
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
        self.modelDigits = load_model("data/digits_model.h5")

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

        # Stupid simple 
        sudokuCorners = self.getSudokuCorners(listRectCorners)
        sudokuCornersOrdered = self.orderPoints(sudokuCorners)
        img_width,img_height = self.orignalImage.size
        imageSudokuCornersOrderedWarp =  self.imageWarp(self.imageUMat.copy(),sudokuCornersOrdered,img_width,img_height)
        cv2.imshow("imageSudokuCornersOrderedWarp", imageSudokuCornersOrderedWarp)
        i = 0
        listRectCornersOrdered = [self.orderPoints(x) for x in listRectCorners]
        for rectCornersOrdered in listRectCornersOrdered:
            cv2.imshow("listRectCornersOrdered : " + str(i) , self.imageWarp(self.imageUMat.copy(),rectCornersOrdered,img_width,img_height))
            i+=1

    def predictionDigit(self,positionCell,image):
        pass

    def boardSudoku(self,image):
        """ This function will allow us to extract each number from each cell of the image and return the corresponding board """
        board = []
        cellsPosition = self.listPositionsCell() 
        listRow = []
        for cellPos in cellsPosition:
            prediction = self.predictionDigit(cellPos,image)
            # if last value of the row
            if(cellPos[0] == 224):
                board.append(listRow)
                listRow = []
        return board

    def listPositionsCell(self):
        """ This function is returning all the position of Origin to each cells in the image """
        listPositionsCell = []
        # Resize image to (252,252) because our model shape(28, 28) -> 28 * 9 = 252
        #imageSized = image.resize((252,252), Image.ANTIALIAS )
        x = 0
        y = 0
        for i_row in range(0,9):
            y += 28
            x = 0
            for i_column in range(0,9):
                listPositionsCell.append([x,y])
                x += 28
        return listPositionsCell

    def getPrediction(self,image):
        prediction = self.modelDigits.predict(image)
        return prediction.argmax()

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
        return numpy.array(sudokuCorners)

        

    def orderPoints(self,points):
        """ """
        pointsReshape = points.reshape((4,2))
        # New shape of the points
        newpts =  numpy.zeros((4,2), dtype = "float32")
        # [ x  y ] -> [x + y]
        sumPts = pointsReshape.sum(axis=1)
        # Bottom left
        newpts[0] = pointsReshape[numpy.argmin(sumPts)]
        # Top right
        newpts[3] = pointsReshape[numpy.argmax(sumPts)]
        
        diff = numpy.diff(pointsReshape,axis=1)
        # BOTTOM RIGHT
        newpts[1] = pointsReshape[numpy.argmax(diff)]
        # TOP LEFT
        newpts[2] = pointsReshape[numpy.argmin(diff)]
        return newpts

    def imageWarp(self,image,pointsOrdered,img_width,img_height):
        newPoints = numpy.array([[0,0],[0,img_height],[img_width,0],[img_width,img_height]],dtype = "float32")
        matrix =  cv2.getPerspectiveTransform(pointsOrdered,newPoints)
        imageWarp = cv2.warpPerspective(image,matrix,(img_width,img_height))
        return imageWarp


    # If you call this method you will run the learning of the model and it will take some times
    def initModel(self):
        """ I used this method to generate the model which was going to allow me to make the recognition of the digits """
        """ Import from : https://www.sitepoint.com/keras-digit-recognition-tutorial/ """
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        image_index = 35
        print(y_train[image_index])
        print(x_train.shape)
        print(x_test.shape)
        img_rows, img_cols = 28, 28

        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        x_train=x_train.astype(float)
        x_test=x_test.astype(float)
        x_train /= 255
        x_test /= 255

        num_classes = 10

        y_train = to_categorical(y_train, num_classes)
        y_test = to_categorical(y_test, num_classes)


        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
            activation='relu',
            input_shape=(img_rows, img_cols, 1)))

        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))
        model.compile(loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])
        batch_size = 128
        epochs = 10

        model.fit(x_train, y_train,
                batch_size=batch_size,
                epochs=epochs,
                verbose=1,
                validation_data=(x_test, y_test))
        score = model.evaluate(x_test, y_test, verbose=0)
        print('Test loss:', score[0]) # Test loss: 0.026652975007891655
        print('Test accuracy:', score[1]) # Test accuracy: 0.9916999936103821
        model.save("data/digits_model.h5")

