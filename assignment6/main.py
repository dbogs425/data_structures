#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#                                                $
#  Assignment 6 -- Daniel Bolognino -- CISC 3130 $
#                                                $
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


#---------------------------------------------
#--------------- Constructors ----------------
#---------------------------------------------

#Storage of a result from a function (avoid "ValueError")
class SortReturn:
    def __init__(r, nums, comparisons, swaps):
        r.nums = nums
        r.comparisons = comparisons
        r.swaps = swaps

class InsertReturn:
    def __init__(r, nums, swaps):
        r.nums = nums
        r.swaps = swaps

#---------------------------------------------
#--------------- Sort Functions --------------
#---------------------------------------------

#Function 1 (Stupid Sort): Bubble Sort
def bubble_sort(nums):
    #Keep track of number of times comparisons are made
    swaps = 0
    count = 0
    comparisons = 0
    length = len(nums)
    #Start at end of array work back as array is sorted
    for x in range(length-1, 0, -1):
        #From the number to the end of the array (end is sorted)
        for i in range(x):
            #If first number is bigger:
            if nums[i] > nums[i+1]:
                #Set temp value to nums at index i
                temp = nums[i]
                #Swap out current value for next value, and set current to the next
                nums[i] = nums[i+1]
                nums[i+1] = temp
                #Increase count by 1 each time a swap is made
                swaps += 1
        count += 1
    val = SortReturn(nums, count, swaps)
    return val

#Function 2 (Great Sort): QuickSort
def quicksort(nums):
    ltPivot = []
    gtPivot = []
    eqPivot = []
    #If array has only one element or is empty return array (base case)
    if len(nums) <= 1:
        return nums
    #Otherwise, sort   
    else:
        pivot = nums[0]
        for num in nums:
            if num < pivot:
                #If less than, put in lt array
                ltPivot.append(num)
            #If equal put in eqPivot array
            elif num == pivot:
                eqPivot.append(num)
            #If greater, put in gt array
            else:
                gtPivot.append(num)
        #After loop recurse -- sort lt and gt array same way until 1 element, then concat all 3 arrays
        return quicksort(ltPivot) + eqPivot + quicksort(gtPivot)

#Function 3: Another sort (insertion sort)
def insertionSort(nums, swaps):
    if len(nums) >= 1:
        # Traverse through 1 to len(nums) 
        for i in range(1, len(nums)): 
            key = nums[i] 
            #Start with 0, and compare uuntil in proper position 
            x = i-1
            #If num in right spot, then exit, if not then keep going until x gets to 0
            while x >=0 and key < nums[x] : 
                #Swap nums
                nums[x+1] = nums[x]
                x -= 1
                swaps += 1
            #Add 1 to key since number in in right spot
            nums[x+1] = key
    isReturn = InsertReturn(nums, swaps)
    return isReturn

#---------------------------------------------
#------------- File read function ------------
#---------------------------------------------
def read_master(isFirst):
    nums = []
    count = 0
    master_file = open("./master.txt", "r")
    tempNums = []
    for line in master_file:
        x = line.split(" ")
        if x[0] != "---------":
            tempNums.append(int(line))
        else:
            if isFirst:
                sw = {
                    0: "---------Almost Sorted 10---------",
                    1: "---------Random 10---------",
                    2: "---------Reverse 10---------",
                    3: "---------Almost Sorted 50---------",
                    4: "---------Random 50---------",
                    5: "---------Reverse 50---------",
                    6: "---------Almost Sorted 100---------",
                    7: "---------Random 100---------",
                    8: "---------Reverse 100---------"
                }
                print sw.get(count)
                for x in tempNums:
                    print str(x)
            nums.append(tempNums)
            tempNums = []
            count += 1
    return nums

def printArray(oldData, s):
    nums = oldData
    if s  == False:
        print "--------UNSORTED LIST-------\n"
        print "--------SORTED LIST-------\n"
    for num in nums:
        #If unsorted print the following:
        print str(num)



#---------------------------------------------
#-------------- Runner functions -------------
#---------------------------------------------
nums = read_master(True)
count = 1
bsSwaps = []
for x in nums:
    print "----------------BUBBLE SORT----------------\nDATASET NUMBER: " + str(count)
    val = bubble_sort(x)
    print "Number of swaps for Bubble Sort: " + str(val.swaps)
    print "Number of comparisons for Bubble Sort: " + str(val.comparisons)
    printArray(val.nums, True)
    count += 1
    bsSwaps.append(val.swaps)


nums = read_master(False)
count = 1
for x in nums:
    print "----------------QUICK SORT----------------\nDATASET NUMBER: " + str(count)
    val = quicksort(x)
    printArray(val, True)
    count += 1

nums = read_master(False)
count = 1
isSwaps = []
for x in nums:
    print "----------------INSERTION SORT----------------\nDATASET NUMBER: " + str(count)
    val = insertionSort(x, 0)
    print "Number of swaps for Insertion Sort: " + str(val.swaps)
    printArray(val.nums, True)
    count += 1
    isSwaps.append(val.swaps)

for x in range(len(isSwaps)):
    if isSwaps > bsSwaps:
        print "SORT " + str(x + 1) + " Bubble Sort More Efficeint"
    elif isSwaps < bsSwaps:
        print "SORT " + str(x + 1) + " Insertion Sort More Efficeint"
    else:
        print "Bubble Sort and Insertion Sort Equally Bad for set " + str(x + 1)
