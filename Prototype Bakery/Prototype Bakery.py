'''
    ================================================================================
                                Prototype Bakery.py:
                                       main()
    --------------------------------------------------------------------------------
    Mainly consists of interface-printing functions 
    and interface-navigating code structure.
    Interface-printing functions are divided into blocks for easy pick and choose.
    Most operations are saved in and called from xxxOpt.py files, 
    named according to their respective page.
    ================================================================================
'''

from os import system
from datetime import datetime
from functools import partial

from modules.options import prompt,printMod,Err
import modules.ingOpt as ingOpt
import modules.recOpt as recOpt
import modules.ordOpt as ordOpt
import modules.mrpOpt as mrpOpt
import modules.filehand as filehand

# Check and regenerate file if missing
newInv,newRec,newDesc,newOrd=['']*4 # Error keys
if not filehand.exist("inv.txt"):
    filehand.write("inv.txt","")
    newInv='missingInv'
if not filehand.exist("rec.txt"):
    filehand.write("rec.txt","")
    newRec='missingRec'
if not filehand.exist("recDesc.txt"):
    filehand.write("recDesc.txt","")
    newDesc='missingRecDesc'
if not filehand.exist("orders.txt"):
    filehand.write("orders.txt","")
    newOrd='missingOrd'

'''
Interface blocks
----------------------------------------------------------------------'''
# Called first for every page to clear screen, then print header
def header(clear):
    if clear:
        system('cls')
    print('')
    printMod(f"{datetime.today().strftime('%Y-%m-%d - %H:%M:%S'):^80}")
    printMod(f"{'Prototype Bakery':^80}")
    printMod(f"{'='*80}")

# Main menu
def pageMain():
    errKey=[newInv,newRec,newDesc,newOrd]
    if any(errKey):
        printMod(f"{'File(s) missing:':^80}")
        for k in errKey:
            if k:
                printMod(f"{Err[k]:^80}")
        printMod("="*80)
    printMod(f"{'Main Menu':^80}")
    printMod("="*80)
    printMod("[I]nventory")
    printMod("[R]ecipes")
    printMod("[O]rders")
    printMod("[M]aterial Requirements Plan")
    print('')
    printMod("[Q]uit")
    printMod("="*80)

# Ingredients block
def pageIngredients(ingListCurrent):
    if ingListCurrent and ingListCurrent[0] != '':
        printMod(f"{'Item:':^26}{' Amount:':^24}")
        printMod('-'*80)
        for elem in ingListCurrent:
            item=elem.strip("\n").split()
            ing,amt,unit=item[0],float(item[2]),item[1]
            printMod(f"{ing:<23}--{amt:>24.2f} {unit}")
    else:
        printMod(f"{'no ingredients':^80}")
    printMod("="*80)
    printMod("[A]dd [D]elete [E]dit [B]ack")
    printMod("="*80)

# Inventory
def pageInventory():
    printMod(f"{'Inventory':^80}")
    printMod("="*80)
    pageIngredients(filehand.read("inv.txt"))

# Recipe
def pageRecipe(): 
    printMod(f"{'Recipes':^80}")
    printMod('='*80)
    for i,recipe in enumerate(recOpt.getRecipeList(),1):
        desc=recOpt.getRecDesc(recipe)
        printMod(f"{i}. {recipe:<20} - {desc:<25}")
    printMod("="*80)
    printMod("[A]dd [D]elete [R]ename [V]iew [B]ack")
    printMod("[E]dit description")
    printMod("="*80)

# Recipe ingredients
def pageRecIngredients(recipeNum):
    recipeName=recOpt.getRecipeList()[recipeNum]
    text=f"Ingredients for {recipeName}"
    printMod(f"{text:^80}")
    desc=recOpt.getRecDesc(recipeName)
    if  desc=='':
        printMod(f"{'No description.':^80}")
    else:
        printMod(f"{desc:^80}")
    printMod("="*80)
    pageIngredients(recOpt.getRecIngredients(recipeName))
    return recipeName

# Orders
def pageOrder(toggleRecipes):
    # Toggleable recipes
    if toggleRecipes:
        printMod("Recipes available:")
        for recipe in recOpt.getRecipeList():            
            recipeIndex=recOpt.getRecipeList().index(recipe)+1
            printMod(f"{recipeIndex}. {recipe:<26}")
        printMod('-'*80)
        print('')

    # Orders
    printMod(f"{'Current Orders':^80}")
    printMod('='*80)
    if not ordOpt.getOrderList():
        printMod(f"{'No orders yet':^80}")
    for i in range(0,len(ordOpt.getOrderList()),2):
        index=i//2+1
        order=ordOpt.getOrderList()[i]
        desc=recOpt.getRecDesc(order)
        amount=ordOpt.getOrderList()[i+1]
        printMod(f"{index}. {order:<17} - {desc:<23}* {amount:<8}")
    print('')
    printMod("="*80)
    printMod("[A]dd [D]elete [E]dit [B]ack")
    printMod("[T]oggle recipes [R]eset orders")
    printMod("="*80)

# 1st half of MRP
def pageMRP1():
    printMod(f"{'Material Requirements Plan':^80}")
    printMod("="*80)
    if not ordOpt.getOrderList():
        printMod(f"{'no orders - no plan':^80}")
    else:
        # Print orders planned
        printMod("Orders planned >>>")
        for i in range(0,len(ordOpt.getOrderList()),2):
            index=i//2+1
            order=ordOpt.getOrderList()[i]
            desc=recOpt.getRecDesc(order)
            amount=ordOpt.getOrderList()[i+1]
            printMod(f"{index}. {order:<17} - {desc:<23}* {amount:<8}")
        print('')

        # Print ingredients and their shortfalls
        printMod('Ingredients required >>>')
        printMod('-'*80)
        printMod(f"{'Ingredients:':<17}{'Stock:':>18}{'Demand:':>18}{'Shortfall:':>21}")
        printMod('-'*80)
        planList=mrpOpt.ingReqList()
        for elemList in planList:
            ingredient,stock,demand,shortfall,unit=elemList
            printMod(f"{ingredient:<17}{stock:>18}{demand:>18}{shortfall:>19}{unit:>2}")
        print('')
    printMod("="*80)

# 2nd half of MRP. Separated to exclude from saved file
def pageMRP2():
    if ordOpt.getOrderList():
        printMod("[S]ave to file  [B]ack")
        printMod("="*80)
    else:
        printMod("[B]ack")
        printMod("="*80)

'''
Menu structures
----------------------------------------------------------------------'''
# Inventory menu
def menuInv():
    while True:
        header(True)
        pageInventory()
        ingListCurrent=filehand.read("inv.txt")
        option=prompt("Option  >>","adeb")

        if option == "B": # Back
            break
        
        elif option == "A": # Add ingredient
            ingOpt.add(ingListCurrent,"inv.txt")

        elif option == "D": # Delete ingredient
            ingOpt.delete(ingListCurrent,"inv.txt")

        elif option == "E": # Edit existing ingredient
            ingOpt.edit(ingListCurrent,"inv.txt")

# Recipe ingredients menu
def menuRecIng():
    # Options prompt with input range [number of recipes] and C;
    # choose recipe by number to view ingredients
    option=prompt(f"{'Select recipe no.':<20}[C]ancel: ",
                    recOpt.getRecipeOptions())

    if option!="C":
        # Recipe ingredients page
        option=int(option)-1
        while True:
            header(True)
            currentRecipeName=pageRecIngredients(option)
            optionRecIng=prompt("Option  >>","adeb")

            if optionRecIng == "B": # Back
                break

            elif optionRecIng == "A": # Add ingredient
                recOpt.rewriteRecIng(currentRecipeName,'A')

            elif optionRecIng == "D": # Delete ingredient
                recOpt.rewriteRecIng(currentRecipeName,'D')

            elif optionRecIng == "E": # Edit ingredient
                recOpt.rewriteRecIng(currentRecipeName,'E')

#Recipe menu
def menuRec():
    while True:
        header(True)
        pageRecipe()
        option=prompt("Option  >>","adrvbe")

        if option == "B": # Back
            break

        elif option == "V": # View recipe ingredients
            menuRecIng()

        elif option == "R": # Rename recipe
            recOpt.rename()

        elif option == "A": # Add recipe name
            recOpt.add()

        elif option == "D": # Delete recipe
            recOpt.delete()

        elif option == "E": # Edit recipe description
            recOpt.description()

# Orders menu
def menuOrd():
    toggleRecipes=True
    while True:
        header(True)
        pageOrder(toggleRecipes)
        option=prompt("Option  >>","adebtr")

        if option == "B": # Back
            break

        elif option == "T": # Toggle "Available recipes" view
            toggleRecipes=not toggleRecipes

        elif option == "A": # Add order from existing recipe:
            ordOpt.add()

        elif option == "D": # Delete order
            ordOpt.delete()

        elif option == "E": # Edit order
            ordOpt.edit()

        elif option == "R": # Reset orders
            ordOpt.reset()

# MRP menu
def menuMRP():
    while True:
        header(True)
        pageMRP1()
        pageMRP2()
        if ordOpt.getOrderList():
            addS='s'
        else: # Remove the Save option if no orders were made
            addS=''
        option=prompt("Option  >>",f"{addS}b")

        # Back to menu
        if option == "B": # Back
            break

        elif option == "S": # Save to file
            mrpOpt.save(partial(header,False),pageMRP1)

'''
main()
---------------------------------------------------------------------------------------'''
# Main menu
while True:
    header(True)
    pageMain()
    # Options prompt with input range I, R, O, M, Q
    option=prompt("Option  >>","iromq")

    if option == "Q": # Quit program
        break

    # Inventory page
    elif option == "I":
        menuInv()

    # Recipes page
    elif option == "R":
        menuRec()

    # Orders page
    elif option == "O":
        menuOrd()

    # MRP page
    elif option == "M":
        menuMRP()
