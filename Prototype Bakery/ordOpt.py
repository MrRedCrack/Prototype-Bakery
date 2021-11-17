'''
ordOpt.py: ordOpt stands for Order Options
This is the function storage for the "Order" page.

Besides containing a function for conveniently returning a list containing orders information,
it defines the operational functions for managing orders:
1. add order
2. delete order
3. edit order

Orders are stored in orders.txt

'''
##Essential module dumps
import filehand
from options import *
from recOpt import getRecipeOptions, getRecipeList

def getOrderOptions(): #Returns a list of ['1','2','3',..,'C'] depending on number of orders in orders.txt
    numList=[f"{num+1}" for num in range(int(len(getOrderList())/2))]
    numList.append("C")
    return numList

def getOrderList(): #Returns a list containing orders information after reading orders.txt; 'OrderName', 'OrderAmount' appended per order to orderList
    orderListRaw=filehand.read("orders.txt")
    orderList=[]
    for elem in orderListRaw:
        elem=elem.strip("\n")
        orderList.append(elem)
    return orderList

def add(): #Add order
    
    #Options prompt with input range [number of orders] and C
    select=prompt("Select recipe no.: ",getRecipeOptions())

    if select != "C":
        #Input, and input validation stage
        check=True
        cancel=False
        while check:
            err=""
            addedAmount=str(input(f"{ind}{'Add amount':<20}[C]ancel: "))
            try:
                if getRecipeList()[int(select)-1] in getOrderList():
                    orderIndex=getOrderList().index(getRecipeList()[int(select)-1])                
                    oldOrderAmount=int(getOrderList()[orderIndex+1])
                    orderExists=True
                else:
                    orderExists=False
                    oldOrderAmount=0            
                if int(addedAmount)+oldOrderAmount > 1000 or int(addedAmount)+oldOrderAmount <= 0:
                    err="Total amount should be more than 0, no more than 1000."
            except:
                if addedAmount.upper() == "C":
                    cancel = True
                else:
                    err="Invalid number."

            if cancel != True:
                if err:
                    printMod(err)
                else:
                    check=False
            else:
                check=False

        #Write added order to orders.txt if not cancelled
        if not cancel:
            newOrderListRaw=getOrderList()

            #Update existing order amount if order already exists
            if orderExists:
                orderIndex=getOrderList().index(getRecipeList()[int(select)-1])                
                oldOrderAmount=getOrderList()[orderIndex+1]
                newOrderListRaw.pop(orderIndex+1)
                newOrderListRaw.insert(orderIndex+1,str(int(addedAmount)+int(oldOrderAmount)))

            #Append to order list if order did not exist
            else:
                newOrderListRaw.append(getRecipeList()[int(select)-1])
                newOrderListRaw.append(addedAmount)

            #Update orders.txt with new order list via filehand
            filehand.writelines("orders.txt",newOrderListRaw)

def delete(): #Delete order
    
    #Options prompt with input range [number of orders] and C
    select=prompt("Select order no.: ",getOrderOptions())

    #Delete order from orders.txt if not cancelled
    if select != "C":
        
        #Find and delete order in order list
        newOrderListRaw=getOrderList()
        orderIndex=((int(select)-1)*2)
        newOrderListRaw.pop(orderIndex)
        newOrderListRaw.pop(orderIndex)

        #Update orders.txt with new order list via filehand
        filehand.writelines("orders.txt",newOrderListRaw)

def edit(): #Edit order amount
    
    #Options prompt with input range [number of orders] and C
    select=prompt("Select order no.: ",getOrderOptions())

    if select != "C":
        #Input amount, and amount validation stage
        check=True
        cancel=False
        while check:
            err=""
            editedAmount=str(input(f"{ind}{'Edit amount':<20}[C]ancel: "))
            try:            
                if int(editedAmount) > 1000 or int(editedAmount) <= 0:
                    err="Amount should be more than 0, no more than 1000."
            except:
                if editedAmount.upper() == "C":
                    cancel = True
                else:
                    err="Invalid number."

            if cancel != True:
                if err:
                    printMod(err)
                else:
                    check=False
            else:
                check=False

        #Update order.txt if not cancelled
        if not cancel:            
            newOrderListRaw=getOrderList()
            orderIndex=(int(select)-1)*2

            #Edit order amount
            newOrderListRaw.pop(orderIndex+1)
            newOrderListRaw.insert(orderIndex+1,editedAmount)
            
            #Update orders.txt with new order list via filehand
            filehand.writelines("orders.txt",newOrderListRaw)

def reset(): #Clear order.txt
    confirm=prompt("Are you sure? [Y]es [C]ancel: ","YC")
    if confirm != "C":
        filehand.write("orders.txt","")