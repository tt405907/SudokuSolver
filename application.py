from windowSudoku import managerWindowSudoku
from unrar import rarfile
import os

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
            interface = managerWindowSudoku("Sudoku",455,500)
            interface.run()
        else:
            print(">> ERROR : There is no sudoku.rar or sudoku.csv, we can't launch the interface")

