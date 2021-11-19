'''
=======================================================================================================================
                                            recOpt.py: Recipe Options
                                      Function storage for the Recipes page.
-----------------------------------------------------------------------------------------------------------------------
A few getXxxXx..() functions were made to return certain recipe info.

Below the 'get' functions are the operational functions:
1. Rewrite rec.txt
2. Rename recipe
3. Add recipe
4. Delete recipe
5. Rewrite description

The recipe description list is stored in and read from recDesc.txt, 
separately from rec.txt (stores recipe name, recipe ingredients)
=======================================================================================================================
'''

import filehand
from options import *

def getOrderList(): # Returns a list after reading orders.txt; 'OrderName', 'OrderAmount' appended per order to orderList
    orderListRaw=filehand.read("orders.txt")
    orderList=[]
    for elem in orderListRaw:
        elem=elem.strip("\n")
        orderList.append(elem)
    return orderList

def getRecipeOptions(): # Returns a list of ['1','2','3',..,'C'] depending on number of recipes in rec.txt
    numList=[f"{num+1}" for num in range(len(getRecipeList()))]
    numList.append("C")
    return numList

def getRecDescListRaw(): # Returns a list from reading recDesc.txt; 'recipeName', 'recipeDescription' appended per description
    descriptionListRaw=filehand.read("recDesc.txt")

    descriptionList=[]
    for elem in descriptionListRaw:
        elem=elem.strip("\n")
        descriptionList.append(elem)
    return descriptionList

def getRecDesc(recipeName): # Returns the description string for 'recipeName'. Returns '' if the recipe has no description.

    if recipeName in getRecDescListRaw():
        description=getRecDescListRaw()[getRecDescListRaw().index(recipeName)+1]
        return description
    else:
        return ""

def getRecipeListRaw(): # Returns list: ['recipe1', ['ingredient1', 'unit', 'amount',...] ,'recipe2',['ingredient1','unit','amount',...],...]
    recListCurrent=filehand.read("rec.txt")
    recipeList=[]
    recipeNameList=[]
    for items in recListCurrent:
        recipeInfo=items.strip("\n").split()
        if len(recipeInfo) == 1:
            recipeInfo.append('') # Append 'recipex', '' to final list if recipe does not have ingredients
        recipeName=recipeInfo[0]
        recipeNameList.append(recipeName)
        recipeList.append(recipeName)
        recipeIngredients=recipeInfo[1:]
        recipeList.append(recipeIngredients)
    return recipeList

def getRecipeList(): # Returns list ['recipe1','recipe2','recipe3',...]
    recListCurrent=filehand.read("rec.txt")
    recipeNameList=[]
    for items in recListCurrent:
        recipeInfo=items.strip("\n").split()
        if len(recipeInfo) == 1:
            recipeInfo.append('')
        recipeName=recipeInfo[0].title()
        recipeNameList.append(recipeName)
    return recipeNameList

def getRecIngList(): # Returns a list like getRecipeListRaw(), but without recipe names.
    recListCurrent=filehand.read("rec.txt")
    recIngList=[]
    for items in recListCurrent:
        recipeInfo=items.strip("\n").split()
        if len(recipeInfo) == 1:
            recipeInfo.append('')
        recIngList.append(recipeInfo[1:])
    return recIngList

def getRecIngredients(recipeName): # Returns list ['ingredient1 unit amount', 'ingredient2 unit amount', ...] for 'recipeName'
    recipeList=getRecipeListRaw()
    recipeIngredientRaw=recipeList[recipeList.index(recipeName)+1]        
    recipeIngredientList=[]
    for i in range(0,len(recipeIngredientRaw),3):
        recipeIngredientSplit=" ".join(recipeIngredientRaw[i:i+3])
        recipeIngredientList.append(recipeIngredientSplit)
    return recipeIngredientList

# # Operational functions    
def rewriteRecipe(currentRecipeName,newIngredientList): # Used by main() within recipe ingredients page to rewrite recipe ingredients
    # Replace ingredient list for selected recipe
    recipeList=getRecipeListRaw()
    recipeList.pop(recipeList.index(currentRecipeName)+1)
    recipeList.insert(recipeList.index(currentRecipeName)+1,newIngredientList) 
    
    # Rewrite rec.txt with new recipeList
    finalRecipeFile=[]    
    for i in range(0,len(recipeList),2):
        if recipeList[i+1] != '': # '' means no ingredients for recipe
            singleRecipe=f"{recipeList[i]} {' '.join(recipeList[i+1])}\n"

        # Avoid adding blank spaces after recipe name if the recipe has no ingredients  
        else:
            singleRecipe=f"{recipeList[i]}\n"
        finalRecipeFile.append(singleRecipe)
   
    filehand.write("rec.txt",f"{''.join(finalRecipeFile)}")


def rename(): # Rename recipe
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions()) 
 
    if select != "C":
        cancel=False
        select=int(select)-1
        # New recipe name input and validation stage
        while True:
            err=""
            newName=str.title(input(f"{ind}{'New recipe name':<20}[C]ancel: "))
            if not newName or len(newName) > 15:
                err="Invalid name. Name length must be no more than 15 characters."
            if newName in getRecipeList():
                err="Name already exists!"
            if ' ' in newName:
                err="Please use a symbol to replace blank spaces."

            if newName.upper() != "C":
                if err:
                    printMod(err)
                else:
                    break
            else:
                cancel=True
                break
        
        if not cancel:
            
            # Rename recipe in recDesc.txt
            newDescListRaw=getRecDescListRaw()
            if getRecipeList()[select] in newDescListRaw:
                descIndex=newDescListRaw.index(getRecipeList()[select])
                newDescListRaw.pop(descIndex)
                newDescListRaw.insert(descIndex,newName)

                filehand.writelines("recDesc.txt",newDescListRaw)

            # Rename recipe in orders.txt
            newOrderListRaw=getOrderList()
            if getRecipeList()[select] in newOrderListRaw:
                orderIndex=newOrderListRaw.index(getRecipeList()[select])
                newOrderListRaw.pop(orderIndex)
                newOrderListRaw.insert(orderIndex,newName)

                filehand.writelines("orders.txt",newOrderListRaw)

            # Rename recipe in rec.txt
            tempRecipeList=getRecipeList()
            tempRecipeList.pop(select)
            tempRecipeList.insert(select,newName)
            newRecipeFile=[]
            i=0
            for elem in tempRecipeList:
                if ''.join(getRecIngredients(getRecipeList()[i])) != '':
                    newRecipeLine=elem+" "+" ".join(getRecIngredients(getRecipeList()[i]))+"\n"
                else:
                    newRecipeLine=elem+"\n"
                newRecipeFile.append(newRecipeLine)
                i+=1
            filehand.write("rec.txt",''.join(newRecipeFile))         

def add(): # Add recipe
    cancel=False

    # New recipe name input and validation stage    
    while True:
        err=""
        newName=str.title(input(f"{ind}{'New recipe name':<20}[C]ancel: "))
        if not newName or len(newName) > 15:
            err="Invalid name. Name length must be less than 15 characters."
        if newName in getRecipeList():
            err="Name already exists!"
        if ' ' in newName:
            err="Please use a symbol to replace blank spaces."

        if newName.upper() != "C":
            if err:
                printMod(err)
            else:
                break
        else:
            cancel=True
            break
    
    # Append recipe name to rec.txt
    if cancel != True:
        filehand.append("rec.txt",f"{newName}\n")

def delete(): # Delete recipe
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions())

    if select != "C":
        select=int(select)-1        
        # Delete recipe in recDesc.txt
        if getRecipeList()[select] in getRecDescListRaw():
            newDescListRaw=getRecDescListRaw()
            descIndex=getRecDescListRaw().index(getRecipeList()[select])
            
            newDescListRaw.pop(descIndex)
            newDescListRaw.pop(descIndex)

            filehand.writelines("recDesc.txt",newDescListRaw)            

        # Delete recipe in orders.txt
        if getRecipeList()[select] in getOrderList():
            newOrderListRaw=getOrderList()
            orderIndex=getOrderList().index(getRecipeList()[select])
            
            newOrderListRaw.pop(orderIndex)
            newOrderListRaw.pop(orderIndex)

            filehand.writelines("orders.txt",newOrderListRaw)
            
        # Delete recipe in rec.txt
        tempRecipeList=getRecipeList()
        tempRecipeList.pop(select)
        tempIngredientsList=getRecIngList()
        tempIngredientsList.pop(select)
        finalRecipeFile=[]
        for elem in tempRecipeList:
            if ''.join(tempIngredientsList[tempRecipeList.index(elem)]) != '':
                finalRecipeLine=elem+' '+' '.join(tempIngredientsList[tempRecipeList.index(elem)])+"\n"
            else:
                finalRecipeLine=elem+"\n"
            finalRecipeFile.append(finalRecipeLine)
        filehand.write("rec.txt",f"{''.join(finalRecipeFile)}")
        
def description(): # Rewrite recipe description
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions())

    if select != "C":
        cancel=False
        select=int(select)-1
        # New description input and validation stage
        while True:
            err=""
            newDesc=str(input(f"{ind}{'New description (leave blank to delete)':<20}[C]ancel: "))
            if len(newDesc) > 20:
                err="Invalid description. Description length must be no more than 20 characters."
            
            if newDesc.upper() != "C":
                if err:
                    printMod(err)
                else:
                    break
            else:
                cancel=True
                break
      
        if not cancel:
            newDescListRaw=getRecDescListRaw()
            
            # Edit recipe description if an old description existed
            if getRecipeList()[select] in getRecDescListRaw():
                descIndex=getRecDescListRaw().index(getRecipeList()[select])
                
                # Delete description if left blank
                if not newDesc:
                    newDescListRaw.pop(descIndex)
                    newDescListRaw.pop(descIndex)
                # Rewrite description if not blank
                else:
                    newDescListRaw.pop(descIndex+1)
                    newDescListRaw.insert(descIndex+1,newDesc)

            # Append non-blank recipe description if didn't exist in recDesc.txt
            elif newDesc:
                newDescListRaw.append(getRecipeList()[select])
                newDescListRaw.append(newDesc)

            filehand.writelines("recDesc.txt",newDescListRaw)



