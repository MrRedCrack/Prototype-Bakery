'''
=============================================================
                   ordOpt.py: Order Options
            Function storage for the Orders page.
-------------------------------------------------------------
Besides containing functions that return orders information,
it defines the operational functions:
1. Add order
2. Delete order
3. Edit order

Orders are stored in and read from orders.txt
=============================================================
'''

import filehand
from options import *
from recOpt import getRecipeOptions, getRecipeList

def getOrderOptions(): # Returns a list of ['1','2','3',..,'C'] depending on number of orders in orders.txt
    numList=[f"{num+1}" for num in range(int(len(getOrderList())/2))]
    numList.append("C")
    return numList

def getOrderList(): # Returns a list after reading orders.txt; 'OrderName', 'OrderAmount' appended per order to orderList
    orderListRaw=filehand.read("orders.txt")
    orderList=[]
    for elem in orderListRaw:
        elem=elem.strip("\n")
        orderList.append(elem)
    return orderList

def add(): # Add order
    
    # Options prompt with input range [number of orders] and C
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions())

    if select != "C":
        cancel=False
        select=int(select)-1
        # Input, and input validation stage
        while True:
            err=""
            addedAmount=str(input(f"{ind}{'Add amount':<20}[C]ancel: "))
            try:
                if getRecipeList()[select] in getOrderList():
                    orderIndex=getOrderList().index(getRecipeList()[select])                
                    oldOrderAmount=int(getOrderList()[orderIndex+1])
                    orderExists=True
                else:
                    oldOrderAmount=0            
                    orderExists=False
                if int(addedAmount)+oldOrderAmount > 1000 or int(addedAmount)+oldOrderAmount <= 0:
                    err="Total amount should be more than 0, no more than 1000."
            except:
                if addedAmount.upper() == "C":
                    cancel=True
                    break
                else:
                    err="Invalid number."

            if not cancel:
                if err:
                    printMod(err)
                else:
                    break

        if not cancel:
            newOrderListRaw=getOrderList()

            # Update existing order amount if order already exists
            if orderExists:
                orderIndex=getOrderList().index(getRecipeList()[select])                
                oldOrderAmount=getOrderList()[orderIndex+1]
                newOrderListRaw.pop(orderIndex+1)
                newOrderListRaw.insert(orderIndex+1,str(int(addedAmount)+int(oldOrderAmount)))

            # Append to order list if order did not exist
            else:
                newOrderListRaw.append(getRecipeList()[select])
                newOrderListRaw.append(addedAmount)

            filehand.writelines("orders.txt",newOrderListRaw)

def delete(): # Delete order
    
    select=prompt(f"{'Select order no.':<20}[C]ancel: ",getOrderOptions())

    if select != "C":
        select=int(select)-1
        # Find and delete order in order list
        newOrderListRaw=getOrderList()
        orderIndex=(select*2)
        newOrderListRaw.pop(orderIndex)
        newOrderListRaw.pop(orderIndex)

        filehand.writelines("orders.txt",newOrderListRaw)

def edit(): # Edit order amount
    
    select=prompt(f"{'Select order no.':<20}[C]ancel: ",getOrderOptions())

    if select != "C":
        cancel=False
        select=int(select)-1
        # Input amount, and amount validation stage
        while True:
            err=""
            editedAmount=str(input(f"{ind}{'Edit amount':<20}[C]ancel: "))
            try:            
                if int(editedAmount) > 1000 or int(editedAmount) <= 0:
                    err="Amount should be more than 0, no more than 1000."
            except:
                if editedAmount.upper() == "C":
                    cancel = True
                    break
                else:
                    err="Invalid number."

            if not cancel:
                if err:
                    printMod(err)
                else:
                    break

        if not cancel:            
            newOrderListRaw=getOrderList()
            orderIndex=select*2

            # Edit order amount
            newOrderListRaw.pop(orderIndex+1)
            newOrderListRaw.insert(orderIndex+1,editedAmount)
            
            filehand.writelines("orders.txt",newOrderListRaw)

def reset(): # Clear order.txt
    confirm=prompt("Are you sure? [Y]es [C]ancel: ","YC")
    if confirm != "C":
        filehand.write("orders.txt","")