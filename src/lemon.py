# imports
from colors import *
import os
import getpass
import subprocess
import sys

processRunning = False
mode = "Lemon"
parameter = None

print("Lemon Terminal ver: 0.1")
print("")

while processRunning == False:

    print(color(getpass.getuser(), fg="cyan"), end=" ")
    print(color(os.getcwd(), fg="yellow"))

    command = input(color(mode + " > ", fg="green"))

    processRunning = True

    comamand = command.lower()
    keyWord = command.split(" ", 1)[0] # getting first word from string
    try:
        parameter = command.split(" ", 2)[1] #getting second word from string
    except:
        pass

    # general commands
    if command == "exit":
        sys.exit(1)
    elif command == "":
        pass
    elif keyWord == "cd": # changing cwd
        try:
            os.chdir(command[3:])
        except:
            print("Could not change path")
            print("Path is non-existent or permission was denied")

    elif keyWord == "mode": # changing terminal mode
        if parameter == "powershell":
            mode = "Powershell"
        elif parameter == "cmd":
            mode = "Command Prompt"
        elif parameter == "lemon":
            mode = "Lemon"
        else:
            print("Incorrect mode name")

    # mode specific commands
    elif mode == "Lemon":
        if keyWord == "debug":
            print("Mode = " + mode)

        # file managment commands
        elif keyWord == "showdir": # printing directory contents
            if parameter == None:
                print(os.listdir(os.getcwd()))
            else:
                print(os.listdir(command[8:]))

        elif keyWord == "remove": # deleting files
            if command[7:] == "":
                print("Path not specified")
            else:
                try:
                    os.remove(command[7:])
                except FileNotFoundError:
                    print("File not found")
                except:
                    try:
                        os.rmdir(command[7:])
                    except:
                        print("File/Directory is non-existent, permission was denied or directory is not empty")

        elif keyWord == "newdir": # creating directory
            os.mkdir(command[7:])

        elif keyWord == "rename": # renaming directory
            target = command[7:]
            newname = input("Enter new file name: ")
            try:
                os.rename(target, newname)
            except:
                print("Renaming failed. File does not exist or permission was denied")

        # task managment commands
        elif keyWord == "endtask":
            try:
                os.system("taskkill /F /im " + command[8:])
            except:
                print("Failed to kill " + command[8:])

        elif keyWord == "start":
            try:
                subprocess.Popen(command[6:])
            except:
                print("File not found or permission was denied")
        elif keyWord == "clear":
            os.system("cls")
        else:
            try:
                subprocess.Popen(command)
            except:
                print(command + " wasn't found. Executing CMD command instead")
                os.system("cmd /c " + command)

    elif mode == "Command Prompt":
        os.system("cmd /c " + command)

    elif mode == "Powershell":
        os.system("powershell /c " + command)

    processRunning = False
    parameter = None
