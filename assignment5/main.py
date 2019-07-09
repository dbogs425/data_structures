#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#                                                $
#  Assignment 5 -- Daniel Bolognino -- CISC 3130 $
#                                                $
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#---------------------------------------------
#--------------- Constructors ----------------
#---------------------------------------------

class Node(object):
    def __init__(node, data):
        node.data = data
        node.parent = None
        node.children = []
    
    def addChild(node, child):
        node.children.append(child)
    
    def setParent(node, parent):
        node.parent = parent

class Record:
    def __init__(record, name, numChildren):
        record.name = name
        record.numChildren = numChildren

#---------------------------------------------
#------------ File Read Functions ------------
#---------------------------------------------

#Tree number (1-5) to read tree from master
def readMaster(treeNum):
    count = 0
    records = [];
    master_file = open("./master.txt", "r")
    for line in master_file:
        if count == treeNum:
            values = line.split()
            if values:
                record = Record(values[0], int(values[1]))
                records.append(record)
            else:
                return records
        elif line == "\n":
            count += 1
    return records

def createTree(family, last, numBrothers):
    if len(family) != 0:
        #First step
        if last == None:
            father = Node(family[0].name)
            for x in range(family[0].numChildren):
                child = Node(family[x].name)
                child.setParent(father)
                father.addChild(child)
            family.pop(0)
            return createTree(family, father, len(father.children))
        #Second step
        elif numBrothers != 0:
            father = Node(family[0].name)
            numChildren = family[0].numChildren
            father.setParent(last)
            for x in range(numChildren):
                child = Node(family[x + numBrothers].name)
                child.setParent(father)
                father.addChild(child)
            if numBrothers != 1:
                numBrothers -= 1
            family.pop(0)
        if len(family) == 1:
            return last
        else:
            return createTree(family, father, numBrothers)
    else:
        return None

#Function 1: print the father
def whoIsFather(node):
    return node.parent

#Function 2: print the sons
def whoAreSons(node):
    childNames = []
    if len(node.children):
        for child in node.children:
            childNames.append(child.data)
    else:
        childNames = ["No Children"]
    return childNames

def whoIsGrandpa(node):
    if node.parent:
        dad = node.parent
        if dad.parent:
            return dad.parent.data
    else:
        return "No Grandpa"

#---------------------------------------------
#------------ Runner Functions ---------------
#---------------------------------------------

#here's a loop to do the things:
for x in range(5):
    #Step 1: read values from master
    family = readMaster(x)

    #Step 2: create tree, you now have the last node in the tree
    last = createTree(family, None, 0)


    #Step 3: Do things to the tree
    #1) Who is the father
    print "-------Father of " + last.data + "--------\n"
    father = whoIsFather(last)
    print father.data + "\n"
    #2) Print out all the sons of the father
    childNames = whoAreSons(father)
    print "--------Children--------\n"
    for child in childNames:
        print child + "\n"
        #3)Who is grandfather of p?
        grandpa = whoIsGrandpa(last)
        print "--------Grandpa--------\n" + grandpa

