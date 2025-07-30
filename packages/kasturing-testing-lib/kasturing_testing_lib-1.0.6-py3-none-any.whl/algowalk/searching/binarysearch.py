import matplotlib.pyplot as plt

def binary_search_with_steps(arr, target):
    """
    Perform binary search and record each step for visualization.

    Args:
        arr (list): A sorted list of elements to search.
        target (any): The value to search for.

    Returns:
        tuple: (index of target or -1, list of steps)
    """
    steps = []
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        steps.append({
            'array': arr.copy(),
            'left': left,
            'right': right,
            'mid': mid,
            'status': 'found' if arr[mid] == target else 'searching'
        })

        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # Final step when not found
    steps.append({
        'array': arr.copy(),
        'left': left,
        'right': right,
        'mid': -1,
        'status': 'not_found'
    })

    return -1, steps


def visualize_binary_search(steps, delay=0.8):
    """
    Visualizes binary search steps using matplotlib.
    Each step shows the full array and highlights the current mid index.

    :param steps: A list of dictionaries with search state per step.
    :param delay: Delay between frames (in seconds).
    """
    for step in steps:
        array = step['array']
        left = step['left']
        right = step['right']
        mid = step['mid']
        status = step['status']

        colors = ['gray'] * len(array)

        # Highlight left, right, and mid
        if 0 <= left < len(array): colors[left] = 'blue'
        if 0 <= right < len(array): colors[right] = 'blue'
        if 0 <= mid < len(array): colors[mid] = 'red' if status == 'searching' else 'green'

        plt.clf()
        plt.bar(range(len(array)), array, color=colors)
        plt.title(f"Binary Search - Status: {status} | Mid: {mid}")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.pause(delay)

    plt.show()