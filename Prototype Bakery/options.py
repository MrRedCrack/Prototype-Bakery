'''
options.py:
This is the function storage for general option-handling operations.

For each options prompt with a range of letters or numbers to choose from,
the prompt() function is called.
Returns "Invalid option!" if the option input is out of range, and repeats the prompt until a valid option is entered.

Here also lies the user interface (UI) indentation function: printMod()
Edit the Indent Value to completely change UI indentation.

'''
##UI indentation
indent=10 ##Indent Value
ind=' '*indent
def printMod(string):
    indent
    print(f"{ind}{string}")

##prompt function: Prompts a line, and only lets a valid input through according to inputRange.
def prompt(prompt,inputRange):

    #Define input range as [range]
    if isinstance(inputRange,list):
        range=inputRange
    if isinstance(inputRange,str): #Splits str into individual capitalized letters as list
        range=[char for char in str(inputRange).upper()]

    #Options input and validation stage
    while True:
        err=""
        opt=str(input(ind+prompt)).upper()
        if opt not in range: #Check if input is within [range]
            err="Invalid option!"
        
        #Check if there was error
        if err:
            printMod(f"{err}")
        else:
            break
    
    return opt

