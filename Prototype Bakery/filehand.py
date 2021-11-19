'''
====================================================
                    filehand.py:
 Function storage for all file-handling operations.
====================================================
'''

from os.path import dirname,abspath,exists
from os import mkdir
import sys

def loc(): # Current parent directory path
    return f"{dirname(abspath(__file__))}\\"

def exist(path): # Returns True if path (.txt or folder) exists in current directory
    exist=exists(f"{loc()}{path}")
    return exist

def write(path, text): # Creates or rewrites .txt with text
    handler=open(f"{loc()}{path}",'w')
    handler.write(text)
    handler.close()

def writelines(path, list): # Inject each string with "\n" in list, then rewrites .txt with the lines
    linesList=[]
    for elem in list:
        linesList.append(elem+"\n")
    write(path,f"{''.join(linesList)}")

def append(path, text): # Appends text to .txt
    handler=open(f"{loc()}{path}","a")
    handler.write(text)
    handler.close()

def read(path): # Returns raw list of .txt lines as strings with "\n"
    handler=open(f"{loc()}{path}",'r')
    data=handler.readlines()
    handler.close()
    return data

def mkFolder(directoryName): # Create a directory/folder
    mkdir(f"{loc()}{directoryName}")

def printFile(path,function): # Prints function() into .txt
    original_stdout=sys.stdout
    with open(f"{loc()}{path}",'w') as file:
        sys.stdout = file
        function()
        sys.stdout = original_stdout