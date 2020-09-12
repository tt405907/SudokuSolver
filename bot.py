from abc import ABC, abstractmethod
import copy
from board import Board
from enum import Enum

class typeBot(Enum):
    """ If one day I implement another bot to compare performances it will be useful to me """
    BOT_BACKTRACKING = 1

class botManager:
    def __init__(self,root,managerSudoku,bouton,board,typeBot):
        self.root = root
        self.boutonBot = bouton
        self.managerSudoku = managerSudoku
        self.board = board
        self.typeBot = typeBot
        self.bot = self.initBot(typeBot)

    def resetBot(self):
        """ This function create a new instance of the bot with the new bord """
        self.bot = self.initBot(self.typeBot)

    def initBot(self,typeBot):
        """ This function return a new instance of Bot """
        if(typeBot == typeBot.BOT_BACKTRACKING):
             return BotBacktracking(self.board.update_board)

    def turnOn(self):
        """ This function active the bot """
        self.boucleBot()
    
    def boolActivationBot(self):
        """ This function allows to check the status of the button ButtonBotActive to see if we need to stop the botManager """
        return self.boutonBot.cget('background') == "green"

    def boucleBot(self):
        """ This function loops on itself and asks the bot what action it wants to perform on the board and updates the interface and the board with managerSudoku """
        if(self.boolActivationBot() ):
            row,col,val = self.bot.move(self.board.update_board)
            #print("row : " + str(row) + " col : " + str(col) + " val : " + str(val))
            if(row == -1 and col == -1 and val == -1):
                self.boutonBot.configure(background="SystemButtonFace",activebackground="SystemButtonFace",state='disable')
            else:
                self.board.update(val,row,col)
                self.managerSudoku.updateEntry(row,col,val)
                self.root.after(50,self.boucleBot)

class Position:
    """ This class allows to contain the position that the bot has to process """
    def __init__(self,rowSize,columnSize):
        self.row = 0
        self.column = 0
        self.maxRow = rowSize - 1 
        self.maxColumn = columnSize - 1

    def nextPosition(self):
        """ This function allows to advance the position in the board matrix   """
        if(self.column == self.maxColumn):
            self.column = 0
            self.row+=1
        else:
            self.column+=1
    
    def backPosition(self):
        """ This function allows to move back the position in the matrix of the board """
        if(self.column == 0):
            self.row-= 1
            self.column = self.maxColumn
        else:
            self.column-=1

    def __repr__(self):
        return " row : " + str(self.row) + " | column : " + str(self.column)

class BotBacktracking:
    """ This class is the Bot that will solve sudoku using the backtracking principle """
    def __init__(self,listboard):
        self.actions = []
        # Cache all the changes set on the board in order
        self.listCache = [ ]
        # All the possibility numbers for each cells, if their is a number in a cell and not list it's a diseable cell
        self.possibility_board = self.givePossibilityBoard(listboard)
        self.indexMemory = self.giveIndexMemory(listboard)
        # Position
        self.position = Position(9,9)
    
    def giveListNumberWithoutZero(self,listTchuk):
        """ For a given list, return a list without all the 0 inside """
        return [ i for i in listTchuk if i != 0]

    def column(self,matrix, index):
        """ For a given matrix and a index, return the column of it """
        return [row[index] for row in matrix]
        
    def getCubeNumbers(self,row,column,board):
        """ For a given row and column ( Position of the left top corner of the cube that we want get data), this will collect the number (expect the 0) of a cube (3x3) in a board given """
        cube = []
        for row_cube in range((row*3),(row*3)+3):
            for columns_cube in range((column*3),(column*3)+3):
                number = board[row_cube][columns_cube]
                if( number > 0 ):
                    cube.append(number)
        return cube

    def getListCubesNumber(self,board):
        """ For a given board, this will return the list of each cells with all the numbers inside his cube """
        listCubesNumber  = [[ [] for x in range(0,9) ] for x in range(0,9)]
        for i_row in range(0,3):
            for i_column in range(0,3):
                cube = self.getCubeNumbers(i_row,i_column,board)
                # Insert the data from this cube into the cells of this cube
                for row_cube in range((i_row*3),(i_row*3)+3):
                    for columns_cube in range((i_column*3),(i_column*3)+3):
                        listCubesNumber[row_cube][columns_cube] = cube
        return listCubesNumber

    def givePossibilityBoard(self,board):
        """ Return the list of the possibility numbers that can have the empty cells """
        res = []
        listRowsNumber = [ self.giveListNumberWithoutZero(x) for x in board ]
        listColumnsNumber = [ self.giveListNumberWithoutZero(x) for x in [ self.column(board,x) for x in range(0,9)] ]         
        listCubesNumber  = self.getListCubesNumber(board)
    
        for i_row in range(0,9):
            tempRow = []
            for i_column in range(0,9):
                if(board[i_row][i_column] == 0 ):
                    listDefault = set([1,2,3,4,5,6,7,8,9])
                    listSet = set(listRowsNumber[i_row] + listColumnsNumber[i_column] + listCubesNumber[i_row][i_column])
                    result = listDefault - listSet
                    tempRow.append(list(result))
                else:
                    tempRow.append(board[i_row][i_column])
            res.append(tempRow)
        return res
    
    def giveIndexMemory(self,board):
        """ This function initializes the indexMemory matrix that will remind him which sudoku combination he has already performed """
        res = []
        for row in range(0,9):
            tempRow = []
            for column in range(0,9):
                if(board[row][column] == 0):
                    tempRow.append([])
                else:
                    tempRow.append(self.possibility_board[row][column])
            res.append(tempRow)
        return res

    def valid(self,row,column,value,actualBoard):
        """ This function allows you to check whether a value at a location on the board is correct or not """
        for i in range(0,9):
            # Verif row
            if(actualBoard[row][i] == value):
                return False
             # Verif column
            if(actualBoard[i][column] == value):
                return False
        # Verif cube
        cube = self.getCubeNumbers((row//3),(column//3),actualBoard)
        if(value in cube):
            return False
        # Valid value
        return True

    def backtracking(self):
        """ This function deletes the tried values in the cell where we are in the indexMemory and then loops until it reaches the last changed value to see if there is another possible solution """
        # Reset the indexMemory of the actual cell
        self.indexMemory[self.position.row][self.position.column] = []
        # We back position one time before, to not stop on the actual cell
        self.position.backPosition()
        # back position to the last cell
        while type(self.possibility_board[self.position.row][self.position.column]) is not list:
            self.position.backPosition()
        # Reset the value of this actual cell to nothing for update the UI and the board
        return self.position.row,self.position.column,0
        

    def move(self,actualBoard):
        """ This function returns the location and value that the bot chooses to change on the board, format : row,columnn,value """
        i_row = copy.deepcopy(self.position.row)
        i_colmun = copy.deepcopy(self.position.column)
        if(i_row == 9):
            return -1,-1,-1
        cell = self.possibility_board[i_row][i_colmun]
        if(type(cell) is list):
            for value in cell:
                # Verif that this value have not be already testing
                if(value not in self.indexMemory[i_row][i_colmun]):
                    # Verif that the value if valid 
                    if(self.valid(i_row, i_colmun, value, actualBoard) ):
                        # Update the indexMemory of this cell
                        self.indexMemory[i_row][i_colmun].append(value)
                        # Go to next position
                        self.position.nextPosition()
                        # Remember all actions
                        self.actions.append([i_row,i_colmun,value])
                        return i_row,i_colmun,value
            # If their is no value valid, we have to back to change it 
            return self.backtracking()
        else:
            #print("Not a List")
            self.position.nextPosition()
            return self.move(actualBoard)

