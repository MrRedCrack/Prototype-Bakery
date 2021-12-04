'''
    =============================================================
                   ingOpt.py: Ingredient Options
     Function storage for Inventory and Recipe Ingredients page.
    -------------------------------------------------------------
    Here stores the operational functions:
    1. Add ingredient
    2. Delete ingredient
    3. Edit ingredient

    Depending on the targetFile, those functions will either... 

    directly rewrite inv.txt (inventory ingredients) 
    or return a list for final actions in recOpt.rewriteRecIng()
    =============================================================
'''

import modules.filehand as filehand
from modules.options import printMod,inputMod,unitConversion,Err

# Name duplicate check
def dup(itemName,ingListCurrent,arg):
    itemDuplicateCheck=[]
    for items in ingListCurrent:
        item=items.strip("\n").split(' ')
        itemDuplicateCheck.append(item[0])
    if arg=='list':
        return itemDuplicateCheck
    elif arg=='check' and (itemName in itemDuplicateCheck):
        return True
    else:
        return False

'''
Operational functions
-----------------------------------------------------------------------------'''
# Add ingredient
def add(ingListCurrent,targetFile):
    cancel=False

    # Item name input and validation stage
    while True:
        err=""
        itemName=str.title(inputMod(f"{'Ingredient name':<20}[C]ancel: "))
        if itemName.upper() != "C":
            if dup(itemName,ingListCurrent,'check'):
                err=Err['itemDuplicate']
            if not itemName or len(itemName) > 15:
                err=Err['nameLength']
            if " " in itemName:
                err=Err['nameSpace']

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
            itemUnit=str.lower(inputMod(f"{'Unit of measure':<20}[C]ancel: "))
            if itemUnit.upper() != "C":
                if itemUnit not in ["g","kg","mg"]:
                    err=Err['unit']

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
            itemAmount=inputMod(f"{'Amount':<20}[C]ancel: ")
            if itemAmount.upper() != "C":
                try:
                    amount=unitConversion(float(itemAmount),itemUnit,"g")
                    if amount > 999999999:
                        err=Err['amountLarge']
                    if amount < 0.01:
                        err=Err['amountSmall']
                except:
                    err=Err['invalidNo']

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
            filehand.write("inv.txt",''.join(sorted(ingListCurrent)))
        elif targetFile == "rec.txt":
            if '' in ingListCurrent:
                ingListCurrent.remove('')
            ingListCurrent.append(f"{itemName} {itemUnit} {itemAmount}")
            return sorted(ingListCurrent)
    else:
        return []

# Delete ingredient
def delete(ingListCurrent,targetFile):
    cancel=False

    # Item name input and validation stage
    while True:
        err=""
        itemName=str.title(inputMod(f"{'Ingredient name':<20}[C]ancel: "))
        if itemName.upper() != "C":
            if not dup(itemName,ingListCurrent,'check'):
                err=Err['noSuchName']

            if err:
                printMod(err)
            else:
                break
        else:
            cancel=True
            break

    if not cancel:

        # Delete ingredient from ingListCurrent
        indexer=dup(itemName,ingListCurrent,'list')
        for items in indexer:
            if itemName == items:
                del ingListCurrent[indexer.index(items)]

        # Final actions depending on targetFile
        if targetFile == "inv.txt":
            filehand.write("inv.txt",''.join(ingListCurrent))
        elif targetFile == "rec.txt":
            if not ingListCurrent:
                ingListCurrent.append("")
            return ingListCurrent

    else:
        return []

# Edit ingredient unit and amount
def edit(ingListCurrent,targetFile):
    cancel=False

    # Item name input and validation stage
    while True:
        err=""
        itemName=str.title(inputMod(f"{'Ingredient name':<20}[C]ancel: "))
        if itemName.upper() != "C":
            if not dup(itemName,ingListCurrent,'check'):
                err=Err['noSuchName']

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
            itemUnit=str.lower(inputMod(f"{'Unit of measure':<20}[C]ancel: "))
            if itemUnit.upper() != "C":
                if itemUnit not in ["g","kg","mg"]:
                    err=Err['unit']

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
            itemAmount=inputMod(f"{'Amount':<20}[C]ancel: ")
            if itemAmount.upper() != "C":
                try:
                    amount=unitConversion(float(itemAmount),itemUnit,"g")
                    if amount > 999999999:
                        err=Err['amountLarge']
                    if amount < 0.01:
                        err=Err['amountSmall']
                except:
                    err=Err['invalidNo']

                if err:
                    printMod(err)
                else:
                    break
            else:
                cancel=True
                break

    if not cancel:

        # Edit ingListCurrent with new unit and amount
        indexer=dup(itemName,ingListCurrent,'list')
        for items in indexer:
            if itemName == items:
                index=indexer.index(items)
                ingListCurrent.remove(ingListCurrent[index])
                if targetFile == "inv.txt":
                    ingListCurrent.insert(index,f"{itemName} {itemUnit} {itemAmount}\n")
                if targetFile == "rec.txt":
                    ingListCurrent.insert(index,f"{itemName} {itemUnit} {itemAmount}")

        # Final actions depending on targetFile
        if targetFile == "inv.txt":
            filehand.write("inv.txt",''.join(sorted(ingListCurrent)))
        elif targetFile == "rec.txt":
            return sorted(ingListCurrent)
    else:
        return []
