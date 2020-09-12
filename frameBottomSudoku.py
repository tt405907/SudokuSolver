import tkinter
from tkinter.ttk import Frame
from timeit import default_timer
class FrameBottomSudoku(Frame):
    """ This class allows the management of the entire area below the sudoku """
    def __init__(self,root,rootmain,functionResetGame,functionNewGame,functionActiveBot):
        # Frame Grid
        self.frameGrid = tkinter.Frame(root, background='black')
        self.frameGrid.pack(fill=tkinter.BOTH)
        #self.frameGrid.grid( row=0, column=0 )
         # Timer Resolve
        var = tkinter.StringVar()
        var.set(0)
        self.label_timer = tkinter.Label(self.frameGrid,textvariable=var)
        self.label_timer.configure(font=("Helvetica",18),background="black",foreground='white',highlightthickness=0,borderwidth=0)
        self.label_timer.pack(side=tkinter.LEFT, padx=10,pady=13)

        self.initial_timer = default_timer()
        self.root = rootmain
        self.updateTime()

        # New Game
        self.buttonNewGame = tkinter.Button(self.frameGrid, text="New Sudoku")
        self.buttonNewGame.bind("<Button-1>", functionNewGame)
        self.buttonNewGame.pack(side=tkinter.RIGHT, padx=(0,0), pady=13)
        # Reset Timer of the game & the game
        self.buttonReset = tkinter.Button(self.frameGrid, text="Restart")
        self.buttonReset.bind("<Button-1>", functionResetGame)
        self.buttonReset.pack(side=tkinter.RIGHT, padx=(0,10), pady=13)
        # Bot Active 
        self.buttonBotActive = tkinter.Button(self.frameGrid, text="Active Bot")
        self.buttonBotActive.bind("<Button-1>", functionActiveBot)
        self.buttonBotActive.pack(side=tkinter.RIGHT, padx=(0,10), pady=13)

    # Reboot Time 
    def rebootTimer(self):
        """ This function will reboot the timer of the game """
        self.initial_timer = default_timer()
        self.updateTime()

    def updateTime(self):
        """ This function is looping non stop when he is call for updating the time """
        difference_time = default_timer() - self.initial_timer
        m,s = divmod(difference_time, 60)
        h,m= divmod(m,60)
        text_ = "%d:%02d:%02d" % (h,m,s)
        var = tkinter.StringVar()
        var.set(text_)
        self.label_timer.configure(textvariable=var)
        self.root.after(1000,self.updateTime)
