from board import Board
import tkinter
from tkinter.ttk import Frame
import copy

class FrameSudoku(Frame):
    """ This class allows the management of all the interface part of the sudoku """
    def __init__(self,root):
        # Some Stats of games
        self.numberGame = 0
        self.listOfTime = []
        # True for Finish and False for not end
        self.listOfState = []

        self.root = root
        # Init the Board Game
        self.current_board = Board(self.numberGame)
        self.initAllEntry()
        self.updateAllEntry()

    def rebootGameToInitial(self):
        """ Reboot the same Sudoku from the start """
        self.current_board.boardInit(self.numberGame)
        self.updateAllEntry()

    def nextSudoku(self):
        """ Setup the next Sudoku interface """
        self.numberGame+=1
        self.rebootGameToInitial()
        

    def initAllEntry(self):
        """ Init all the tkinter Entry for the Sudoku """
        # Grid Setup
        self.list_Entry = []
        for i_row in range(0,9):
            self.list_Entry.append([])
            for i_column in range(0,9):
                entry = tkinter.Entry(self.root,width=2,font=('Helvetica',28),justify='center')
                entry.grid( row=i_row, column=i_column )
                # Padx left Squares
                if(i_column % 3 == 0):
                    entry.grid(padx=(10,0))
                # Pady top Squares
                if(i_row % 3 == 0):
                    entry.grid(pady=(10,0))
                self.list_Entry[i_row].append(entry)
    
    def updateAllEntry(self):
        """ Update all the tkinter Entry with the right number inside and the good state, from the Board """
        for i_row in range(0,9):
            for i_column in range(0,9):
                # Delete the old value in the Entry
                self.list_Entry[i_row][i_column].configure(textvariable=tkinter.StringVar(value=""))
                # Get the data from the board
                data = self.current_board.update_board[i_row][i_column]
                # Convert the text from the board
                text = tkinter.StringVar(value=str(data)) if data != 0 else ""
                # Reset all the Entry 
                self.list_Entry[i_row][i_column].configure(state='normal',textvariable=text)
                # Desactive the Entry for init number
                if(data != 0):
                    self.list_Entry[i_row][i_column].configure(state='disabled')
        
    def updateEntry(self,row,column,value):
        """ This function will update a specific Entry of the board"""
        self.list_Entry[row][column].configure(textvariable=tkinter.StringVar(value=""))
        text = tkinter.StringVar(value=str(value)) if value != 0 else ""
        self.list_Entry[row][column].configure(textvariable=text)