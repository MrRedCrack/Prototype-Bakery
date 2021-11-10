'''
Prototype Bakery.py: The main program
This is the main() program to be executed.

It mainly consists of interface-printing functions and interface-navigating code structure.
Interface-printing functions are divided into different blocks for easy pick and combining in building a new page.
Most operations are saved in and called from xxxOpt.py files, named according to their respective page.

Every supposedly - print() function is modified and replaced with options.printMod() for indentation purposes.
All {options.ind} too, found after \n are for indentation purposes only. They can be found in other files.
Interface indentation can be updated in options.py

'''
##Essential module dumps
import os
import datetime

import filehand
##Check and regenerate file if missing
#Inventory
newIngredientFile=False
if filehand.exist("ing.txt") != True:
    filehand.write("ing.txt","")
    newIngredientFile=True #Report to Inventory page if the file was missing and regenerated

#Recipe
newRecipeFile=False
if filehand.exist("rec.txt") != True:
    filehand.write("rec.txt","")
    newRecipeFile=True #Report to Recipes page if the file was missing and regenerated

#Recipe Descriptions
if filehand.exist("recDesc.txt") != True:
    filehand.write("recDesc.txt","")

#Orders
if filehand.exist("orders.txt") != True:
    filehand.write("orders.txt","")

import options
import ingOpt
import recOpt
import ordOpt
import mrpOpt

##Interface blocks definition
def header(clear=False): #Called first for every page to clear screen (if clear==True), then print date, time, and bakery name.
    if clear==True:
        os.system('cls')
    print('')
    options.printMod(f"{datetime.datetime.today().strftime('%Y-%m-%d - %H:%M:%S'):^80}")
    options.printMod(f"{'Prototype Bakery':^80}")
    options.printMod(f"{'='*80}")

def mainMenu(): #Main menu page block
    options.printMod(f"{'Main Menu':^80}")
    options.printMod("="*80)
    options.printMod(f" [I]nventory\n{options.ind} [R]ecipes\n{options.ind} [O]rder\n{options.ind} [M]aterial Requirements Plan\n\n{options.ind} [Q]uit")
    options.printMod("="*80)

def pageInventory(): #Inventory menu page block
    options.printMod(f"{'Inventory':^80}")
    global newIngredientFile
    if newIngredientFile==True:
        options.printMod(f"{'Could not find ing.txt ... A new file was created.':^80}")
        newIngredientFile=False
    options.printMod("="*80)

    #Read and print ingredients list from ing.txt
    ingListCurrent=filehand.read("ing.txt")
    if len(ingListCurrent)>0:
        options.printMod(f"{'Item:':^26}{' Amount:':^24}")
        options.printMod('-'*80)
        for items in ingListCurrent:
            item=items.strip("\n").split(" ")
            options.printMod(f"{item[0]:<23}--{float(item[2]):>24.2f} {item[1]}")   
    else:
        options.printMod(f"{'no ingredients':^80}")

    options.printMod("="*80)
    options.printMod("[A]dd [D]elete [E]dit [B]ack")
    options.printMod("="*80)

def pageRecipe(): #Recipe page block
    options.printMod(f"{'Recipes':^80}")
    global newRecipeFile
    if newRecipeFile==True:
        options.printMod(f"{'Could not find rec.txt ... A new file was created.':^80}")
    options.printMod('='*80)

    #Read from rec.txt
    for elem in recOpt.getRecipeList():        
        #And print recipe list
        options.printMod(f"{recOpt.getRecipeList().index(elem)+1}. {elem:<20} - {recOpt.getRecDesc(elem):<25}")

    options.printMod("="*80)
    options.printMod("[A]dd [D]elete [R]ename [V]iew [B]ack")
    options.printMod("[E]dit description")
    options.printMod("="*80)

def pageRecDesc(recipeName): #Recipe description block. To be used in ingredients page of recipes
    if recOpt.getRecDesc(recipeName) == '':
        options.printMod(f"{'No description.':^80}")
    else:
        options.printMod(f"{recOpt.getRecDesc(recipeName):^80}")
    options.printMod("="*80)

def pageRecIngredients(recipeNum): #Recipe ingredients block. To be used in ingredients page of recipes
    recipeName=recOpt.getRecipeList()[recipeNum]
    text=f"Ingredients for {recipeName}"
    options.printMod(f"{text:^80}")
    pageRecDesc(recipeName)

    #Read and print ingredients list from getRecIngredients(recipeName)
    ingListCurrent=recOpt.getRecIngredients(recipeName)
    if len(ingListCurrent)>0 and ingListCurrent[0] != '':
        options.printMod(f"{'Item:':^26}{' Amount:':^24}")
        for items in ingListCurrent:
            item=items.split(" ")
            options.printMod(f"{item[0]:<23}--{float(item[2]):>24.2f} {item[1]}")
    
    options.printMod("="*80)
    options.printMod("[A]dd [D]elete [E]dit [B]ack")
    options.printMod("="*80)
    return recipeName

def pageOrder(toggleRecipes): #Order page block

    if toggleRecipes:
        options.printMod("Recipes available:")
        #Read from rec.txt
        for elem in recOpt.getRecipeList():
            
            #And print recipe list
            options.printMod(f"{recOpt.getRecipeList().index(elem)+1}. {elem:<26}")
        options.printMod('-'*80)
        options.printMod('')

    options.printMod(f"{'Current Orders':^80}")
    options.printMod('='*80)
    if len(ordOpt.getOrderList()) < 1:
        options.printMod(f"{'No orders yet':^80}")
    for counter in range(0,len(ordOpt.getOrderList()),2):
        options.printMod(f"{int(counter/2+1)}. {ordOpt.getOrderList()[counter]:<17} - {recOpt.getRecDesc(ordOpt.getOrderList()[counter]):<23}* {ordOpt.getOrderList()[counter+1]:<8}")

    options.printMod("")
    options.printMod("="*80)
    options.printMod(f"[A]dd [D]elete [E]dit [B]ack \n{options.ind}[T]oggle recipes [R]eset orders")
    options.printMod("="*80)

def pageMRP1(): #1st half of MRP page block
    options.printMod(f"{'Material Requirements Plan':^80}")
    options.printMod("="*80)
    if len(ordOpt.getOrderList()) < 1:
        options.printMod(f"{'no orders - no plan':^80}") #No MRP if no orders
    else:

        #Start printing report!
        #Print orders planned
        options.printMod("Orders planned >>>")
        for counter in range(0,len(ordOpt.getOrderList()),2):
            options.printMod(f"{int(counter/2+1)}. {ordOpt.getOrderList()[counter]:<17} - {recOpt.getRecDesc(ordOpt.getOrderList()[counter]):<23}* {ordOpt.getOrderList()[counter+1]:<8}")
        options.printMod('')
        
        #Print ingredients and their shortfalls
        options.printMod('Ingredients required >>>')
        options.printMod('-'*80)
        options.printMod(f"{'Ingredients:':<17}{'Stock:':>18}{'Demand:':>18}{'Shortfall:':>21}")
        options.printMod('-'*80)
        planList=mrpOpt.ingReqList()
        for elem in planList:
            options.printMod(f"{elem[0]:<17}{elem[1]:>18}{elem[2]:>18}{elem[3]:>19}{elem[4]:>2}")
        
        options.printMod(f"")

    options.printMod("-"*80)

def pageMRP2(): #2nd half of MRP page block. Separated to not be included when printing to MRP txt file
    if len(ordOpt.getOrderList()) >= 1:
        options.printMod("[S]ave to file  [B]ack")
        options.printMod("="*80)
   
    else:
        options.printMod("[B]ack")
        options.printMod("="*80)

##main()
#MainMenu
isOn = True
while isOn:
    header(True)
    mainMenu()
    option=(options.prompt("Option  >>","QIROM")) #Options prompt with input range Q, I, R, O, M
    
    if option == "Q": #Quit program
        isOn = False

    ##IngredientsPage
    if option == "I":
        onIng=True
        while onIng==True:
            header(True)
            pageInventory()
            option=(options.prompt("Option  >>","BADE")) #Options prompt with input range B, A, D, E

            if option == "B": #Back
                onIng=False

            if option == "A": #Add ingredient
                ingOpt.add(filehand.read("ing.txt"),"ing.txt")

            if option == "D": #Delete ingredient
                ingOpt.delete(filehand.read("ing.txt"),"ing.txt")

            if option == "E": #Edit existing ingredient
                ingOpt.edit(filehand.read("ing.txt"),"ing.txt")

    ##RecipesPage
    if option == "R":
        onRec=True
        while onRec:
            header(True)
            pageRecipe()
            option=(options.prompt("Option  >>","ABDEVR")) #Options prompt with input range A, B, D, E, V, R

            if option == "B": #Back
                onRec = False

            if option == "V": #View recipe ingredients
                cancel=False
                while cancel==False:
                    
                    #Options prompt with input range [number of recipes] and C; choose recipe by number to view its ingredients
                    option=options.prompt("Select recipe no.: ",recOpt.getRecipeOptions())
                    if option == "C": #Cancel recipe selection
                        cancel=True
                    
                    ##Recipe ingredients page
                    else:
                        onRecIngredient=True
                        while onRecIngredient:
                            header(True)
                            currentRecipeName=pageRecIngredients(int(option)-1)
                            optionRecIng=(options.prompt("Option  >>","ADEB")) #Options prompt with input range A, D, E, B

                            if optionRecIng == "B": #Back
                                onRecIngredient=False
                                cancel=True

                            if optionRecIng == "A": #Add ingredient
                                addedIng=ingOpt.add(recOpt.getRecIngredients(currentRecipeName),"rec.txt")

                                if len(addedIng) > 0: #Confirm add ingredient if list returned is not empty
                                    recOpt.rewriteRecipe(currentRecipeName,addedIng)

                            if optionRecIng == "D": #Delete ingredient
                                deletedIng=ingOpt.delete(recOpt.getRecIngredients(currentRecipeName),"rec.txt")

                                if len(deletedIng) > 0: #Confirm delete ingredient if list returned is not empty
                                    recOpt.rewriteRecipe(currentRecipeName,deletedIng)

                            if optionRecIng == "E": #Edit ingredient
                                editedIng=ingOpt.edit(recOpt.getRecIngredients(currentRecipeName),"rec.txt")

                                if len(editedIng) > 0: #Confirm edit ingredient if list returned is not empty
                                    recOpt.rewriteRecipe(currentRecipeName,editedIng)

            if option == "R": #Rename recipe
                recOpt.rename()

            if option == "A": #Add recipe name
                recOpt.add()

            if option == "D": #Delete recipe
                recOpt.delete()

            if option == "E": #Edit recipe description
                recOpt.description()

    ##OrdersPage
    if option == "O":
        onOrd=True
        toggleRecipes=True
        while onOrd:
            header(True)            
            pageOrder(toggleRecipes)
            option=(options.prompt("Option  >>","BTADER")) #Options prompt with input range B, T, A, D, E, R

            if option == "B": #Back
                onOrd=False
            
            if option == "T": #Toggle "Available recipes" view
                toggleRecipes= not toggleRecipes
            
            if option == "A": #Add order from existing recipe:
                ordOpt.add()
            
            if option == "D": #Delete order
                ordOpt.delete()

            if option == "E": #Edit order
                ordOpt.edit()

            if option == "R": #Reset orders
                ordOpt.reset()

    ##MRP page
    if option == "M":
        onMRP=True
        while onMRP:
            def printMRP(): #Collecting required functions to print in one function into Save2File
                header(False)
                pageMRP1()
            header(True)
            pageMRP1()
            pageMRP2()
            if len(ordOpt.getOrderList()) < 1: #Remove the Save2File option if no orders were made
                addS=''
            else:
                addS='S'
            option=(options.prompt("Option  >>",f"B{addS}"))

            #Back to menu
            if option == "B": #Back
                onMRP=False

            if option == "S": #Save2File
                dirName="Saved Documents" #Folder/directory name, can change here
                if not filehand.exist(dirName):
                    filehand.mkdir(dirName)
                fileName=f"MRP {datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')}.txt" #Text file name, can change here
                filehand.write(f"{dirName}\\{fileName}","")
                filehand.printFile(f"{dirName}\\{fileName}",printMRP)
                input(f"{options.ind}Saved as '{fileName}' in folder '{dirName}'\n{options.ind}Enter to continue.")