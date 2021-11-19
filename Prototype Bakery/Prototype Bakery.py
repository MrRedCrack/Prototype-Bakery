'''
===================================================================================================================
                                              Prototype Bakery.py:
                                                     main()
-------------------------------------------------------------------------------------------------------------------
It mainly consists of interface-printing functions and interface-navigating code structure.
Interface-printing functions are divided into different blocks for easy pick and combining in building a new page.
Most operations are saved in and called from xxxOpt.py files, named according to their respective page.

Note:
from options.py import *:
1. Imports prompt() for interface navigations.
2. Every supposedly - print() function is modified and replaced with printMod() for indentation purposes.
3. All {ind} too, found after '\n's are imported for indentation purposes only.
===================================================================================================================
'''

from os import system
from datetime import datetime

from options import *
import ingOpt
import recOpt
import ordOpt
import mrpOpt
import filehand

# # Check and regenerate file if missing
newInventoryFile=False
if not filehand.exist("inv.txt"):
    filehand.write("inv.txt","")
    # Report to Inventory page if the file was regenerated
    newInventoryFile=True 

newRecipeFile=False
if not filehand.exist("rec.txt"):
    filehand.write("rec.txt","")
    # Report to Recipes page if the file was regenerated
    newRecipeFile=True 

if not filehand.exist("recDesc.txt"):
    filehand.write("recDesc.txt","")

if not filehand.exist("orders.txt"):
    filehand.write("orders.txt","")

# # Interface blocks definition
def header(clear): # Called first for every page to clear screen, then print date, time, and bakery name.
    if clear==True:
        system('cls')
    print('')
    printMod(f"{datetime.today().strftime('%Y-%m-%d - %H:%M:%S'):^80}")
    printMod(f"{'Prototype Bakery':^80}")
    printMod(f"{'='*80}")

def mainMenu(): # Main menu page block
    printMod(f"{'Main Menu':^80}")
    printMod("="*80)
    printMod(f" [I]nventory\n{ind} [R]ecipes\n{ind} [O]rder\n{ind} [M]aterial Requirements Plan\n\n{ind} [Q]uit")
    printMod("="*80)

def pageInventory(): # Inventory menu page block
    printMod(f"{'Inventory':^80}")
    global newInventoryFile
    if newInventoryFile==True:
        printMod(f"{'Could not find inv.txt ... A new file was created.':^80}")
        newInventoryFile=False
    printMod("="*80)

    # Read and print ingredients list from inv.txt
    ingListCurrent=filehand.read("inv.txt")
    if ingListCurrent:
        printMod(f"{'Item:':^26}{' Amount:':^24}")
        printMod('-'*80)
        for items in ingListCurrent:
            item=items.strip("\n").split()
            printMod(f"{item[0]:<23}--{float(item[2]):>24.2f} {item[1]}")   
    else:
        printMod(f"{'no ingredients':^80}")

    printMod("="*80)
    printMod("[A]dd [D]elete [E]dit [B]ack")
    printMod("="*80)

def pageRecipe(): # Recipe page block
    printMod(f"{'Recipes':^80}")
    global newRecipeFile
    if newRecipeFile==True:
        printMod(f"{'Could not find rec.txt ... A new file was created.':^80}")
    printMod('='*80)

    # Read from rec.txt
    for recipe in recOpt.getRecipeList():        
        # And print recipe list
        index=recOpt.getRecipeList().index(recipe)+1
        desc=recOpt.getRecDesc(recipe)
        printMod(f"{index}. {recipe:<20} - {desc:<25}")

    printMod("="*80)
    printMod("[A]dd [D]elete [R]ename [V]iew [B]ack")
    printMod("[E]dit description")
    printMod("="*80)

def pageRecDesc(recipeName): # Recipe description block. To be used in ingredients page of recipes
    if recOpt.getRecDesc(recipeName) == '':
        printMod(f"{'No description.':^80}")
    else:
        printMod(f"{recOpt.getRecDesc(recipeName):^80}")
    printMod("="*80)

def pageRecIngredients(recipeNum): # Recipe ingredients block. To be used in ingredients page of recipes
    recipeName=recOpt.getRecipeList()[recipeNum]
    text=f"Ingredients for {recipeName}"
    printMod(f"{text:^80}")
    pageRecDesc(recipeName)

    # Read and print ingredients list from getRecIngredients(recipeName)
    ingListCurrent=recOpt.getRecIngredients(recipeName)
    if ingListCurrent and ingListCurrent[0] != '':
        printMod(f"{'Item:':^26}{' Amount:':^24}")
        printMod("-"*80)
        for items in ingListCurrent:
            item=items.split()
            printMod(f"{item[0]:<23}--{float(item[2]):>24.2f} {item[1]}")
    
    printMod("="*80)
    printMod("[A]dd [D]elete [E]dit [B]ack")
    printMod("="*80)
    return recipeName

def pageOrder(toggleRecipes): # Orders page block

    if toggleRecipes:
        printMod("Recipes available:")
        # Read from rec.txt
        for elem in recOpt.getRecipeList():            
            # And print recipe list
            printMod(f"{recOpt.getRecipeList().index(elem)+1}. {elem:<26}")
        printMod('-'*80)
        print('')

    printMod(f"{'Current Orders':^80}")
    printMod('='*80)
    if not ordOpt.getOrderList():
        printMod(f"{'No orders yet':^80}")
    for i in range(0,len(ordOpt.getOrderList()),2):
        index=int(i/2+1)
        order=ordOpt.getOrderList()[i]
        desc=recOpt.getRecDesc(ordOpt.getOrderList()[i])
        amt=ordOpt.getOrderList()[i+1]
        printMod(f"{index}. {order:<17} - {desc:<23}* {amt:<8}")

    print('')
    printMod("="*80)
    printMod(f"[A]dd [D]elete [E]dit [B]ack \n{ind}[T]oggle recipes [R]eset orders")
    printMod("="*80)

def pageMRP1(): # 1st half of MRP page block
    printMod(f"{'Material Requirements Plan':^80}")
    printMod("="*80)
    if not ordOpt.getOrderList():
        printMod(f"{'no orders - no plan':^80}")
    else:
        # Print orders planned
        printMod("Orders planned >>>")
        for i in range(0,len(ordOpt.getOrderList()),2):
            index=int(i/2+1)
            order=ordOpt.getOrderList()[i]
            desc=recOpt.getRecDesc(ordOpt.getOrderList()[i])
            amt=ordOpt.getOrderList()[i+1]
            printMod(f"{index}. {order:<17} - {desc:<23}* {amt:<8}")
        print('')
        
        # Print ingredients and their shortfalls
        printMod('Ingredients required >>>')
        printMod('-'*80)
        printMod(f"{'Ingredients:':<17}{'Stock:':>18}{'Demand:':>18}{'Shortfall:':>21}")
        printMod('-'*80)
        planList=mrpOpt.ingReqList()
        for elem in planList:
            printMod(f"{elem[0]:<17}{elem[1]:>18}{elem[2]:>18}{elem[3]:>19}{elem[4]:>2}")
        
        print('')

    printMod("="*80)

def pageMRP2(): # 2nd half of MRP page block. Separated to not be included when printing into txt file
    if ordOpt.getOrderList():
        printMod("[S]ave to file  [B]ack")
        printMod("="*80)
   
    else:
        printMod("[B]ack")
        printMod("="*80)

# # main()
# MainMenu
while True:
    header(True)
    mainMenu()
    option=(prompt("Option  >>","QIROM")) # Options prompt with input range Q, I, R, O, M
    
    if option == "Q": # Quit program
        break

    # # IngredientsPage
    if option == "I":
        while True:
            header(True)
            pageInventory()
            option=(prompt("Option  >>","BADE")) 

            if option == "B": # Back
                break

            if option == "A": # Add ingredient
                ingOpt.add(filehand.read("inv.txt"),"inv.txt")

            if option == "D": # Delete ingredient
                ingOpt.delete(filehand.read("inv.txt"),"inv.txt")

            if option == "E": # Edit existing ingredient
                ingOpt.edit(filehand.read("inv.txt"),"inv.txt")

    # # RecipesPage
    if option == "R":
        while True:
            header(True)
            pageRecipe()
            option=(prompt("Option  >>","BVRADE")) 

            if option == "B": # Back
                break

            if option == "V": # View recipe ingredients
                vCancel=False
                while vCancel==False:
                    
                    # Options prompt with input range [number of recipes] and C; choose recipe by number to view its ingredients
                    option=prompt(f"{'Select recipe no.':<20}[C]ancel: ",recOpt.getRecipeOptions())
                    if option == "C": # Cancel recipe selection
                        vCancel=True
                    
                    # # Recipe ingredients page
                    else:
                        while True:
                            header(True)
                            currentRecipeName=pageRecIngredients(int(option)-1)
                            recIngList=recOpt.getRecIngredients(currentRecipeName)
                            optionRecIng=(prompt("Option  >>","ADEB")) 

                            if optionRecIng == "B": # Back, and cancel V selection on previous page
                                vCancel=True
                                break

                            if optionRecIng == "A": # Add ingredient
                                addedIng=ingOpt.add(recIngList,"rec.txt")

                                if addedIng: # (Add if addedIng is not empty, else cancel)
                                    recOpt.rewriteRecipe(currentRecipeName,addedIng)

                            if optionRecIng == "D": # Delete ingredient
                                deletedIng=ingOpt.delete(recIngList,"rec.txt")

                                if deletedIng: 
                                    recOpt.rewriteRecipe(currentRecipeName,deletedIng)

                            if optionRecIng == "E": # Edit ingredient
                                editedIng=ingOpt.edit(recIngList,"rec.txt")

                                if editedIng: 
                                    recOpt.rewriteRecipe(currentRecipeName,editedIng)

            if option == "R": # Rename recipe
                recOpt.rename()

            if option == "A": # Add recipe name
                recOpt.add()

            if option == "D": # Delete recipe
                recOpt.delete()

            if option == "E": # Edit recipe description
                recOpt.description()

    # # OrdersPage
    if option == "O":
        toggleRecipes=True
        while True:
            header(True)            
            pageOrder(toggleRecipes)
            option=(prompt("Option  >>","BTADER")) 

            if option == "B": # Back
                break
            
            if option == "T": # Toggle "Available recipes" view
                toggleRecipes= not toggleRecipes
            
            if option == "A": # Add order from existing recipe:
                ordOpt.add()
            
            if option == "D": # Delete order
                ordOpt.delete()

            if option == "E": # Edit order
                ordOpt.edit()

            if option == "R": # Reset orders
                ordOpt.reset()

    # # MRP page
    if option == "M":
        while True:            
            header(True)
            pageMRP1()
            pageMRP2()
            if not ordOpt.getOrderList(): # Remove the Save option if no orders were made
                addS=''
            else:
                addS='S'
            option=(prompt("Option  >>",f"B{addS}"))

            # Back to menu
            if option == "B": # Back
                break

            if option == "S": # Save to file
                def printMRP(): # Compile required functions to print into .txt file
                    header(False)
                    pageMRP1()
                dirName="Saved Documents" # Folder/directory name, can edit here
                if not filehand.exist(dirName):
                    filehand.mkFolder(dirName)
                fileName=f"MRP {datetime.today().strftime('%Y-%m-%d %H-%M-%S')}.txt" # Text file name, can edit here
                filehand.write(f"{dirName}\\{fileName}","")
                filehand.printFile(f"{dirName}\\{fileName}",printMRP)
                input(f"{ind}Saved as '{fileName}' in folder '{dirName}'\n{ind}Enter to continue.")
