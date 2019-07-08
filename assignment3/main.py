#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#                                                $
#  Assignment 3 -- Daniel Bolognino -- CISC 3130 $
#                                                $
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#---------------------------------------------
#--------------- Constructors ----------------
#---------------------------------------------

#Constructer for singly linked list
class LinkedList:
    def __init__(self):
        self.head = None

#Constructor for a node (Singly Linked List)
class Node(object):
    def __init__(node, data=None, next_node=None):
        node.data = data
        node.next_node = next_node

    def get_data(node):
        return node.data

    def get_next(node):
        return node.next_node

    def set_next(node, newNode):
        node.next_node = newNode

#Sale Constructor
class Sale:
    def __init__(sale, quantity, discountRate):
        sale.quantity = quantity
        #Discount rate -- usually 1 (100%)
        sale.discountRate = discountRate

#Receipt Constructor
class Receipt:
    def __init__(receipt, quantity, price):
        receipt.quantity = quantity
        receipt.price = price

#Promotion Constructor
class Promotion:
    def __init__(promotion, discount):
        promotion.discount = discount

#---------------------------------------------
#--------------- File Read Func --------------
#---------------------------------------------

#Read the master file, return a singly linked list
def readMaster():
    count = 0
    #Initiate List
    masterList = LinkedList()
    master_file = open("./master.txt", "r")
    #Iterate through master
    for line in master_file:
        values = line.split(",")
        if values[0] == "P":
            data = Promotion(int(values[1]))
        #If data is a sale:
        elif values[0] == "S":
            data = Sale(int(values[1]), 1.0)
        #If data is a receipt:
        elif values[0] == "R":
            data = Receipt(int(values[1]), (float(values[2])))
        newNode = Node(data)
        #First value must be pushed to head val:
        if count == 0:
            masterList.head = newNode
        #Second value must be linked to head value
        elif count == 1:
            masterList.head.next_node = newNode
            current = newNode
        #All other values treat the same -- assign next node to current node, reset current to this node after operation is done
        else:
            current.next_node = newNode
            current = newNode
        count += 1
    return masterList


#---------------------------------------------
#----------- Processing Functions ------------
#---------------------------------------------

#Function handling processing of sale cards
def processSale(head, node):
    #Total of order, counter for quantity filled, string to be printed, and a reference for iterrating through the list
    total = 0.00
    quantityCounter = 0
    printString = ""
    referenceNode = head
    #Will be reducing node.data.quantity
    totalNeeded = node.data.quantity
    #Start from beginning of list to make sure all items are sold in FIFO order, stop in the event that you get to the same place as node, or if order has been filled (quantity level met)
    print "\nSALE:\n---------------------"
    while referenceNode != node and quantityCounter != totalNeeded:
        #If list item is a receipt type, and items left from that record:
        if (referenceNode.data.__class__.__name__ == "Receipt" and referenceNode.data.quantity != 0):
            #Track quantity purchased (referenceNode value will be reset)
            quantityPurchased = 0
            #If that node has items available for purchase, but not enough to fill the whole order, do the following:
            if ((node.data.quantity - referenceNode.data.quantity) >  0):
                #Add what's available to quantity counter (overall), quantityPurchased (at this price), and order total  
                quantityCounter += referenceNode.data.quantity
                quantityPurchased = referenceNode.data.quantity
                #Items have been depleted from this record, so set that node's quantity available to 0, reduce number required for sale
                referenceNode.data.quantity = 0
            else:
                quantityPurchased = node.data.quantity
                quantityCounter += quantityPurchased
                referenceNode.data.quantity -= quantityPurchased
                    
            total += (quantityPurchased * 1.3 * referenceNode.data.price * node.data.discountRate)
            #Reduce available items on this node by quantity purchased
            node.data.quantity -= quantityPurchased
            #Add to print string
            printString += str(quantityPurchased) + " at " + str(referenceNode.data.price * 1.3 * node.data.discountRate) + "\tSales: $" + str(referenceNode.data.price * 1.3 * node.data.discountRate * quantityPurchased) + "\n"
            #Set the reference to next node in list and repeat
        referenceNode = referenceNode.get_next()
        #END OF LOOP
                
    print printString + "\n\t\tTotal Sales: $" + str(total)
    #Check to see if the entire order has been placed, if not print it out
    if (node.data.quantity != 0):
        #If not print what has been, and items not available
        print "*Remainder of " + str(node.data.quantity) + " widgets not available"

        
#Function handling processing of promotion cards
def processPromotion(node):
    #Reference to track nodes, and promotionsApplied counter
    referenceNode = node
    promotionsApplied = 0
    #Run a loop until list is at end or if 2 promotions were applied (Using multiplicative identity to apply promos)
    while referenceNode != None and promotionsApplied < 2:
        print referenceNode.data.__class__.__name__
        #check to see if referenceNode is sale -- apply discount to this sale
        if (referenceNode.data.__class__.__name__ == "Sale"):
            referenceNode.data.discountRate =  ((100.00 - float(node.data.discount)) / 100.00)
            print referenceNode.data.discountRate
            promotionsApplied += 1
        referenceNode = referenceNode.get_next()
        #END OF LOOP
    print "\nPROMOTION\n---------------------\nAmount applied to next two sales: " + str(node.data.discount) + "% off"


#Function handling processing of receipt cards
def processReceipt(node):
    #Simply print the receipt
    print "\nRECEIPT:\n---------------------\nPrice: $" + str(node.data.price) + "\tQuantity: " + str(node.data.quantity) + "\nTotal: $" + str(node.data.quantity * node.data.price)

def processList(node):
    #Store head (node passed to function) for later use
    head = node
    #Loop through cards (masterList), conditionals for each case
    while node != None:
        if(node.data.__class__.__name__ == "Receipt"):
            processReceipt(node)
        elif(node.data.__class__.__name__ == "Sale"):
            processSale(head, node)
        elif(node.data.__class__.__name__ == "Promotion"):
            processPromotion(node)
        #Get next card
        node = node.get_next()


#Calculate the items remaining in the list at the end
def widgetsRemaining(node):
    print "\n\n\nTOTAL REMAINING\n---------------------\n"
    while node != None:
        if (node.data.__class__.__name__ == "Receipt" and node.data.quantity != 0):
            print ("Quantity: " + str(node.data.quantity) + "\tPurchase Price: " + str(node.data.price))
        node = node.get_next()
    
#---------------------------------------------
#------------- Runner Functions --------------
#---------------------------------------------

# STEP 1) READ MASTER FILE
masterList = readMaster()

# STEP 2) PROCESS AND PRINT OPERATIONS
processList(masterList.head)

# STEP 3) COUNT WIDGETS REMAINING AND ORIGINAL PRICES
widgetsRemaining(masterList.head)