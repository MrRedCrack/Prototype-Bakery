'''
============================================================================
                              options.py:
               Function storage for backbone operations.
----------------------------------------------------------------------------
For each prompt when navigating or selecting simple options within menus,
the prompt() function is called.
It filters out invalid input adaptively based on injected input range.

Here also stores the UI indentation function: printMod()
Edit the Indent Value to completely change UI indentation.
============================================================================
'''
# # UI indentation
indent=10 # Indent Value, edit here
ind=' '*indent
def printMod(string):
    indent
    print(f"{ind}{string}")

# # Generic prompt function
def prompt(prompt,inputRange):

    # Initialize range
    if isinstance(inputRange,list):
        range=inputRange
    if isinstance(inputRange,str): 
        # Split string into individual capitalized letters as list
        range=[char for char in str(inputRange).upper()]

    # Input and validation stage
    while True:
        opt=str(input(ind+prompt)).upper()
        if opt not in range:
            printMod("Invalid option!")
        else:
            break
    
    return opt

