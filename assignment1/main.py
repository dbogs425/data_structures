#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#                                                $
#  Assignment 1 -- Daniel Bolognino -- CISC 3130 $
#                                                $
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#---------------------------------------------
#--------------- Constructors ----------------
#---------------------------------------------

#Order class, to store orders
class Order:
    def __init__(transaction, transactionId, customerId):
      transaction.transactionId = transactionId
      transaction.customerId = customerId
      
      def processPayment(transaction):
        #Itterate through customers to find customer number
        for customer in customers:
            #If number matches subtract amount paid
            if customer.customerId == transaction.customerId:
              customer.balanceDue -= transaction.paymentAmount
        #Print out
        print ("#" + transaction.transactionId + "/t" + transaction.itemOrdered + "/t" + transaction.cost)
        
      def processOrder(transaction):
        #Itterate through customers to find customer number
        for customer in customers:
            #If number matches subtract amount paid
            if customer.customerId == transaction.customerId:
              customer.balanceDue -= transaction.paymentAmount
        #Print out
        print ("#" + transaction.transactionId + "/t" + transaction.paymentAmount + "/t" + transaction.cost)

#Payment class, to store payments

#Customer class for customer objects
class Customer:
  def __init__(customer, customerId, name, balanceDue):
    customer.customerId = customerId
    customer.name = name
    customer.balanceDue = balanceDue

#Transaction class for transaction objects
class Transaction:
  def __init__(transaction, customerId, transactionId, isOrder):
    transaction.customerId = customerId
    transaction.transactionId = transactionId
    transaction.isOrder = isOrder

#Order class -- child of Transaction
class Order(Transaction):
  def __init__(order, customerId, transactionId, itemOrdered, quantity, cost):
    order.customerId = customerId
    order.transactionId = transactionId
    order.itemOrdered = itemOrdered
    order.quantity = quantity
    order.cost = cost

#Payment class -- child of Transaction
class Payment(Transaction):
  def __init__(payment, customerId, transactionId, paymentAmount):
    payment.customerId = customerId
    payment.transactionId = transactionId
    payment.paymentAmount = paymentAmount

#---------------------------------------------
#----------- File Read Functions -------------
#---------------------------------------------
#Read the master file, store to customers array
def readMaster():
  customers = []
  master_file = open("./master.txt", "r")
  for line in master_file:
      values = line.split()
      customer = Customer(int(values[0]), values[1], float(values[2]))
      customers.append(customer)
  return customers

    
#Function to read the transaction file
def processTransactions():
  orders = []
  payments = []
  count = 0
  transaction_file = open("./transaction.txt", "r")
  #Read each line separately in transaction file
  for line in transaction_file:
      #Declare empty transaction object
      transaction = {}
      #Could use delimeter such as "," and read from csv, but just using a space char
      values = line.split()
      #These values are independent of order type
      customerId = values[0]
      transactionId = values[2]
      #Conditional for if item is an order or payment
      if values[1] == "O":
          itemOrdered = values[3]
          quantity = values[4]
          cost = values[5]
          #Create an order object from corresponding values
          order = Order(int(customerId), int(transactionId), itemOrdered, int(quantity), float(cost))
          #Add order to order Array
          orders.append(order)
      #If payment store the following:
      else:
          paymentAmount = values[3]
          #Create a payment object from corresponding values
          payment = Payment(int(customerId), int(transactionId), float(paymentAmount))
          #Add payment to payment Array
          payments.append(payment)
      count += 1
  return orders, payments

#----------------------------------------
#------- Transaction functions ----------
#----------------------------------------

#Function to check for duplicates
def checkValidity(orders, customers, payments):
  for customer in customers:
    if sum(c.customerId == customer.customerId for c in customers) > 1:
          print("DUPLICATE CUSTOMER: " + str(customer.customerId) + "\n")
          customers.remove(customer)

  for order in orders:
    if sum(o.transactionId == order.transactionId for o in orders) > 1:
          print("DUPLICATE TRANSACTION (ORDER): " + str(order.transactionId) + "\n")
          orders.remove(order)

  for payment in payments:
    if sum(p.transactionId == payment.transactionId for p in payments) > 1:
          print("DUPLICATE TRANSACTION (PAYMENT): " + str(payment.transactionId) + "\n")
          payments.remove(payment)

#Function to complete transactions and update customers (in memory)
def completeTransactions(orders, customers, payments):
  #Array to hold completed transaction numbers -- used in end to check if any were not completed
  completedTransactions = []
  for customer in customers:
    #Check to see if there is more than one customer with the same ID:
    print("NAME: " + customer.name + "\nCUSTOMER NUMBER: " + str(customer.customerId) + "\nPREVIOUS BALANCE: $" + str(customer.balanceDue) + "\n")
    for order in orders:
        if str(order.customerId) == str(customer.customerId):
            print("TRANSACTION NUMBER: " + str(order.transactionId) + "\tITEM ORDERED: " + order.itemOrdered + "\tQUANTITY: " + str(order.quantity) + "\tORDER AMOUNT: $" + str(order.cost))
            customer.balanceDue += order.cost
            completedTransactions.append(order.transactionId)
    for payment in payments:
        if str(payment.customerId) == str(customer.customerId):
            print("TRANSACTION NUMBER: " + str(payment.transactionId) +"\tPAYMENT AMOUNT: $" + str(payment.paymentAmount))
            customer.balanceDue -= payment.paymentAmount
            completedTransactions.append(payment.transactionId)
    print("\nBALANCE DUE: $" + str(customer.balanceDue) + "\n")
  return completedTransactions

#Function to handle errors (customer number not found)
def handleErrors(orders, payments, completedTransactions):
  for order in orders:
    if sum(t == order.transactionId for t in completedTransactions) == 0:
        print("ERROR: CUSTOMER ID NOT FOUND FOR TRANSACTION (ORDER) " + str(order.transactionId))
        orders.remove(order)
  for payment in payments:
    if sum(t == payment.transactionId for t in completedTransactions) == 0:
        print("ERROR: CUSTOMER ID NOT FOUND FOR TRANSACTION (PAYMENT) " + str(order.transactionId))
        orders.remove(order)
  return orders, payments

#----------------------------------------
#------- File Write Function   ----------
#----------------------------------------
def updateMaster(customers):
  f = open("updatedMaster.txt", "w")
  for customer in customers:
    f.write(customer.name + " " + str(customer.customerId) + " " + str(customer.balanceDue) + "0\n")

#----------------------------------------
#----------- Runner functions -----------
#----------------------------------------

#STEP 1: READ THE FILES, STORE THE DATA
customers = readMaster()
orders, payments = processTransactions()
#STEP 2: CHECK TO MAKE SURE THERE ARE NO DUPLICATE RECORDS (ENSURE VALIDITY)
checkValidity(orders, customers, payments)
#STEP 3: USE DATA TO UPDATE AND PRINT CUSTOMER INFO
completedTransactions = completeTransactions(orders, customers, payments)
#STEP 4: HANDLE DATA WITHOUT ASSOCIATED CUSTOMER:
orders, payments = handleErrors(orders, payments, completedTransactions)
#STEP 5: UPDATE MASTER FILE WITH CORRECT DATA
updateMaster(customers)