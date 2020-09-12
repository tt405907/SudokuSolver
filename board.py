import copy
import numpy
import csv
class Board:
    """ This class represents the sudoku game and all the interactions you can do on it """
    def __init__(self,numberGame):
        # Load the data from the csv 
        with open("data/sudoku.csv",'r') as f:
            self.data_board = list(csv.reader(f,delimiter=","))
        self.data_board.pop(0)
        self.boardInit(numberGame)
        self.update_board = copy.deepcopy(self.start_board)
        self.right_position_update = self.list_postion(self.start_board)
        # Optionnal Printer Boolean
        self.printer = False

    def boardInit(self,numberGame):
        """ Init/Update the board from a data base"""
        self.start_board = []
        listboard = list(self.data_board[numberGame][0])
        temp = []
        for i in listboard:
            temp.append(int(i))
            if(len(temp)== 9):
                self.start_board.append(temp)
                temp=[]
        self.update_board = copy.deepcopy(self.start_board)
        self.right_position_update = self.list_postion(self.start_board)

    def list_postion(self,board):
        """ For a given board give all the position that got no number from the start"""
        res = []
        len_square = len(board)
        for i_row in range (0,len_square):
            for i_column in range (0,len_square):
                if(board[i_row][i_column] == 0):
                    res.append([i_row,i_column])
        return res


    def update(self,number,row,column,printer=None):
        """ We can update the board with this method"""
        # Update indicator Printer
        if(printer != None):
            self.printer = printer
        if(self.can_we_update(number,row,column)):
            self.update_board[row][column] = number
            if(self.printer):
                print("The position [" + str(row) + "," + str(column) + "] = " + str(number) + " is Valid")
            

    def can_we_update(self,number,row,column):
        """ This function return a bool who verif if your modification is valid """
        # Exception for 0, it's just for update the interface
        if(self.right_position_update and number == 0):
            return True
        row_square = row - (row % 3) 
        column_square = column - (column % 3) 
        return self.verif_column(number,column) and self.verif_row(number,row) and [row,column] in self.right_position_update and self.verif_square(number,row_square,column_square)
    
    def verif_column(self,number,column):
        """ Verification if the number is already on this column """
        for row in range(0,len(self.update_board)):
            if(self.update_board[row][column] == number):
                if(self.printer):
                    print("Error : verif_column( number = " + str(number) + ", column = " + str(column) + ")" )
                return False
        return True

    def verif_row(self,number,row):
        """ Verification if the number is already on this row """
        for column in range(0,len(self.update_board)):
            if(self.update_board[row][column] == number):
                if(self.printer):
                    print("Error : verif_row( number = " + str(number) + ", row = " + str(row) + ")" )
                return False
        return True
    
    def verif_square(self,number,row,column):
        """ Verification if the number is already in this square, input will be the position of the first number of the square"""
        for i_row in range(row,row+3):
            for i_column in range(column,column+3):
                if(self.update_board[i_row][i_column]== number):
                    if(self.printer):
                        print("Error : verif_square( number = " + str(number) + ", row = " + str(row) + ", column = " + str(column) + ")"  )
                    return False
        return True
    
    def game_is_finish(self):
        """ This function is the boolean that give the state of the game """
        # Check all the rows
        for raw in self.update_board:
            if(len(raw) > len(set(raw))):
                print("Raw Alert : " + str(raw) )
                return False
        array = numpy.array(self.update_board)
        # Check all the columns
        for number_column in range(0,len(self.update_board)):
            if(len(array[:, number_column]) > len(set(array[:, number_column])) ):
                print("Column Alert : " + str(array[:, number_column]))
                return False
        # Check all the squares
        for i_row in [0,3,6]:
            for i_column in [0,3,6]:
                temp = []
                for p_row in range(i_row,i_row+3):
                    for p_column in range(i_column,i_column+3):
                        temp.append(self.update_board[p_row][p_column])
                if(len(temp) > len(set(temp))):
                    print("Square Alert : " + i_row + "," + i_column)
                    return False
        # No more 0 in 
        if(len(self.list_postion(self.update_board)) > 0):
            print("You have to finish this !")
            return False
        return True

    # Optimal parser, made by an expert O~O
    def __repr__(self):
        """ Representation of the actual board game """
        res = []
        caracter = chr(4)
        len_square = len(self.update_board)
        for i_row in range (0,len_square):
            if(i_row == 0):
                for _ in range(0,len_square):
                    res.append(" " + caracter + " " + caracter)
                res.append(" " + caracter + "\n")
            for i_column in range (0,len_square):
                # starter caracter
                if(i_column == 0 ):
                    res.append(" " + caracter + " ")
                # numbers
                res.append(" " + str(self.update_board[i_row][i_column]) + " ")
                # between numbers + end
                if(i_column == 2 or i_column == 5 or i_column == 8):
                    res.append(" " + caracter + " ")
            res.append("\n")
            if(i_row == 2 or i_row == 5 or i_row == 8):
                for _ in range(0,len_square):
                    res.append(" " + caracter + " " + caracter)
                res.append(" " + caracter + "\n")
        return ''.join(res)
