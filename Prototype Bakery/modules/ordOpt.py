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
    4. Clear/reset orders

    Orders are stored in and read from orders.txt
    =============================================================
'''

import modules.filehand as filehand
from modules.options import prompt,printMod,inputMod,Err
from modules.recOpt import getRecipeOptions, getRecipeList

# Returns a list of ['1','2','3',..,'C']
# depending on number of orders in orders.txt
def getOrderOptions(): 
    ordersNo=len(getOrderList())//2
    numList=[f"{num+1}" for num in range(ordersNo)]
    numList.append("C")
    return numList

# Returns a list after reading orders.txt;
# 'OrderName', 'OrderAmount' appended per order to orderList
def getOrderList(): 
    orderListRaw=filehand.read("orders.txt")
    orderList=[]
    for elem in orderListRaw:
        elem=elem.strip("\n")
        orderList.append(elem)
    return orderList

'''
Operational functions
---------------------------------------------------------------------------------'''
# Add order
def add():
    # Options prompt with input range [number of orders] and C
    select=prompt(f"{'Select recipe no.':<20}[C]ancel: ",getRecipeOptions())

    if select != "C":
        cancel=False
        select=int(select)-1
        # Input, and input validation stage
        while True:
            err=""
            addedAmount=inputMod(f"{'Add amount':<20}[C]ancel: ")
            try:
                recipe=getRecipeList()[select]
                if recipe in getOrderList():
                    orderIndex=getOrderList().index(recipe)
                    orderAmtIndex=orderIndex+1             
                    oldOrderAmount=int(getOrderList()[orderAmtIndex])
                    total=int(addedAmount)+oldOrderAmount
                    orderExists=True
                else:            
                    total=int(addedAmount)
                    orderExists=False
                if total > 1000 or total <= 0:
                    err=Err['orderLimit']
            except:
                if addedAmount.upper() == "C":
                    cancel=True
                    break
                else:
                    err=Err['invalidInt']

            if not cancel:
                if err:
                    printMod(err)
                else:
                    break

        if not cancel:

            newOrderListRaw=getOrderList()
            # Update existing order amount
            if orderExists:
                newOrderListRaw[orderAmtIndex]=str(total)
            else: # Append to order list
                newOrderListRaw.append(getRecipeList()[select])
                newOrderListRaw.append(addedAmount)
            filehand.writelines("orders.txt",newOrderListRaw)

# Delete order
def delete():
    select=prompt(f"{'Select order no.':<20}[C]ancel: ",getOrderOptions())

    if select != "C":
        select=int(select)-1
        # Find and delete order in order list
        newOrderListRaw=getOrderList()
        orderIndex=(select*2)
        del newOrderListRaw[orderIndex:orderIndex+2]
        filehand.writelines("orders.txt",newOrderListRaw)

# Edit order amount
def edit():
    select=prompt(f"{'Select order no.':<20}[C]ancel: ",getOrderOptions())

    if select != "C":
        cancel=False
        select=int(select)-1
        # Input amount, and amount validation stage
        while True:
            err=""
            editedAmount=inputMod(f"{'Edit amount':<20}[C]ancel: ")
            try:
                if int(editedAmount) > 1000 or int(editedAmount) <= 0:
                    err=Err['orderLimit']
            except:
                if editedAmount.upper() == "C":
                    cancel = True
                    break
                else:
                    err=Err['invalidInt']

            if not cancel:
                if err:
                    printMod(err)
                else:
                    break

        if not cancel:

            newOrderListRaw=getOrderList()
            orderAmtIndex=select*2+1
            # Edit order amount
            newOrderListRaw[orderAmtIndex]=editedAmount
            filehand.writelines("orders.txt",newOrderListRaw)

# Clear orders
def reset():
    confirm=prompt("Are you sure? [Y]es [C]ancel: ","yc")
    if confirm != "C":
        filehand.write("orders.txt","")
