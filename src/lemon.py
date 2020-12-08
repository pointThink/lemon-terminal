# imports
from colors import *
import os
import getpass
import subprocess
import sys
import shutil

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
        parameter = command.split(" ", 2)[1] # getting second word from string
        parameter2 = command.split(" ", 3)[2] # getting third word from string
    except:
        try:
            parameter = command.split(" ", 2)[1]
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
            print(color("Could not change path", fg="red"))
            print(color("Path is non-existent or permission was denied", fg="red"))

    elif keyWord == "mode": # changing terminal mode
        if parameter == "powershell":
            mode = "Powershell"
        elif parameter == "cmd":
            mode = "Command Prompt"
        elif parameter == "lemon":
            mode = "Lemon"
        else:
            print(color("Incorrect mode name", fg="red"))

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
                    print(color("File not found", fg="red"))
                except:
                    try:
                        os.rmdir(command[7:])
                    except:
                        print(color("File/Directory is non-existent, permission was denied or directory is not empty", fg="red"))

        elif keyWord == "newdir": # creating directory
            os.mkdir(command[7:])

        elif keyWord == "rename": # renaming directory
            target = command[7:]
            newname = input("Enter new file name: ")
            try:
                os.rename(target, newname)
            except:
                print(color("Renaming failed. File does not exist or permission was denied", fg="red"))

        # task managment commands
        elif keyWord == "endtask": # killing task
            try:
                os.system("taskkill /F /im " + command[8:])

            except:
                print(color("Failed to kill " + command[8:], fg="red"))

        elif keyWord == "showtasks":
            output = os.popen('wmic process get description, processid').read()
            print(output)

        elif keyWord == "start": # starting programs
            try:
                subprocess.Popen(command[6:])
            except:
                print(color("File not found or permission was denied", fg="red"))

        elif keyWord == "clear":
            print(chr(27)+'[2j')
            print('\033c')
            print('\x1bc')

        elif keyWord == "copy":
            path = input("Enter file/directory destination: ")

            try:
                shutil.copyfile(command[5:], path)
            except:
                try:
                    shutil.copytree(command[5:], path + command[5:])

                except:
                    print(color("Failed to copy file", fg="red"))
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
