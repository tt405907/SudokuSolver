import tkinter
from frameSudoku import FrameSudoku
from frameBottomSudoku import FrameBottomSudoku
from bot import botManager,BotBacktracking,typeBot
from windowScan import ManagerWindowScan

class managerWindowSudoku:
    """ This class allows the management of the Sudoku window """
    def __init__(self,title,width,height):
        # Window Setup
        self.window = tkinter.Tk()
        self.window.title(title)
        self.window.minsize(width,height)
        self.window.maxsize(width,height)
        self.window.protocol("WM_DELETE_WINDOW", self.callback_closing)
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
        self.managerFrameBottomSudoku = FrameBottomSudoku(self.frameBottomSudoku,self.window,self.callback_restartGame,self.callback_newGame,self.callback_activeBot,self.callback_scan)
        # Manager Bot
        self.managerBot = botManager(self.window,self.managerFrameSudoku,self.managerFrameBottomSudoku.buttonBotActive,self.managerFrameSudoku.current_board,typeBot.BOT_BACKTRACKING)
        # Manager Scan windows
        self.managerWindowScan = ManagerWindowScan("Sudoku Scan",640,480)

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
    
    def callback_scan(self,event):
        """ This will launch a new window where we will scan a sudoku and resolve it """
        self.managerWindowScan.destroy()
        print(">> SCAN SUDOKU RUNNING")
        self.managerWindowScan.run()

    def callback_closing(self):
        """ This function will destroy this window and the Scan windows if he is running"""
        self.managerWindowScan.destroy()
        print(">> SUDOKU CLOSE")
        self.window.destroy()

    def run(self):
        """ Run Run Run """
        print(">> SUDOKU RUNNING")
        self.window.mainloop()



