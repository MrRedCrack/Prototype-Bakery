'''
    ============================================================
          mrpOpt.py: Material Requirements Plan Options
     Function storage for the Material Requirements Plan page.
    ============================================================
'''

from datetime import datetime

import modules.filehand as filehand
import modules.recOpt as recOpt
import modules.ordOpt as ordOpt
from modules.options import unitConversion,inputMod,printMod

# Ingredients requirement algorithm (1 function)
# Returns 2D list containing required ingredients, stock, demand, and shortfall
def ingReqList():  
    # Get inventory as ingList
    invListRaw=filehand.read("inv.txt")
    invList=[]
    for items in invListRaw:
        item=items.strip("\n").split(' ')
        invList.extend(item)
    
    # Get recipe ingredients according to orders into recIngList: 
    # 'Ingredient name', 'unit', 'amount', 'multiplier' appended per ingredient
    recIngList=[]
    orders=ordOpt.getOrderList()
    for i in range(0,len(orders),2):
        recipe=orders[i]
        multiplier=orders[i+1]
        recIngListElem=recOpt.getRecIngredients(recipe)
        for ingredients in recIngListElem:
            ingredients=ingredients.split(' ')
            if ingredients[0]: # Only extend list if recipe has ingredients
                recIngList.extend(ingredients)
                recIngList.append(multiplier)

    # Condense recIngList into: 'Ingredient name', 'amount' per ingredient, 
    # while combining duplicate ingredients from different recipes
    condensedRecIngList=[] 
    for i in range(0,len(recIngList),4):
        ingredientName=recIngList[i]
        amount=recIngList[i+2]
        unit=recIngList[i+1]
        multiplier=int(recIngList[i+3])
        amountInGrams=unitConversion(amount,unit,'g')*multiplier
        # Append new ingredient
        if ingredientName not in condensedRecIngList:
            condensedRecIngList.append(ingredientName)            
            condensedRecIngList.append(f"{amountInGrams:.2f}")
        else:
            # Update existing ingredient amount
            itemIndex=condensedRecIngList.index(ingredientName)
            oldAmount=float(condensedRecIngList[itemIndex+1])
            total=amountInGrams+oldAmount
            del condensedRecIngList[itemIndex+1]
            condensedRecIngList.insert(itemIndex+1,f"{total:.2f}")

    # Final compilation
    reqList=[] 
    for i in range(0,len(condensedRecIngList),2):
        
        # Ingredient name
        ingName=condensedRecIngList[i]
        
        # Stock amount
        stockAmount='0'
        if ingName in invList:
            ingIndex=invList.index(ingName)
            amount=invList[ingIndex+2]
            unit=invList[ingIndex+1]
            amountInGrams=unitConversion(amount,unit,'g')
            stockAmount=f"{amountInGrams:.2f}"
        
        # Demand amount
        demandAmount=condensedRecIngList[i+1]

        # Shortfall amount
        shortfallAmount='N/A'
        if float(demandAmount)>float(stockAmount):
            shortfallAmount=f"{float(demandAmount)-float(stockAmount):.2f}"

        # Convert stock amount to N/A if value stays 0
        if stockAmount=='0':
            stockAmount='N/A'

        # Standard unit: g if there is shortfall, otherwise append blank element as unit
        unit=''
        if shortfallAmount != 'N/A':
            unit='g'
        
        # Append every element above as a list into 2D list
        reqList.append([ingName,stockAmount,demandAmount,shortfallAmount,unit])
    reqList.sort(key=lambda x:x[0])
    return reqList

# Save to file function
def save(function):
    # Folder/directory name, can edit here
    dirName="Saved Documents" 
    if not filehand.exist(dirName,'main'):
        filehand.mkFolder(dirName,'main')
    # Text file name, can edit here
    fileName=f"MRP {datetime.today().strftime('%Y-%m-%d %H-%M-%S')}.txt"
    if not filehand.exist(f"{dirName}\\{fileName}",'main'): #Edge case
        filehand.printFile(f"{dirName}\\{fileName}",function,'main')
        printMod(f"Saved as '{fileName}' in folder '{dirName}'")
        inputMod(f"Press Enter to continue.")
