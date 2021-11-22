'''
    ============================================================================
                                  options.py:
              Function and variable storage for backbone operations.
    ----------------------------------------------------------------------------
    Edit the Indent Value to completely change UI indentation.

    On each generic prompt for selecting simple options,
    the prompt() function is called.
    It filters out invalid input adaptively based on injected input range.
    ============================================================================
'''

# UI indentation
indent=10 # Indent Value, edit here
ind=' '*indent

def printMod(string):
    print(ind+string)

def inputMod(string):
    return input(ind+string)

# Generic prompt function
def prompt(prompt,inputRange):

    # Initialize range
    if isinstance(inputRange,list):
        range=inputRange
    if isinstance(inputRange,str): 
        # Split string into individual capitalized letters as list
        range=[char for char in str(inputRange).upper()]

    # Input and validation stage
    while True:
        opt=str(inputMod(prompt)).upper()
        if opt not in range:
            printMod(f"Invalid option! Accepted: {', '.join(range)}")
        else:
            break
    
    return opt

# Convert injected amount to targetUnit
def unitConversion(amount,amountUnit,targetUnit): 
    if targetUnit=="g":
        if amountUnit=="kg":
            amount=float(amount)*1000
        if amountUnit=="mg":
            amount=float(amount)/1000
    return float(amount)

# Error dictionary
Err={
    #File error
    'missingInv':'Could not find inv.txt ... A new inv.txt was created.',
    'missingRec':'Could not find rec.txt ... A new rec.txt was created.',
    'missingRecDesc':'Could not find recDesc.txt ... A new recDesc.txt was created.',
    'missingOrd':'Could not find orders.txt ... A new orders.txt was created.',

    # Operation error
    'noSuchName':'Item name not in list.',
    'itemDuplicate':'Duplicate name. Add a different item.',
    'nameDuplicate':'Name already exists!',
    'nameLength':'Too long... Name length must be no more than 15 characters.',
    'nameSpace':'Invalid name. Please use symbols to replace blank spaces.',
    'unit':'Invalid unit. Accepted units are mg/g/kg',
    'amountLarge':'The amount is too large! Accepts no more than 999,999 kg',
    'amountSmall':'Please enter an amount no less than 10 mg',
    'invalidNo':'Invalid number.',
    'invalidInt':'Invalid integer.',
    'descLength':'Too long... Length must be no more than 20 characters.',
    'orderLimit':'Total amount should be more than 0, no more than 1000.'
}
