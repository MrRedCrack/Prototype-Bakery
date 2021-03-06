'''
    ====================================================
                        filehand.py:
     Function storage for all file-handling operations.
    ====================================================
'''

from os.path import dirname,abspath,exists
from os import mkdir
import sys

# Directory path
def loc(arg=None):
    if arg is None:
        # Current (modules) directory path
        return f"{dirname(abspath(__file__))}\\"
    elif arg=='main':
        # Main program directory path
        return f"{dirname(dirname(abspath(__file__)))}\\"

# Return True if path (.txt or folder) exists in current directory
def exist(path,arg=None):
    exist=exists(f"{loc(arg)}{path}")
    return exist

# Create or rewrite .txt with text
def write(path,text,arg=None):
    with open(f"{loc(arg)}{path}",'w') as file:
        file.write(text)

# Inject each string with "\n" in list, then rewrites .txt with the lines
def writelines(path,list):
    linesList=[]
    for elem in list:
        linesList.append(elem+"\n")
    write(path,"".join(linesList))

# Special rewrite function for rec.txt
def updateRecipes(recipeList):
    finalRecipeFile=[]
    for i in range(0,len(recipeList),2):
        finalRecipeFile.append(recipeList[i])
        ingList=recipeList[i+1]
        if ingList != ['']:
            finalRecipeFile[i//2]+=' '+' '.join(ingList)
    writelines("rec.txt",finalRecipeFile)

# Append text to .txt
def append(path,text):
    with open(f"{loc()}{path}",'a') as file:
        file.write(text)

# Return raw list of .txt lines as strings with "\n"
def read(path):
    with open(f"{loc()}{path}",'r') as file:
        return file.readlines()

# Create a directory/folder
def mkFolder(directoryName,arg=None): 
    mkdir(f"{loc(arg)}{directoryName}")

# Prints f() into .txt
def printFile(path,funcs,arg=None):
    original=sys.stdout
    with open(f"{loc(arg)}{path}",'w') as file:
        sys.stdout=file
        for f in funcs:
            f()
        sys.stdout=original
