#sortingUtils.py
from multiprocessing import Pool #Library for parallelism and multiprocessing

def merge(left, right):
    result = []
    i = j = 0
    
    #Comparing both sublists, and adding the smaller element to result
    while i < len(left) and j < len(right): 
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    #Appending any remaining elements, one of these will be empty
    result.extend(left[i:])
    result.extend(right[j:])
    return result

#Standard recursively done mergesort implementation
def sequentialMergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = sequentialMergeSort(arr[:mid]) #Recursively sort left half to mid
    right = sequentialMergeSort(arr[mid:]) #Recursively sort right half from mid
    return merge(left, right)              #Merge both halves

def parallelMergeSort(arr, processCount):
    #If the array is relatively small or requested processes are less than or equal to 1 then use sequentialMergeSort
    if len(arr) <= 10000 or processCount <= 1:
        return sequentialMergeSort(arr)

    #Size of chunk which every process will be working with
    chunkSize = len(arr) // processCount
    
    #A list of lists a little bit harder to understand, but basically contains all chunks possible
    chunks = [arr[i:i + chunkSize] for i in range(0, len(arr), chunkSize)]

    #Create a pool of worker processes that are equal to processCount
    with Pool(processCount) as pool:
        #Each worker receives a chunk and runs sequentialMergeSort on it, the result is sortedChunks, which is a list of lists
        sortedChunks = pool.map(sequentialMergeSort, chunks)

    while len(sortedChunks) > 1: #Keep merging until only 1 element is left
        temp = [] #Temporary list to keep merged chunks this iteration
        for i in range(0, len(sortedChunks), 2): #Go through sorted chunks in pairs
            if i + 1 < len(sortedChunks): #If i and i+1 exists then merge them
                temp.append(merge(sortedChunks[i], sortedChunks[i + 1]))
            else:                         #If i and i+1 does not exist then just append the list to temp
                temp.append(sortedChunks[i])
        sortedChunks = temp               #Replace sorted chunks with the current merged list

    return sortedChunks[0] #Return first element from sortedChunks, which is the array we need