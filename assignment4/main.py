#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#                                                $
#  Assignment 4 -- Daniel Bolognino -- CISC 3130 $
#                                                $
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#---------------------------------------------
#--------------- Constructors ----------------
#---------------------------------------------

#Tree Node
class Node(object):
    def __init__(node, data):
        node.left = None
        node.right = None
        node.data = data
    
    def getData(node):
        return node.data

    def set_left(node, newNode):
        node.left = newNode

    def set_right(node, newNode):
        node.right = newNode

#Insert Function
    def insert(node, data):
        if node.data is not None:
            if data < node.data:
                if node.left is None:
                    node.left = Node(data)
                else:
                    node.left.insert(data)
            elif data >= node.data:
                if node.right is None:
                    node.right = Node(data)
                else:
                    node.right.insert(data)
        else:
            node.data = data
            
    def deleteNode(node, key):
        #Return None if node Does not exist
        if node is None: 
            return None
	    if node.data > key: 
          #If node value is greater than key, go left (lower number)
		  node.left = node.left.deleteNode(key)
	      #Go right if lesser
        elif node.data < key: 
		  node.right = node.right.deleteNode(key)
        #Delete if the root is the key
        else: 
            #No Right Children:
            if node.right is None:
                return node.left
	       #If there is no left children delete the node and new root would be root.right	
            if node.left is None:
                return node.right
            #If has both, find the min value to replace in the right and delete, set proper values for children
            successor = node.right
            minimum = successor.data
            while successor.left:
                successor = successor.left
                minimum = successor.data
            node.data = minimum
            node.right = node.right.deleteNode(node.right.data)
        return node
        

#inorder Tree print function
    def printTreeInOrder(node):
        if node.left:
            node.left.printTreeInOrder()
        print node.data
        if node.right:
            node.right.printTreeInOrder()

#preorder Tree print function
    def printTreePreOrder(node):
        print node.data
        if node.left is not None:
            node.left.printTreePreOrder()
        if node.right is not None:
            node.right.printTreePreOrder()

#postorder Tree print function
    def printTreePostOrder(node):
        if node.left :
            node.left.printTreePostOrder()
        if node.right:
            node.right.printTreePostOrder()
        print node.data

        
#Record Set
class Record:
    def __init__(record, values, operations):
        record.values = values
        record.operations = operations
        
    def add_operation(record, data):
        record.operations.append(data)
        
    def add_value(record, data):
        record.values.append(data)
            

#---------------------------------------------
#------------- File Read Functions -----------
#---------------------------------------------
def processMaster():
    #Will hold record objects -- contain operations and values for tree initialization
    records = []
    record = Record([], [])
    count = 0
    master_file = open("./master.txt", "r")
    #Iterate through master
    for line in master_file:
        if line == "\n":
            records.append(record)
            count = 0
            record = Record([], [])
        elif line.find(str(-999)) != -1:
            values = line.split(",")
            for v in values:
                if int(v) != -999:
                  record.add_value(int(v))
        else:
            values = line.split(",")
            for v in values:
              if v.find("\n") == -1:
                record.add_operation(int(v))
              else:
                record.add_operation(int(v.replace("\n", "")))
    return records
            
            
    
#---------------------------------------------
#--------------- Tree Functions --------------
#---------------------------------------------

def size(root):
    if root is None:
        return 0
    elif root.left is not None or root.right is not None:
        return (size(root.left) + 1 + size(root.right))
    else:
        return 1

def numChildren(node):
    if node.right is not None and node.left is not None:
        return "2"
    elif node.right is not None or node.left is not None:
        return "1"
    else:
        return "0"

def freeTree(node):
    if node.data is not None:
        if node.left:
            freeTree(node.left)
        if node.right:
            freeTree(node.right)
        node.right = None
        node.left = None
    else:
        print "Empty Node"

def numChildrenHelper(node):
    if node.data is not None:
        if node.left:
            numChildrenHelper(node.left)
        print numChildren(node)
        if node.right:
            numChildrenHelper(node.right)
    else:
        print "Empty Tree"


def completeTasks(record):
    if record.values:
        root = Node(record.values[0])
        del record.values[0]
        #STEP 1: CREATE THE TREE
        for v in record.values:
            root.insert(v)
        #STEP 2: PRINT IN PREORDER, INORDER, POSTORDER
        print "\n--------InOrder--------"
        root.printTreeInOrder()
        print "\n--------PreOrder--------"
        root.printTreePreOrder()
        print "\n--------PostOrder--------"
        root.printTreePostOrder()
        #STEP 3: PRINT THE NUMBER OF NODES IN THE TREE
        print size(root)
        #STEP 4: PRINT THE NUMBER OF CHILDREN EACH NODE HAS -- Done inorder
        count = 0
        print "\n-------Child Count InOrder---------"
        numChildrenHelper(root)
        #STEP 5: PERFORM OPERATONS
        print "\n-------DELETE AND OTHER OPS BEING PERFORMED--------"
        for o in record.operations:
            #Set all addition operations to '+' numbers and deletion to '-'
            if(o >= 0):
                root.insert(o)
            else:
                root.deleteNode((o * -1))
        #STEP 6: PRINT AGAIN
        print "\n--------InOrder--------"
        root.printTreeInOrder()
        print "\n--------PreOrder--------"
        root.printTreePreOrder()
        print "\n--------PostOrder--------"
        root.printTreePostOrder()
        #STEP 7: CALL CHILDREN AGAIN
        print "\n-------Child Count InOrder---------"
        numChildrenHelper(root)
        #STEP 8: FREE THE TREE
        freeTree(root)


#---------------------------------------------
#--------------- Runner Functions ------------
#---------------------------------------------
records = processMaster()

for record in records:
    completeTasks(record)
