'''
recOpt.py: recOpt stands for Recipe Options
This is the function storage for the "Recipes" page.

For there are myriads of information contained within each recipe (recipe, recipe description, recipe ingredients),
a bunch of getXxxXx..() functions were made for receiving different kinds of recipe information for operations.

Below the 'get' functions lies the operational functions for managing recipes:
1. rename recipe
2. add recipe
3. delete recipe
4. description rewrite

The recipe description list is stored in recDesc.txt, 
separately from rec.txt (recipe name, recipe ingredients)
Description-rewrite function automatically deletes the description from recDesc.txt if a blank description is entered.

'''

import filehand
from options import *

def getOrderList(): #Returns a list containing orders information after reading orders.txt; 'OrderName', 'OrderAmount' appended per order to orderList
    orderListRaw=filehand.read("orders.txt")
    orderList=[]
    for elem in orderListRaw:
        elem=elem.strip("\n")
        orderList.append(elem)
    return orderList

def getRecipeOptions(): #Returns a list of ['1','2','3',..,'C'] depending on number of recipes in rec.txt
    numList=[f"{num+1}" for num in range(len(getRecipeList()))]
    numList.append("C")
    return numList

def getRecDescListRaw(): #Returns a list of recipes and their descriptions from reading recDesc.txt; 'recipeName', 'recipeDescription' appended per description
    descriptionListRaw=filehand.read("recDesc.txt")

    descriptionList=[]
    for elem in descriptionListRaw:
        elem=elem.strip("\n")
        descriptionList.append(elem)
    return descriptionList

def getRecDesc(recipeName): #Returns the description str for 'recipeName'. Returns '' if the recipe has no description.

    if recipeName in getRecDescListRaw():
        description=getRecDescListRaw()[getRecDescListRaw().index(recipeName)+1]
        return description
    else:
        return ""

def getRecipeListRaw(): #Returns list: ['recipe1', ['ingredient1', 'unit', 'amount','ingredient2','unit','amount',...] ,'recipe2',['ingredient1','unit','amount',...],...]
    recListCurrent=filehand.read("rec.txt")
    recipeList=[]
    recipeNameList=[]
    for items in recListCurrent:
        recipeInfo=items.strip("\n").split(" ")
        if len(recipeInfo) == 1:
            recipeInfo.append('') #Append 'recipex', '' to final list if recipe does not have ingredients
        recipeName=recipeInfo[0]
        recipeNameList.append(recipeName)
        recipeList.append(recipeName)
        recipeIngredients=recipeInfo[1:]
        recipeList.append(recipeIngredients)
    return recipeList

def getRecipeList(): #Returns list ['recipe1','recipe2','recipe3',...]
    recListCurrent=filehand.read("rec.txt")
    recipeNameList=[]
    for items in recListCurrent:
        recipeInfo=items.strip("\n").split(" ")
        if len(recipeInfo) == 1:
            recipeInfo.append('')
        recipeName=recipeInfo[0].title()
        recipeNameList.append(recipeName)
    return recipeNameList

def getRecIngList(): #Returns a list like getRecipeListRaw(), but without recipe names.
    recListCurrent=filehand.read("rec.txt")
    recIngList=[]
    for items in recListCurrent:
        recipeInfo=items.strip("\n").split(" ")
        if len(recipeInfo) == 1:
            recipeInfo.append('')
        recIngList.append(recipeInfo[1:])
    return recIngList

def getRecIngredients(recipeName): #Returns list ['ingredient1 unit amount', 'ingredient2 unit amount', ...] for 'recipeName'
    recipeList=getRecipeListRaw()
    recipeIngredientRaw=recipeList[recipeList.index(recipeName)+1]        
    recipeIngredientList=[]
    for counter in range(0,len(recipeIngredientRaw),3):
        recipeIngredientSplit=" ".join(recipeIngredientRaw[counter:counter+3])
        recipeIngredientList.append(recipeIngredientSplit)
    return recipeIngredientList

def rewriteRecipe(currentRecipeName,newIngredientList): #Used by main() within recipe ingredients page to rewrite recipe ingredients
    #Replace ingredient list for 'currentRecipeName'
    recipeList=getRecipeListRaw()
    recipeList.pop(recipeList.index(currentRecipeName)+1)
    recipeList.insert(recipeList.index(currentRecipeName)+1,newIngredientList) 
    
    #Rewrite rec.txt with new recipeList
    finalRecipeFile=[]    
    for counter in range(0,len(recipeList),2):
        if recipeList[counter+1] != '': #'' means no ingredients for recipe
            singleRecipe=f"{recipeList[counter]} {' '.join(recipeList[counter+1])}\n"

        #Avoid adding blank spaces after recipe name if the recipe has no ingredients  
        else:
            singleRecipe=f"{recipeList[counter]}\n"
        finalRecipeFile.append(singleRecipe)
   
    filehand.write("rec.txt",f"{''.join(finalRecipeFile)}")


##Operational functions    
def rename(): #Rename recipe
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions()) #Options prompt with input range [number of recipes] and C; choose recipe by number
 
    if select != "C":
        cancel=False
        select=int(select)-1
        #New recipe name input and validation stage
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
            
            #rename recipe in recDesc.txt
            newDescListRaw=getRecDescListRaw()
            if getRecipeList()[select] in newDescListRaw:
                descIndex=newDescListRaw.index(getRecipeList()[select])
                newDescListRaw.pop(descIndex)
                newDescListRaw.insert(descIndex,newName)

                filehand.writelines("recDesc.txt",newDescListRaw)

            #rename recipe in orders.txt
            newOrderListRaw=getOrderList()
            if getRecipeList()[select] in newOrderListRaw:
                orderIndex=newOrderListRaw.index(getRecipeList()[select])
                newOrderListRaw.pop(orderIndex)
                newOrderListRaw.insert(orderIndex,newName)

                filehand.writelines("orders.txt",newOrderListRaw)

            #rename recipe in rec.txt
            tempRecipeList=getRecipeList()
            tempRecipeList.pop(select)
            tempRecipeList.insert(select,newName)
            newRecipeFile=[]
            counter=0
            for elem in tempRecipeList:
                if ''.join(getRecIngredients(getRecipeList()[counter])) != '':
                    newRecipeLine=elem+" "+" ".join(getRecIngredients(getRecipeList()[counter]))+"\n"
                else:
                    newRecipeLine=elem+"\n"
                newRecipeFile.append(newRecipeLine)
                counter+=1
            filehand.write("rec.txt",''.join(newRecipeFile))         

def add(): #Add recipe
    cancel=False

    #New recipe name input and validation stage    
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
    
    #Append recipe name to rec.txt
    if cancel != True:
        filehand.append("rec.txt",f"{newName}\n")

def delete(): #Delete recipe
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions()) #Options prompt with input range [number of recipes] and C; choose recipe by number

    if select != "C":
        select=int(select)-1        
        #delete recipe in recDesc.txt
        if getRecipeList()[select] in getRecDescListRaw():
            newDescListRaw=getRecDescListRaw()
            descIndex=getRecDescListRaw().index(getRecipeList()[select])
            
            newDescListRaw.pop(descIndex)
            newDescListRaw.pop(descIndex)

            filehand.writelines("recDesc.txt",newDescListRaw)            

        #delete recipe in orders.txt
        if getRecipeList()[select] in getOrderList():
            newOrderListRaw=getOrderList()
            orderIndex=getOrderList().index(getRecipeList()[select])
            
            newOrderListRaw.pop(orderIndex)
            newOrderListRaw.pop(orderIndex)

            filehand.writelines("orders.txt",newOrderListRaw)
            
        #delete recipe in rec.txt
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
        
def description(): #Rewrite recipe description
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions()) #Options prompt with input range [number of recipes] and C; choose recipe by number

    if select != "C":
        cancel=False
        select=int(select)-1
        #New description input and validation stage
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
            #Rewrite recipe description
            newDescListRaw=getRecDescListRaw()
            
            #Edit recipe description if an old description existed
            if getRecipeList()[select] in getRecDescListRaw():
                descIndex=getRecDescListRaw().index(getRecipeList()[select])
                
                #Delete description if left blank
                if not newDesc:
                    newDescListRaw.pop(descIndex)
                    newDescListRaw.pop(descIndex)
                #Rewrite description if not blank
                else:
                    newDescListRaw.pop(descIndex+1)
                    newDescListRaw.insert(descIndex+1,newDesc)

            #Just append non-blank recipe description if didn't exist in recDesc.txt
            elif newDesc:
                newDescListRaw.append(getRecipeList()[select])
                newDescListRaw.append(newDesc)

            filehand.writelines("recDesc.txt",newDescListRaw)



