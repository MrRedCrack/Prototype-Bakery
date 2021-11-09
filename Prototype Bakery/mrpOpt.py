'''
mrpOpt.py: mrpOpt stands for Material Requirements Plan Options
This is the function storage for the "Material Requirements Plan (MRP)" page.

The function ingReqList() contains the algorithm for calculating and returning a 2D list of required ingredients based on orders made, 
along with their respective information.

Hashtags were placed before certain codes for log feedback during debug. 
Undo them to view the algorithm process during MRP generation.

'''
##Essential module dumps
import filehand
import recOpt
import ordOpt

def unitConversion(amount,amountUnit,targetUnit): #Convert injected amount into the standard g unit for calculation
    if targetUnit=="g":
        if amountUnit=="kg":
            amount=float(amount)*1000
        if amountUnit=="mg":
            amount=float(amount)/1000
    return float(amount)

def ingReqList():
    
    #Get inventory as ingList
    ingListRaw=filehand.read("ing.txt")
    ingList=[]
    for items in ingListRaw:
        item=items.strip("\n").split(" ")
        ingList.extend(item)
#    options.printMod(ingList)
    
    #Get recipe ingredients as recIngList: 'Ingredient name', 'unit', 'amount', 'multiplier' per element
    recIngList=[]
    for counter in range(0,len(ordOpt.getOrderList()),2):
        recIngListElem=recOpt.getRecIngredients(ordOpt.getOrderList()[counter])
        for ingredients in recIngListElem:
            ingredients=ingredients.split()
            recIngList.extend(ingredients)
            recIngList.append(ordOpt.getOrderList()[counter+1])    
#    input(recIngList)

    ##Condensation and multiplication...
    #Condense recIngList into: 'Ingredient name', 'amount in g' per element, combine duplicate ingredients
    condensedRecIngList=[] 
    for counter in range(0,len(recIngList),4):
        ingredientName=recIngList[counter]
        
        #Append ingredient if not in condensedRecIngList
        if ingredientName not in condensedRecIngList:
            condensedRecIngList.append(ingredientName)
            amountInGrams=f"{unitConversion(recIngList[counter+2],recIngList[counter+1],'g')*int(recIngList[counter+3]):.2f}"
            condensedRecIngList.append(amountInGrams)
        else:
            amountInGrams=unitConversion(recIngList[counter+2],recIngList[counter+1],'g')*int(recIngList[counter+3])
            itemIndex=condensedRecIngList.index(ingredientName)
            oldAmount=float(condensedRecIngList[itemIndex+1])
            condensedRecIngList.pop(itemIndex+1)
            condensedRecIngList.insert(itemIndex+1,f"{amountInGrams+oldAmount:.2f}")
#    input(condensedRecIngList)

    #Initiate algorithm
    reqList=[] #[Ingredient name, Stock amount(N/A if none), Demand amount, Shortfall amount(N/A if none), Unit] per element
    for counter in range(0,len(condensedRecIngList),2):
        
        #Ingredient name
        ingName=condensedRecIngList[counter]
        
        #Stock amount
        stockAmount='0'
        if ingName in ingList:
            ingListIndex=ingList.index(ingName)
            stockAmount=f"{unitConversion(ingList[ingListIndex+2],ingList[ingListIndex+1],'g'):.2f}"
        
        #Demand amount
        demandAmount=condensedRecIngList[counter+1]

        #Shortfall amount
        shortfallAmount='N/A'
        if float(demandAmount)>float(stockAmount):
            shortfallAmount=f"{float(demandAmount)-float(stockAmount):.2f}"

        #Convert stock amount to N/A if value stays 0
        if stockAmount=='0':
            stockAmount='N/A'

        #Standard unit: g if there is shortfall, otherwise append blank element as unit
        unit=''
        if shortfallAmount != 'N/A':
            unit='g'
        
        #Append everyone as a list into 2D list: reqList
        reqList.append([ingName,stockAmount,demandAmount,shortfallAmount,unit])
#    input(reqList)
    return reqList #Return 2D list