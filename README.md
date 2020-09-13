# SudokuSolver
Personal project to explore some new technologies (tkinter,backtracking,..)

### Coming soon
- Code cleanup (changing file names, classes and maybe some methods).
- Implementation of a new feature that will allow you to scan a sudoku from your camera.

## How to run this code ?

### Information
In the folder there is a `.rar` file containing 3 million sudoku so don't be surprised if the download takes a few seconds.
Your environment will need a 64-bit python and the version >= 3.7 .

### Clone

Clone the whole directory on your machine, it may take some time depending on the internet speed you have (data inside).

### Setup 

For the execution of this application, we used `unrar` to extract the data contained in the `.rar` file and `numpy`.
So you will have to install this library on your environment, if you use linux could simply install it with : 
```shell
$ pip install unrar
$ pip install numpy
```
If you are on windows, it will be much more complicated:
- First step open your command prompt, with a `cd` put the path of the python script directory you're going to use as below: 
```shell
cd "C:\Users\traco\AppData\Local\Programs\Python\Python37\Scripts"
```
- You will be able to execute the installation command as below: 
```shell
pip install unrar
pip install numpy
```
- You will have to install [https://www.rarlab.com/rar/UnRARDLL.exe](https://www.rarlab.com/rar/UnRARDLL.exe). I follow this guy [guide](https://github.com/matiasb/python-unrar/issues/15).
- After this you will need to add an environment variable to your environment, with the name : `UNRAR_LIB_PATH`and value : `C:\Program Files (x86)\UnrarDLL\x64\UnRAR64.dll`

### Run
- Run the `main.py` file.
