def binary_search(arr, target):
    """
    Perform binary search on a sorted array to find the index of a target value.

    Args:
        arr (list): A sorted list of elements to search.

    Returns:
        int: The index of the target value if found, otherwise -1.
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Check if the target is present at mid
        if arr[mid] == target:
            return mid
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        # If target is smaller, ignore right half
        else:
            right = mid - 1

    # Target was not found in the array
    return -1
