# imports
from colors import *
import os
import getpass
import subprocess
import sys
import shutil
import platform
import psutil
import win32api
import win32file
import socket
from get_nic import getnic
import datetime
# wow that's a lot of imports

processRunning = False
mode = "Lemon"
parameter = None

print("Lemon Terminal ver: 0.2.1")
print("")

while processRunning == False:

    print(color(platform.node() + " | " + getpass.getuser(), fg="cyan"), end=" ")
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

    print()
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
        elif keyWord == "ls": # printing directory contents
            try:
                if parameter == None:
                    dirList = os.listdir(os.getcwd()) # getting list of contents
                else:
                    dirList = os.listdir(command[3:])
            except:
                print(color("Directiry is non existent or permission was denied", fg="red"))

            for file in range(len(dirList)):
                print(dirList[file])

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

        elif keyWord == "tasklist":
            output = os.popen('wmic process get description, processid').read()
            print(output, end="")

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

        elif keyWord == "sysinfo":
            print("Name: " + color(platform.node(), fg="orange"))
            print("Windows Version: " + color(platform.platform(), fg="orange"))
            print("CPU: " + color(platform.processor(), fg="orange"))
            print("Architecture: " + color(platform.machine(), fg="orange"))
            memory = psutil.virtual_memory()
            print("Memory: " + color(round(memory.total / 1000000000, 1), fg="orange"))

        elif keyWord == "type":
            if command[5:] == "":
                print("File not specified")
            else:
                try:
                    file = open(command[5:])

                    for line in file:
                        print(line, end="")
                except:
                    print(color("Could not open file " + file, fg="red"))
                    
        elif keyWord == "info": # prints information about system
            if parameter == "mem": # memory
                 memory = psutil.virtual_memory()
                 print("Total: " + color(round(memory.total / 1000000000, 1), fg="orange"))
                 print()
               
                 print("Used: " + color(round(memory.used / 1000000000, 1), fg="orange")) # calculating used memory
                 print("Free: " + color(round(memory.available / 1000000000, 1), fg="orange"))
            elif parameter == "drive":
                drives = win32api.GetLogicalDriveStrings()
                drives = drives.split('\000')[:-1]
                
                try:
                
                    for drive in drives:
                        print(drive, end=" ")
                        print("info")
                    
                        print("Total: " + color(psutil.disk_usage(drive).total / 1000000000, fg="orange"))
                        print("Used space: " + color(psutil.disk_usage(drive).used / 1000000000, fg="orange"))
                        print("Free space: " + color(psutil.disk_usage(drive).free / 1000000000, fg="orange"))
                    
                        driveTypeInt = win32file.GetDriveType(drive)
                    
                        if driveTypeInt == 2:
                            driveType = "Removable Disk"
                        elif driveTypeInt == 3:
                            driveType = "Local Disk"
                        elif driveTypeInt == 4:
                            driveType = "Network Drive"
                        elif driveTypeInt == 5:
                            driveType = "CD"
                        else:
                            driveType = "Unknown"
                    
                        print("Drive type: " + color(driveType, fg ="orange"))
                        print()
                        
                except PermissionError:
                        print(color("Could not read drive " + drive  + " Drive not ready", fg="red"))
        
            elif parameter == "net":
                print("Name: " + color(socket.gethostname(), fg="orange"))
                print("IP Adress: " + color(socket.gethostbyname(socket.gethostname()), fg="orange"))
                
                print()
                print("NIC Cards")
                

                addrs = psutil.net_if_addrs().keys
                
                for nic in addrs():
                        print(color(nic, fg="orange"))
                
            elif parameter == "power":
                print("Charge: " + color(psutil.sensors_battery().percent, fg="orange"), end="")
                print(color("%", fg="orange"))
                
                if psutil.sensors_battery().power_plugged == False:
                    print("Status: " + color("Using Battery", fg="orange"))
                    
                elif psutil.sensors_battery().power_plugged == True:
                    print("Status: " + color("Plugged in", fg="orange"))

                else:
                    print("Status: " + color("Unknown", fg="orange"))
            
            elif parameter == "cpu":
                print("CPU: " + color(platform.processor(), fg="orange"))
                print("Architecture: " + color(platform.machine(), fg="orange"))
                print("Logical CPU's: " + color(psutil.cpu_count(logical=True), fg="orange"))
                
            
            else:
                print(color("Invalid parameter", fg="red"))
            
        elif keyWord == "time":
            print("The current time is ", end="")
            print(datetime.datetime.now())

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
        
    print()

    processRunning = False
    parameter = None
