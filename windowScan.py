import tkinter
from frameCamera import FrameCamera

class ManagerWindowScan:
    """ This class allows the management of the Sudoku Scan window """
    def __init__(self,title,width,height):
        self.title = title
        self.width = width
        self.height = height
        self.running = False

    def run(self):
        """ Run Run Run """
        # Window Setup
        self.running = True
        self.window = tkinter.Tk()
        self.window.title(self.title)
        self.window.minsize(self.width,self.height)
        self.window.maxsize(self.width,self.height)
        # General color of the background of the Game
        self.window.configure(background='black')
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)
        # Frame sudoku
        self.frameCamera = tkinter.Frame(self.window, background='black')
        self.frameCamera.grid( row=0, column=0 )
        # Manager Frame Sudoku
        self.managerFrameCamera = FrameCamera(self.frameCamera) 
        # Window receptive
        self.window.mainloop()


    def destroy(self):
        """ This function will destroy the window """
        if(self.running):
            print(">> SCAN SUDOKU CLOSE")
            self.window.destroy()
        self.running = False
    
