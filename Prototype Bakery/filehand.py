'''
filehand.py: filehand stands for File Handler
This is the function storage for all file-handling operations.

'''
##Essential module dumps
import os
import sys

def loc(): #Gets current directory path to be injected into subsequent file-handling functions below
    return f"{os.path.dirname(os.path.abspath(__file__))}\\"

def exist(path): #Boolean that returns True if 'path' exists in current directory, for example 'ing.txt'
    exist=os.path.exists(f"{loc()}{path}")
    return exist

def write(path, text): #Creates or rewrites 'path' file with 'text'
    handler=open(f"{loc()}{path}",'w')
    handler.write(text)
    handler.close()

def writelines(path, list): #Joins each string in list as separate lines injected with "\n", then rewrites 'path' with the lines
    linesList=[]
    for elem in list:
        linesList.append(elem+"\n")
    write(path,f"{''.join(linesList)}")

def append(path, text): #Appends 'text' to 'path' file
    handler=open(f"{loc()}{path}","a")
    handler.write(text)
    handler.close()

def read(path): #Returns raw list of file lines as string elements, including the "\n"s
    handler=open(f"{loc()}{path}",'r')
    data=handler.readlines()
    handler.close()
    return data

def mkdir(directoryName): #Create a directory within current directory
    os.mkdir(f"{loc()}{directoryName}")

def printFile(path,function): #Prints 'function()' into 'path' file
    original_stdout=sys.stdout
    with open(f"{loc()}{path}",'w') as file:
        sys.stdout = file
        function()
        sys.stdout = original_stdout