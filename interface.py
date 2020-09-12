import tkinter
from frameSudoku import FrameSudoku
from frameBottomSudoku import FrameBottomSudoku
from bot import botManager,BotBacktracking,typeBot
from unrar import rarfile
import os

class Interface:
    """ Main class """
    def __init__(self,title,width,height):
        # Window Setup
        self.window = tkinter.Tk()
        self.window.title(title)
        self.window.minsize(width,height)
        self.window.maxsize(width,height)
        # General color of the background of the Game
        self.window.configure(background='black')
        # Frame sudoku
        self.frameSudoku = tkinter.Frame(self.window, background='black')
        self.frameSudoku.grid( row=0, column=0 )
        # Manager Frame Sudoku
        self.managerFrameSudoku = FrameSudoku(self.frameSudoku)  
        # Frame Bottom Sudoku
        self.frameBottomSudoku = tkinter.Frame(self.window,background="brown")
        self.frameBottomSudoku.grid(row=1,column=0,sticky='WE',padx=(10,0))
        # Manager Bottom Frame Sudoku
        self.managerFrameBottomSudoku = FrameBottomSudoku(self.frameBottomSudoku,self.window,self.callback_restartGame,self.callback_newGame,self.callback_activeBot)
        # Manager Bot
        self.managerBot = botManager(self.window,self.managerFrameSudoku,self.managerFrameBottomSudoku.buttonBotActive,self.managerFrameSudoku.current_board,typeBot.BOT_BACKTRACKING)

    def callback_restartGame(self,event):
        """ This is the callback calling by the button "restart" in the UI """
        print(">> RESTART GAME")
        self.managerFrameSudoku.rebootGameToInitial()
        self.managerFrameBottomSudoku.buttonBotActive.configure(state="normal")
        print(">> RESTART TIMER")
        self.managerFrameBottomSudoku.rebootTimer()
        print(">> RESTART BOT")
        self.managerBot.resetBot()

    def callback_newGame(self,event):
        """ This is the callback calling by the button "Next Game" in the UI """
        print(">> NEW GAME")
        self.managerFrameSudoku.nextSudoku()
        self.managerFrameBottomSudoku.buttonBotActive.configure(state="normal")
        print(">> RESTART TIMER")
        self.managerFrameBottomSudoku.rebootTimer()
        print(">> RESTART BOT")
        self.managerBot.resetBot()
    
    def callback_activeBot(self,event):
        """ This is the callback calling by the button "Active Bot" in the UI """
        if(self.managerFrameBottomSudoku.buttonBotActive.cget('background') == "green"):
            print(">> BOT DESACTIVE")
            self.managerFrameBottomSudoku.buttonBotActive.configure(background="SystemButtonFace",activebackground="SystemButtonFace")
        else:
            print(">> BOT ACTIVE")
            self.managerFrameBottomSudoku.buttonBotActive.configure(background="green",activebackground="green")
            self.managerBot.turnOn()

    def run(self):
        """ Run Run Run """
        self.window.mainloop()

class Application():
    """ Class that makes sure that the pre-processing was done for the interface and game startup """
    def __init__(self):
        pass

    def processRun(self):
        """ This function will check that the pre-processing was done and will return the appropriate boolean """
        sudokucsv = False
        sudokurar = False
        # Check than you already have extract the data from the .rar
        for file in os.listdir('data'):
            if(file == "sudoku.rar"):
                sudokurar = True
            if(file == "sudoku.csv"):
                sudokucsv = True
        # Already extract
        if(sudokucsv):
            return True
        # We have to extract
        if(sudokurar):
            print(">> FILE EXTRACT")
            rar = rarfile.RarFile('data/sudoku.rar')
            rar.extractall('./data')
            return True
        else:
            return False

    def run(self):
        """ Run the interface """
        if(self.processRun()):
            print(">> PREPROCESSING FINISH")
            # Launch the interface
            interface = Interface("Sudoku",455,500)
            interface.run()
        else:
            print(">> ERROR : There is no sudoku.rar or sudoku.csv, we can't launch the interface")




