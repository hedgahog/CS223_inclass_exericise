def insertionSortRecursive(arr,n):
    # base case
    if n <= 1:
        return
    # Sort first n-1 elements
    insertionSortRecursive(arr, n-1)
    # Insert last element at its correct position in sorted array.
    last = arr[n-1]
    j = n-2
    # Move elements of arr[0..i-1], that are greater than key, to one position ahead
    # of their current position
    while (j >= 0 and arr[j] > last):
        arr[j+1] = arr[j]
        j = j-1
    arr[j+1] = last

def insertionSortIterative(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        # Move elements of arr[0..i-1], that are greater than key, to one position ahead
        # of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def iterative_selection_sort(arr): # write two loops
    n = len(arr)
    for i in range(n-1): # first loop iterates through array
        min_idx = i
        print(min_idx)
    for j in range(i+1, n):
        if arr[j] < arr[min_idx]:
            min_idx = j

