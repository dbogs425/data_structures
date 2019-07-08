#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#                                                $
#  Assignment 2 -- Daniel Bolognino -- CISC 3130 $
#                                                $
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#---------------------------------------------
#--------------- Constructors ----------------
#---------------------------------------------

#Define inventory / name associated with a warehouse
class Warehouse():
    def __init__(warehouse, warehouseName, amt1, amt2, amt3):
        warehouse.warehouseName = warehouseName
        warehouse.amt1 = amt1
        warehouse.amt2 = amt2
        warehouse.amt3 = amt3

#Constructor for order cards
class Card():
    def __init__(card, orderType, city, amt1, amt2, amt3):
        card.orderType = orderType
        card.city = city
        card.amt1 = amt1
        card.amt2 = amt2
        card.amt3 = amt3
        
#Constructor for storing price list (3 items)
class PriceList():
    def __init__(pricelist, item1, item2, item3):
        pricelist.item1 = item1
        pricelist.item2 = item2
        pricelist.item3 = item3

#---------------------------------------------
#----------- File Read Functions -------------
#---------------------------------------------
#Initialize the 5 warehouse objects, and append to array for updated inforamtion
def initialize():
  warehouses = []
  warehouses.append(Warehouse("New York", 0, 0, 0))
  warehouses.append(Warehouse("Miami", 0, 0, 0)) 
  warehouses.append(Warehouse("Los Angeles", 0, 0, 0))
  warehouses.append(Warehouse("Houston", 0, 0, 0))
  warehouses.append(Warehouse("Chicago", 0, 0, 0))
  return warehouses

#Read function for master txt file (comma delimited)
def readMaster():
  cards = []
  count = 0
  master_file = open("./master.txt", "r")
  for line in master_file:
        values = line.split(", ")
        count += 1
        #Initial value is the pricelist, store this first
        if count == 1:
            pricelist = PriceList(float(values[0]), float(values[1]), float(values[2]))
        #Store all card information
        else:
            card = Card(values[0], values[1], int(values[2]), int(values[3]), int(values[4]))
            cards.append(card)
  return pricelist, cards

#---------------------------------------------
#----------- Processing Functions ------------
#---------------------------------------------

#Function to process shipments -- update inventory of warehouses
def processShipment(city, warehouses):
    for warehouse in warehouses:
        if city == warehouse.warehouseName:
            warehouse.amt1 += card.amt1
            warehouse.amt2 += card.amt2
            warehouse.amt3 += card.amt3
            print ("SHIPMENT: " + card.city + " " + str(card.amt1) + " " + str(card.amt2) + " " + str(card.amt3) + "\nUPDATED INVENTORY: " + warehouse.warehouseName + " " + str(warehouse.amt1) + " " + str(warehouse.amt2) + " " + str(warehouse.amt3) + "\n")

#Function to fill orders if not found in warehouse
def searchFor(itemNumber, quantity):
    largest = Warehouse("", 0, 0, 0)
    #Case for if items, ex. if itemNumber is number 1 (comparing amt1)
    if(itemNumber == 1):
        for warehouse in warehouses:
            if warehouse.amt1 >= quantity and warehouse.amt1 > largest.amt1:
                largest = warehouse
    elif(itemNumber == 2):
        for warehouse in warehouses:
            if warehouse.amt2 >= quantity and warehouse.amt2 > largest.amt2:
                largest = warehouse
    elif(itemNumber == 3):
        for warehouse in warehouses:
            if warehouse.amt3 >= quantity and warehouse.amt3 > largest.amt3:
                largest = warehouse
    #If largest's city property remains unchanged, return unfilled
    if largest.warehouseName == "":
        return "Order Unfilled"
    elif(itemNumber == 1):
        for warehouse in warehouses:
            if warehouse.warehouseName == largest.warehouseName:
                warehouse.amt1 -= quantity
                return "Item " + str(itemNumber) + " shipped from " + warehouse.warehouseName + " to "
    elif(itemNumber == 2):
        for warehouse in warehouses:
            if warehouse.warehouseName == largest.warehouseName:
                warehouse.amt2 -= quantity
                return "Item " + str(itemNumber) + " shipped from " + warehouse.warehouseName + " to "
    elif(itemNumber == 3):
        for warehouse in warehouses:
            if warehouse.warehouseName == largest.warehouseName:
                warehouse.amt3 -= quantity
                return "Item " + str(itemNumber) + " shipped from " + warehouse.warehouseName + " to "
    
    
#Base function for processing cards
def processOrder(card, warehouses, pricelist):
    #Iterrate through warehouses to find a warehouse with matching city
    for warehouse in warehouses:
         if card.city == warehouse.warehouseName:
            #Basic boolean logic for later comparisons
            enoughItem1 = card.amt1 <= warehouse.amt1
            enoughItem2 = card.amt2 <= warehouse.amt2
            enoughItem3 = card.amt3 <= warehouse.amt3
            #If order can be processed, subtract item from inventory
            if enoughItem1:
                warehouse.amt1 -= card.amt1
            else:
            #Search for items in other locations with searchFor() function
                search1 = searchFor(1, card.amt1)
                if search1 != "Order Unfilled":
                    #If order was filled, amt1 has a 10% surcharge for shipping
                    card.amt1 *= 1.1
                    #Add warehouse name (city) to the output string
                    search1 += warehouse.warehouseName
                    print search1
                else:
                    #Do not use amt for end calculation if not found
                    card.amt1 = 0;
                    print search1 + " for item 1"
            #Repeat for item2
            if enoughItem2:
                warehouse.amt2 -= card.amt2
            else:
                search2 = searchFor(2, card.amt2)
                if search2 != "Order Unfilled":
                    card.amt2 *= 1.1
                    search2 += warehouse.warehouseName
                    print search2
                else:
                    card.amt2 = 0
                    print search2 + " for item 2"
            #Repeat for item3
            if enoughItem3:
                warehouse.amt3 -= card.amt3
            else:
                search3 = searchFor(3, card.amt3)
                if search3 != "Order Unfilled":
                    card.amt1 *= 1.1
                    search3 += warehouse.warehouseName
                    print search3
                else:
                    card.amt3 = 0
                    print search3 + " for item 3"
            print ("Price of Order: " + str((card.amt1 * pricelist.item1) + (card.amt2 * pricelist.item2) + (card.amt3 * pricelist.item3)) + "\n")

#---------------------------------------------
#------------- Runner Functions --------------
#---------------------------------------------
# 1) Start by initializing the 5 warehouses
warehouses = initialize()
# 2) Read master file, store prices in pricelist, store orders as cards
pricelist, cards = readMaster()
# 3) Process the cards, update inventory
for card in cards:
    if card.orderType == "s":
        processShipment(card.city, warehouses)
    elif card.orderType == "o":
        processOrder(card, warehouses, pricelist)
# 4) Print out updated amounts
for warehouse in warehouses:
    print (warehouse.warehouseName + " " + str(warehouse.amt1) + " " + str(warehouse.amt2) + " " + str(warehouse.amt3))