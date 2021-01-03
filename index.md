<h1 align="center">Lemon Terminal</h1>

Lemon-Terminal is a custom, easy to use terminal shell for the Windows OS developed by pointThink
 
 It is in it's early stages of development and dosent have many features but for now we have

- Changing modes
- Basic file managment commands
- Basic task managment commands
- System information commands

note: an alternative terminal emulator is recomended

## List of Lemon-Termial commands

- MODE = Changes the terminal mode (cmd, powershell, lemon)
- EXIT = Does exactly what it says
- CD = Changes the current working directory
- LS = Prints the content of the current directory
- REMOVE = Removes a file or directory
- NEWDIR = Creates a new directory
- ENDTASK = Kills a process
- COPY = Copies and pastes files into selected directory
- CLEAR = Clears the screen
- START = starts a process
- SHOWTASKS = Prints running processes
- SYSINFO = Prints information about the computer
- INFO = Prints information about certian system components (mem, power, cpu, drive, net)
- TYPE = Prints contents of a text file
- TIME = Shows date and time

## Building binary from source code
Requierments:
- python 3 (obviously)
- pyinstaller
- ansi colors for python
- wmi
- psutils
- win32api
- shutil

Building:
- Change the directory to the src folder
- Type in this command
``
pyinstaller -F -i icon.ico lemon.py
