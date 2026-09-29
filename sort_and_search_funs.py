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

# ------Solhee------


def partition(arr, l, h):
    i = ( l - 1 )
    x = arr[h]

    for j in range(l, h):
        if   arr[j] <= x:

            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    return (i + 1)

# Function to do Quick sort
# arr[] --> Array to be sorted,
# l  --> Starting index,
# h  --> Ending index
def quick_sort_iter(arr):
    # Nothing to sort; also the stack below needs room for at least 2 values
    if len(arr) < 2:
        return

    l = 0
    h = len(arr) - 1

    # Create an auxiliary stack
    size = h - l + 1
    stack = [0] * (size)

    # initialize top of stack
    top = -1

    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    # Keep popping from stack while is not empty
    while top >= 0:

        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = partition( arr, l, h )

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h


def quick_sort_rec(arr, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        # Separately sort elements before
        # partition and after partition
        quick_sort_rec(arr, low, pi - 1)
        quick_sort_rec(arr, pi + 1, high)

def binary_search_iter(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def binary_search_rec(arr, target, low, high):
    if low > high:
        return -1

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_rec(arr, target, mid + 1, high)
    else:
        return binary_search_rec(arr, target, low, mid - 1)


# Temporary test driver (to be removed)
if __name__ == "__main__":
    arr = [5, 2, 9, 1, 7, 3]
    quick_sort_iter(arr)
    assert arr == [1, 2, 3, 5, 7, 9]

    arr = [5, 2, 9, 1, 7, 3]
    quick_sort_rec(arr, 0, len(arr) - 1)
    assert arr == [1, 2, 3, 5, 7, 9]

    arr = [1, 2, 3, 5, 7, 9]
    assert binary_search_iter(arr, 4) == -1
    assert binary_search_rec(arr, 4, 0, 5) == -1

    assert binary_search_iter(arr, 5) == 3
    assert binary_search_rec(arr, 5, 0, 5) == 3