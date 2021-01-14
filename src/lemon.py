# TODO: make code less messy
import string
vars = {}

import ctypes
import datetime

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def log(type, string):
    print("[" + "\033[1;32;40m " + str(datetime.datetime.now()) + " \033[m" + "] " + type + ": " + string)

try:
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
    import wmi
    import urllib
    # wow that's a lot of imports
except Exception as exc:
    log("Import Error", str(exc))
    input("Press enter to exit")
    sys.exit(1)

processRunning = False

mode = "Lemon"
version = "0.4.0"

log("Info", "Lemon has been launched succesfully with no errors")
print()

command = "sysinfo"

print("Lemon Terminal version " + version +" |", end=" ")
print(datetime.datetime.now())
print("https://www.github.com/pointThink/lemon-terminal")

while not processRunning:
        

    if command == None:
        print(color(platform.node() + " @ " + getpass.getuser(), fg="cyan"), end=" ") # platform.node = getting computer name | getpass.getuser = getting current user
        print(color(os.getcwd().upper(), fg="yellow"))

        command = input("(" + color(mode, fg="green") + ") ") # command input
    else:
        pass
    
    for key, value in vars.items(): # this replaces the dict key with its contents
        if key in command:
            command = command.replace("*" + key, str(value))


    keyWord = command.split(" ", 1)[0] # getting first word from string
    keyWord = keyWord.lower()
 
    parameters = command.split(" ") # getting parameters from the string
    del parameters[0] # removes the keyword
    
    print()
    processRunning = True
    
    # general commands
    if command == "exit":
        log("Exit", "Exited lemon terminal [Exit by user]")
        sys.exit(1)
    elif command == "":
        pass
    elif keyWord == "cd": # changing cwd
        try:
            os.chdir(command[3:])
        except Exception as e:
            print(color("Could not change path " + str(e), fg="red"))

    elif keyWord == "mode": # changing terminal mode
        if parameters[0] == "powershell":
            mode = "Powershell"
        elif parameters[0] == "cmd":
            mode = "Command Prompt"
        elif parameters[0] == "lemon":
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
                if command[3:] == "":
                    dirList = os.listdir(os.getcwd()) # getting list of content | if directory wasn't specified lemon will use the current working directory
                    dir = os.getcwd() + "/"
                else:
                    dirList = os.listdir(command[3:])
                    dir = command[3:] + "/"
            except Exception as e:
                print(color("Error " + str(e), fg="red"))

            try:
                for file in range(len(dirList)): # using for loop for printing contents beacuse printing lists normally sucks
                    
                        if os.path.isdir(dir + dirList[file]):
                            print("[FOLDER] " + dirList[file])
                    
                        elif os.path.isfile(dir + dirList[file]):
                            print(color("[FILE]   ", fg="green") + dirList[file])
            except:
                pass

        elif keyWord == "remove": # deleting files
            if command[7:] == "":
                print("Path not specified") # Lemon will throw an error if path was not specified
            else:
                try: # lemon will try to remove a file at first
                    os.remove(command[7:])
                except FileNotFoundError:
                    print(color("File not found", fg="red"))
                except: # if it fails it will instead try to remove a directory
                    try:
                        os.rmdir(command[7:])
                    except Exception as e:
                        print(color("Error " + str(e), fg="red"))

        elif keyWord == "newdir": # creating directory
            try:
                os.mkdir(command[7:])
            except:
                print("error")

        elif keyWord == "rename": # renaming directory
            target = command[7:]
            newname = input("Enter new file name: ")
            try:
                os.rename(target, newname)
            except Exception as e:
                print(color("Error " + str(e), fg="red"))

        # task managment commands
        elif keyWord == "endtask": # killing task
            ti = 0
            
            f = wmi.WMI()
            name = parameters[0]
            
            for process in f.Win32_Process():
                if process.name == name:
                    process.Terminate()
                    
                    print(color("SUCESS The process has been terminated", fg="green"))
                    ti += 1
                    
                else:
                    try: # this try except is here to prevent from index out of range error
                        if parameters[1] == "debug":
                            print(color("Names dont match. No process terminated", fg="red"))
                    except:
                        pass
                
            if ti == 0:
                print()
                print(color("Process " + name + " not found", fg="red"))


           # except:
              #  print(color("Failed to kill " + command[8:], fg="red")) # throwing an error if killing task failed

        elif keyWord == "tasklist":
            output = os.popen('wmic process get description, processid').read() # copied from stack overflow (i have no idea how it works cuz i didin't write it)
            print(output)

        elif keyWord == "start": # starting programs
            try:
                subprocess.Popen(command[6:])
            except:
                print(color("File not found or permission was denied", fg="red"))

        elif keyWord == "clear": # cleaaring the screen using ansi symbols
            print(chr(27)+'[2j')
            print('\033c')
            print('\x1bc')

        elif keyWord == "copy":
            path = input("Enter file/directory destination: ")

            try: # At first lemon tries to copy a file
                shutil.copyfile(command[5:], path)
            except:
                try: # if that fails then it tries to copy a directory
                    shutil.copytree(command[5:], path + command[5:])

                except: # if that also fails it throws a very vauge error. Figure it out yourself
                    print(color("Failed to copy file", fg="red"))

        elif keyWord == "sysinfo":
            print("Name: " + color(platform.node(), fg="orange")) # prints computer name
            print("Windows Version: " + color(platform.platform(), fg="orange")) # prints current windows version
            print("CPU: " + color(platform.processor(), fg="orange")) # showing the processor "name"
            print("Architecture: " + color(platform.machine(), fg="orange")) # showing the architecture/machine type
            memory = psutil.virtual_memory() # getting the memory amount
            print("Memory: " + color(round(memory.total / 1000000000, 1), fg="orange")) # converting memory amount to gbs and rounding it

        elif keyWord == "type":
            if command[5:] == "":
                print("File not specified")
            else:
                try: # attempting to open specified file
                    file = open(command[5:])

                    for line in file:
                        print(line, end="")
                except: # if it fails lemon throws an error
                    print(color("Could not open file " + file, fg="red"))
                    
        elif keyWord == "info": # prints information about system
            try:

                if parameters[0] == "mem": # memory
                    memory = psutil.virtual_memory()
                    print("Total: " + color(round(memory.total / 1000000000, 1), fg="orange")) # getting total available memory and rounding it
                    print()
               
                    print("Used: " + color(round(memory.used / 1000000000, 1), fg="orange")) # getting currently used memory and rounding it
                    print("Free: " + color(round(memory.available / 1000000000, 1), fg="orange")) # getting currently available memory and rounding it
                 
                elif parameters[0] == "drive":
                    drives = win32api.GetLogicalDriveStrings() # getting list of available drive
                    drives = drives.split('\000')[:-1]
                
                    try:
                
                        for drive in drives:
                            print(drive, end=" ")
                            print("info")
                    
                            print("Total: " + color(psutil.disk_usage(drive).total / 1000000000, fg="orange")) # printing total space on drive
                            print("Used space: " + color(psutil.disk_usage(drive).used / 1000000000, fg="orange")) # printing used space on drive
                            print("Free space: " + color(psutil.disk_usage(drive).free / 1000000000, fg="orange")) # printing available space on drive
                    
                            driveTypeInt = win32file.GetDriveType(drive) # getting the drive type id
                    
                            if driveTypeInt == 2: # figuring out drive type from id
                                driveType = "Removable Disk"
                            elif driveTypeInt == 3:
                                driveType = "Local Disk"
                            elif driveTypeInt == 4:
                                driveType = "Network Drive"
                            elif driveTypeInt == 5:
                                driveType = "CD"
                            else:
                                driveType = "Unknown"
                    
                            print("Drive type: " + color(driveType, fg ="orange")) # printing the found drive type
                            print()
                        
                    except PermissionError: # The "drive not ready" error is identified as "PermissionError" this may cause problems in some specific scenarios
                        print(color("Could not read drive information Drive not ready", fg="red"))
                    except: 
                        print(color("Unknown Error", fg="red"))
        
                elif parameters[0] == "net":
                    print("Name: " + color(socket.gethostname(), fg="orange")) # getting computer name
                    print("IP Adress: " + color(socket.gethostbyname(socket.gethostname()), fg="orange"))  # getting computer ip adress
                
                    print()
                    print("NIC Cards")
                

                    addrs = psutil.net_if_addrs().keys # getting nic cards
                
                    for nic in addrs():
                        print(color(nic, fg="orange"))
                
                elif parameters[0] == "power":
                    print("Charge: " + color(psutil.sensors_battery().percent, fg="orange"), end="") # printing charge percentage
                    print(color("%", fg="orange"))
                
                    if psutil.sensors_battery().power_plugged == False:  # printing power status
                        print("Status: " + color("Using Battery", fg="orange"))
                    
                    elif psutil.sensors_battery().power_plugged == True:
                        print("Status: " + color("Plugged in", fg="orange"))

                    else:
                        print("Status: " + color("Unknown", fg="orange"))
            
                elif parameters[0] == "cpu":
                    print("CPU: " + color(platform.processor(), fg="orange")) # printing processor namee
                    print("Architecture: " + color(platform.machine(), fg="orange")) # printing architectur
                    print("Logical CPU's: " + color(psutil.cpu_count(logical=True), fg="orange")) # printing logical cpu count
            
                elif parameters[0] == "term": # prints information about terminal
                    print("Lemon-Terminal version " + version)
                    print("Written and maintained by pointThink")
                    print("Project website lemon-terminal.atwebpages.com")
                
            
                else:
                    print(color("Invalid parameter", fg="red"))
            except:
                print(color("Invalid parameter", fg="red"))
            
        elif keyWord == "time": # printing time and date
            print("The current time is ", end="")
            print(datetime.datetime.now())
            
        elif keyWord == "netstatus":
            ip = socket.gethostbyname(socket.gethostname()) # getting ip adress
            
            if ip == "127.0.0.1":
                print("No internet connection")
                
            else:
                print("Connected")
                
        elif keyWord == "log":
            try:
                log(command.split('"')[1], command.split('"')[3])
            except Exception as e:
                print(color("Error " + str(e), fg="red"))
            
        elif keyWord == "pyexec":
            try:
                exec(command[7:])
            except Exception as e:
                print(e)
                
        elif keyWord == "var":
            try:
                length = len(keyWord + "" + parameters[0] + " " + parameters[1] + "  ")
                
                if parameters[0] == "string":
                    vars[parameters[1]] = command.split('=')[1].lstrip().rstrip()
                elif parameters[0] == "int":
                    vars[parameters[1]] = eval(command.split('=')[1])
                elif parameters[0] == "output":
                    
                    if command.split('=')[1].lstrip().rstrip() == "input_read":
                         vars[parameters[1]] = input()
                        
                else:
                    print("Invalid var type")
            except Exception as e:
                print(color("Error: "+ str(e), fg="red"))
                
        elif keyWord == "echo":
            try:
                string = command.split('"')[1]
                print(string)
            except Exception as e:
                print(color("Error: "+ str(e), fg="red"))
                
        elif keyWord == "ice":
            print("ICE - Internal Code Executor")
            print("Anything you write here will be executed as python code")
            print()
            
            code = sys.stdin.readlines()
            joinedCode = "\n".join(code)
            
            try:
                print()
                exec(joinedCode)
            except Exception as e:
                print(e)

        else: # if no matching command was found it will try to execute a program
            try:
                subprocess.call(command)
            except: # if that fails lemon will throw an error
                print(color(command + " isn't a command or executable file", fg="red"))

    elif mode == "Command Prompt":
        os.system("cmd /c " + command)

    elif mode == "Powershell":
        os.system("powershell /c " + command)
        

    parameters = None
    processRunning = False
    command = None

    print()
