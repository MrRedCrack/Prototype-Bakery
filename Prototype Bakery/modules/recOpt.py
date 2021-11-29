'''
    =====================================================================
                        recOpt.py: Recipe Options
                Function storage for the Recipes page.
    ---------------------------------------------------------------------
    A few getXxxXx..() functions were made to return certain recipe info.

    Below the 'get' functions are the operational functions:
    1. Rewrite recipe ingredients
    2. Rename recipe
    3. Add recipe
    4. Delete recipe
    5. Rewrite description

    The recipe description list is stored in and read from recDesc.txt,
    separately from rec.txt (stores recipe name, recipe ingredients)
    =====================================================================
'''

import modules.filehand as filehand
from modules.options import prompt,printMod,inputMod,ind,Err
import modules.ingOpt as ingOpt

# Returns a list after reading orders.txt;
# 'OrderName', 'OrderAmount' appended per order to orderList
# Used for editing recipe names in orders.txt
def getOrderList():
    orderListRaw=filehand.read("orders.txt")
    orderList=[]
    for elem in orderListRaw:
        elem=elem.strip("\n")
        orderList.append(elem)
    return orderList

# Returns a list from reading recDesc.txt;
# 'recipeName', 'recipeDescription' appended per description
def getRecDescListRaw():
    descriptionListRaw=filehand.read("recDesc.txt")
    descriptionList=[]
    for elem in descriptionListRaw:
        elem=elem.strip("\n")
        descriptionList.append(elem)
    return descriptionList

# Returns the description string for 'recipeName'.
# Returns '' if the recipe has no description.
def getRecDesc(recipeName):
    if recipeName in getRecDescListRaw():
        descriptionIndex=getRecDescListRaw().index(recipeName)+1
        description=getRecDescListRaw()[descriptionIndex]
        return description
    else:
        return ""

# Returns list: ['recipe1', ['ingredient1', 'unit', 'amount',...],recipe2,[...],...]
def getRecipeListRaw():
    recListCurrent=filehand.read("rec.txt")
    recipeList=[]
    recipeNameList=[]
    for items in recListCurrent:
        recipeInfo=items.strip("\n").split(' ')
        if len(recipeInfo) == 1:
            recipeInfo.append('') # Append '' if the recipe does not have ingredients
        recipeName=recipeInfo[0]
        recipeNameList.append(recipeName)
        recipeList.append(recipeName)
        recipeIngredients=recipeInfo[1:]
        recipeList.append(recipeIngredients)
    return recipeList

# Returns list ['recipe1','recipe2','recipe3',...]
def getRecipeList():
    recipeNameList=filter(lambda x: isinstance(x,str),getRecipeListRaw())
    return list(recipeNameList)

# Returns a list of ['1','2','3',..,'C']
# depending on number of recipes in rec.txt
def getRecipeOptions():
    recipeNo=len(getRecipeList())
    numList=[f"{num+1}" for num in range(recipeNo)]
    numList.append("C")
    return numList

# Returns a list like getRecipeListRaw(), but without recipe names.
def getRecIngList():
    recIngList=filter(lambda x: isinstance(x,list),getRecipeListRaw())
    return list(recIngList)

# Returns list ['ingredient1 unit amount', 'ingredient2 unit amount', ...] for one recipe
def getRecIngredients(recipeName):
    recipeIndex=getRecipeList().index(recipeName)
    recipeIngredientRaw=getRecIngList()[recipeIndex]
    recipeIngredientList=[]
    for i in range(0,len(recipeIngredientRaw),3):
        recipeIngredientSplit=" ".join(recipeIngredientRaw[i:i+3])
        recipeIngredientList.append(recipeIngredientSplit)
    return recipeIngredientList

'''
Operational functions
-------------------------------------------------------------------------------------'''
# Rewrite recipe ingredients
def rewriteRecIng(currentRecipeName,action):
    recIngList=getRecIngredients(currentRecipeName)
    if action=='A':
        ingRewrite=ingOpt.add(recIngList,"rec.txt")
    elif action=='D':
        ingRewrite=ingOpt.delete(recIngList,"rec.txt")
    elif action=='E':
        ingRewrite=ingOpt.edit(recIngList,"rec.txt")
    if ingRewrite:
        # Replace ingredient list for selected recipe
        recipeList=getRecipeListRaw()
        ingredientsIndex=recipeList.index(currentRecipeName)+1
        del recipeList[ingredientsIndex]
        recipeList.insert(ingredientsIndex,ingRewrite)
        filehand.updateRecipes(recipeList)
        # Rewrite rec.txt with new recipeList

# Rename recipe
def rename():
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions())

    if select != "C":
        cancel=False
        select=int(select)-1
        selectedRec=getRecipeList()[select]
        # New recipe name input and validation stage
        while True:
            err=""
            newName=str.title(inputMod(f"{'New recipe name':<20}[C]ancel: "))
            if not newName or len(newName) > 15:
                err=Err['nameLength']
            if newName in getRecipeList():
                err=Err['nameDuplicate']
            if ' ' in newName:
                err=Err['nameSpace']

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
            descListRaw=getRecDescListRaw()
            if selectedRec in descListRaw:
                descIndex=descListRaw.index(selectedRec)
                del descListRaw[descIndex]
                descListRaw.insert(descIndex,newName)
                filehand.writelines("recDesc.txt",descListRaw)

            # Rename recipe in orders.txt
            orderListRaw=getOrderList()
            if selectedRec in orderListRaw:
                orderIndex=orderListRaw.index(selectedRec)
                del orderListRaw[orderIndex]
                orderListRaw.insert(orderIndex,newName)
                filehand.writelines("orders.txt",orderListRaw)

            # Rename recipe in rec.txt
            recipeList=getRecipeListRaw()
            del recipeList[select*2]
            recipeList.insert(select*2,newName)
            filehand.updateRecipes(recipeList)

# Add recipe
def add():
    cancel=False

    # New recipe name input and validation stage
    while True:
        err=""
        newName=str.title(inputMod(f"{'New recipe name':<20}[C]ancel: "))
        if not newName or len(newName) > 15:
            err=Err['nameLength']
        if newName in getRecipeList():
            err=Err['nameDuplicate']
        if ' ' in newName:
            err=Err['nameSpace']

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

# Delete recipe
def delete():
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions())

    if select != "C":
        select=int(select)-1        
        selectedRec=getRecipeList()[select]
        # Delete recipe in recDesc.txt
        if selectedRec in getRecDescListRaw():
            descListRaw=getRecDescListRaw()
            descIndex=getRecDescListRaw().index(selectedRec)
            del descListRaw[descIndex:descIndex+2]
            filehand.writelines("recDesc.txt",descListRaw)

        # Delete recipe in orders.txt
        if selectedRec in getOrderList():
            orderListRaw=getOrderList()
            orderIndex=getOrderList().index(selectedRec)
            del orderListRaw[orderIndex:orderIndex+2]
            filehand.writelines("orders.txt",orderListRaw)

        # Delete recipe in rec.txt
        recipeList=getRecipeListRaw()
        del recipeList[select*2:select*2+2]
        filehand.updateRecipes(recipeList)

# Rewrite recipe description
def description():
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions())

    if select != "C":
        cancel=False
        select=int(select)-1
        # New description input and validation stage
        while True:
            err=""
            newDesc=inputMod(f"New description (leave blank to delete)\n{ind}[C]ancel: ")
            if len(newDesc) > 20:
                err=Err['descLength']

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
            recipe=getRecipeList()[select]
            # Edit recipe description if an old description existed
            if recipe in getRecDescListRaw():
                descIndex=getRecDescListRaw().index(recipe)

                # Delete description if left blank
                if not newDesc:
                    del newDescListRaw[descIndex:descIndex+2]

                # Rewrite description if not blank
                else:
                    del newDescListRaw[descIndex+1]
                    newDescListRaw.insert(descIndex+1,newDesc)

            # Append non-blank recipe description if didn't exist in recDesc.txt
            elif newDesc:
                newDescListRaw.append(recipe)
                newDescListRaw.append(newDesc)
            filehand.writelines("recDesc.txt",newDescListRaw)
