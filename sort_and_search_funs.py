def insertionSortRecursive(arr, n):
    # base case
    if n <= 1:
        return
    # Sort first n-1 elements
    insertionSortRecursive(arr, n - 1)
    # Insert last element at its correct position in sorted array.
    last = arr[n - 1]
    j = n - 2
    # Move elements of arr[0..i-1], that are greater than key, to one position ahead
    # of their current position
    while (j >= 0 and arr[j] > last):
        arr[j + 1] = arr[j]
        j = j - 1
    arr[j + 1] = last


def insertionSortIterative(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1], that are greater than key, to one position ahead
        # of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def iterative_selection_sort(arr):  # write two loops
    n = len(arr)
    for i in range(n - 1):  # first loop iterates through array
        min_idx = i
        for j in range(i + 1, n):  # second loop finds the smallest of the unsorted rest
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Put the smallest element at the end of the sorted part
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


def recursive_selection_sort(arr, i, n):
    # base case: 0 or 1 unsorted elements left
    if i >= n - 1:
        return
    # Find the smallest element of arr[i..n-1]
    min_idx = i
    for j in range(i + 1, n):
        if arr[j] < arr[min_idx]:
            min_idx = j
    # Put it at the end of the sorted part, then sort the rest
    arr[i], arr[min_idx] = arr[min_idx], arr[i]
    recursive_selection_sort(arr, i + 1, n)


def partition(arr, l, h):
    i = (l - 1)
    x = arr[h]

    for j in range(l, h):
        if arr[j] <= x:
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
        p = partition(arr, l, h)

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p - 1 > l:
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


# Merge the sorted halves arr[l..m] and arr[m+1..h] back into arr[l..h]
def merge(arr, l, m, h):
    left = arr[l:m + 1]
    right = arr[m + 1:h + 1]

    i = 0
    j = 0
    k = l

    while i < len(left) and j < len(right):
        # <= keeps equal elements in their original order
        if left[i] <= right[j]:
            arr[k] = left[i]
            i = i + 1
        else:
            arr[k] = right[j]
            j = j + 1
        k = k + 1

    # Copy whatever is left of either half
    while i < len(left):
        arr[k] = left[i]
        i = i + 1
        k = k + 1
    while j < len(right):
        arr[k] = right[j]
        j = j + 1
        k = k + 1


def merge_sort_rec(arr, low, high):
    if low < high:
        mid = (low + high) // 2

        # Sort both halves, then merge them
        merge_sort_rec(arr, low, mid)
        merge_sort_rec(arr, mid + 1, high)
        merge(arr, low, mid, high)


def merge_sort_iter(arr):
    n = len(arr)

    # Bottom-up: merge runs of size 1, then 2, 4, 8, ...
    size = 1
    while size < n:
        for low in range(0, n - size, 2 * size):
            mid = low + size - 1
            high = min(low + 2 * size - 1, n - 1)
            merge(arr, low, mid, high)
        size = size * 2


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
