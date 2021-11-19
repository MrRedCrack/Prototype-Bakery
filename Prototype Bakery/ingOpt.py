'''
========================================================================================
                            ingOpt.py: Ingredient Options
             Function storage for Inventory and Recipe Ingredients page.
----------------------------------------------------------------------------------------
Here stores only the operational functions:
1. Add ingredient
2. Delete ingredient
3. Edit ingredient

Depending on the targetFile, the functions will either... 

directly rewrite inv.txt (inventory ingredients) 

or target rec.txt (recipe ingredients),
returning a list to be reviewed in main() to decide whether to rewrite the rec.txt file.
Only if the returned list is empty when cancelling, rec.txt will not be rewritten.
========================================================================================
'''

import filehand
from options import *
import mrpOpt

def add(ingListCurrent,targetFile): # Add ingredient to ingListCurrent
    cancel=False
    
    # Item name input and validation stage
    while True:
        err=""
        itemName=str.title(input(f"{ind}{'Ingredient name':<20}[C]ancel: "))    
        if itemName.upper() != "C":
            itemDuplicateCheck=[]
            for items in ingListCurrent:
                item=items.strip("\n").split()
                itemDuplicateCheck.append(item[0])
            if itemName in itemDuplicateCheck:
                err="Duplicate name. Add a different item."
            if not itemName or len(itemName) > 15:
                err="Invalid name. Name length must be no more than 15 characters."
            if " " in itemName:
                err="Please use a symbol to replace blank spaces."
        
            if err:
                printMod(err)
            else:
                break
        else:
            cancel=True
            break       
    
    if not cancel:
       
        # Item unit input and validation stage
        while True:
            err=""
            itemUnit=str.lower(input(f"{ind}{'Unit of measure':<20}[C]ancel: "))
            if itemUnit.upper() != "C":
                if itemUnit not in ["g","kg","mg"]:
                    err="Invalid unit. Accepted units are mg/g/kg"
                
                if err:
                    printMod(err)
                else:
                    break
            else:
                cancel=True
                break
        
    if not cancel:
        
        # Item amount input and validation stage
        while True:
            err=""
            itemAmount=str(input(f"{ind}{'Amount':<20}[C]ancel: "))
            if itemAmount.upper() != "C":
                try:
                    if mrpOpt.unitConversion(float(itemAmount),itemUnit,"g") > 999999999:
                        err="The amount is too large! Accepts no more than 999,999 kg"
                    if mrpOpt.unitConversion(float(itemAmount),itemUnit,"g") < 0.01:
                        err="Please enter an amount no less than 10 mg"
                except:
                    err="Invalid Number."
                            
                if err:
                    printMod(err)
                else:
                    break
            else:
                cancel=True
                break
        
    if not cancel:
        
        # Final actions depending on targetFile
        if targetFile == "inv.txt":
            ingListCurrent.append(f"{itemName} {itemUnit} {itemAmount}\n")
            filehand.write("inv.txt",f"{''.join(ingListCurrent)}")
        if targetFile == "rec.txt":
            if '' in ingListCurrent:
                ingListCurrent.remove('')
            ingListCurrent.append(f"{itemName} {itemUnit} {itemAmount}")
            return ingListCurrent
    else:
        return []


def delete(ingListCurrent,targetFile): # Delete ingredient
    cancel=False
    
    # Item name input and validation stage
    while True:
        err=""
        itemName=str.title(input(f"{ind}{'Ingredient name':<20}[C]ancel: "))
        if itemName.upper() != "C":
            itemDuplicateCheck=[]
            for items in ingListCurrent:
                item=items.strip("\n").split()
                itemDuplicateCheck.append(item[0])
            if itemName not in itemDuplicateCheck:
                err="Item name not in list."
        
            if err:
                printMod(err)
            else:
                break
        else:
            cancel=True
            break 
    
    if not cancel:
        
        # Delete ingredient from ingListCurrent
        itemDuplicateCheck=[]
        for items in ingListCurrent:
            item=items.strip("\n").split()
            itemDuplicateCheck.append(item[0])
        for items in itemDuplicateCheck:
            if itemName == items:
                ingListCurrent.remove(ingListCurrent[itemDuplicateCheck.index(items)])

        # Final actions depending on targetFile
        if targetFile == "inv.txt":
            filehand.write("inv.txt",f"{''.join(ingListCurrent)}")
        if targetFile == "rec.txt":
            if not ingListCurrent:
                ingListCurrent.append("")
            return ingListCurrent
        
    else:
        return []

def edit(ingListCurrent,targetFile): # Edit ingredient unit and amount
    cancel=False       
    
    # Item name input and validation stage
    while True:
        err=""
        itemName=str.title(input(f"{ind}{'Ingredient name':<20}[C]ancel: "))    
        if itemName.upper() != "C":
            itemDuplicateCheck=[]
            for items in ingListCurrent:
                item=items.strip("\n").split()
                itemDuplicateCheck.append(item[0])
            if itemName not in itemDuplicateCheck:
                err="Item name not in list."
        
            if err:
                printMod(err)
            else:
                break
        else:
            cancel=True
            break 
    
    if not cancel:
        
        # Item unit input and validation stage
        while True:
            err=""
            itemUnit=str.lower(input(f"{ind}{'Unit of measure':<20}[C]ancel: "))
            if itemUnit.upper() != "C":
                if itemUnit not in ["g","kg","mg"]:
                    err="Invalid unit. Accepted units are mg/g/kg"
                
                if err:
                    printMod(err)
                else:
                    break
            else:
                cancel=True
                break
        
    if not cancel:

        # Item amount input and validation stage        
        while True:
            err=""
            itemAmount=str(input(f"{ind}{'Amount':<20}[C]ancel: "))
            if itemAmount.upper() != "C":
                try:
                    if mrpOpt.unitConversion(float(itemAmount),itemUnit,"g") > 999999999:
                        err="The amount is too large! Accepts no more than 999,999 kg"
                    if mrpOpt.unitConversion(float(itemAmount),itemUnit,"g") < 0.01:
                        err="Please enter an amount no less than 10 mg"
                except:
                    err="Invalid Number."
                            
                if err:
                    printMod(err)
                else:
                    break
            else:
                cancel=True
                break
        
    if not cancel:
        
        # Edit ingListCurrent with new unit and amount
        for items in itemDuplicateCheck:
            if itemName == items:
                ingListCurrent.remove(ingListCurrent[itemDuplicateCheck.index(items)])
                if targetFile == "inv.txt":
                    ingListCurrent.insert(itemDuplicateCheck.index(items),f"{itemName} {itemUnit} {itemAmount}\n")
                if targetFile == "rec.txt":
                    ingListCurrent.insert(itemDuplicateCheck.index(items),f"{itemName} {itemUnit} {itemAmount}")
        
        # Final actions depending on targetFile
        if targetFile == "inv.txt":
            filehand.write("inv.txt",f"{''.join(ingListCurrent)}")
        if targetFile == "rec.txt":
            return ingListCurrent
    else:
        return []
    
