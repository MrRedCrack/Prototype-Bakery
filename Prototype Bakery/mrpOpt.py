'''
======================================================================================================
                          mrpOpt.py: Material Requirements Plan Options
                   Function storage for the Material Requirements Plan page.
------------------------------------------------------------------------------------------------------
ingReqList() contains the algorithm for calculating and returning a 2D list of required ingredients 
based on orders made, along with their respective stock, demand, and shortfall.
======================================================================================================
'''

import filehand
import recOpt
import ordOpt

def unitConversion(amount,amountUnit,targetUnit): # Convert injected amount to targetUnit
    if targetUnit=="g":
        if amountUnit=="kg":
            amount=float(amount)*1000
        if amountUnit=="mg":
            amount=float(amount)/1000
    return float(amount)

def ingReqList():
    
    # Get inventory as ingList
    ingListRaw=filehand.read("inv.txt")
    ingList=[]
    for items in ingListRaw:
        item=items.strip("\n").split()
        ingList.extend(item)
    
    # Get recipe ingredients according to orders as recIngList: 
    # 'Ingredient name', 'unit', 'amount', 'multiplier' appended per ingredient
    recIngList=[]
    for i in range(0,len(ordOpt.getOrderList()),2):
        recIngListElem=recOpt.getRecIngredients(ordOpt.getOrderList()[i])
        for ingredients in recIngListElem:
            ingredients=ingredients.split()
            recIngList.extend(ingredients)
            recIngList.append(ordOpt.getOrderList()[i+1])    

    # # Condensation and multiplication...
    # Condense recIngList into: 'Ingredient name', 'amount' per ingredient, 
    # while combining duplicate ingredients
    condensedRecIngList=[] 
    for i in range(0,len(recIngList),4):
        ingredientName=recIngList[i]
        
        # Append ingredient if not in condensedRecIngList
        if ingredientName not in condensedRecIngList:
            condensedRecIngList.append(ingredientName)
            amountInGrams=f"{unitConversion(recIngList[i+2],recIngList[i+1],'g')*int(recIngList[i+3]):.2f}"
            condensedRecIngList.append(amountInGrams)
        else:
            amountInGrams=unitConversion(recIngList[i+2],recIngList[i+1],'g')*int(recIngList[i+3])
            itemIndex=condensedRecIngList.index(ingredientName)
            oldAmount=float(condensedRecIngList[itemIndex+1])
            condensedRecIngList.pop(itemIndex+1)
            condensedRecIngList.insert(itemIndex+1,f"{amountInGrams+oldAmount:.2f}")

    # Final compilation
    reqList=[] 
    for i in range(0,len(condensedRecIngList),2):
        
        # Ingredient name
        ingName=condensedRecIngList[i]
        
        # Stock amount
        stockAmount='0'
        if ingName in ingList:
            ingListIndex=ingList.index(ingName)
            stockAmount=f"{unitConversion(ingList[ingListIndex+2],ingList[ingListIndex+1],'g'):.2f}"
        
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
    return reqList