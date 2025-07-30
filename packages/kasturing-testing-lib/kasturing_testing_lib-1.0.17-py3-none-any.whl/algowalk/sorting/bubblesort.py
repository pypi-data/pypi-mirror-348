import plotly.graph_objects as go
def bubble_sort_with_steps(arr):
    """
    Perform bubble sort and record each step for visualization.

    Args:
        arr (list): A list of elements to sort.

    Returns:
        tuple: (sorted_array, steps)
    """
    steps = []
    array = arr.copy()
    n = len(array)

    def record_step(highlight=[]):
        steps.append({
            "array": array.copy(),
            "highlight": highlight.copy()
        })

    record_step()  # initial state

    for i in range(n):
        for j in range(0, n - i - 1):
            record_step([j, j + 1])
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                record_step([j, j + 1])  # record after swap

    return array, steps



def visualize_bubble_sort_plotly(steps):
    x = list(range(len(steps[0]['array'])))
    frames = []

    for i, step in enumerate(steps):
        array = step["array"]
        highlight = step["highlight"]
        colors = ['gray'] * len(array)
        for idx in highlight:
            if 0 <= idx < len(array):
                colors[idx] = 'red'

        frames.append(go.Frame(
            data=[go.Bar(x=x, y=array, marker_color=colors)],
            name=f"Step {i}"
        ))

    fig = go.Figure(
        data=[go.Bar(x=x, y=steps[0]["array"], marker_color='gray')],
        layout=go.Layout(
            title="Bubble Sort Visualization (Plotly)",
            xaxis_title="Index",
            yaxis_title="Value",
            updatemenus=[{
                "type": "buttons",
                "buttons": [{
                    "label": "▶️ Play",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 300, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 100}
                    }]
                }]
            }]
        ),
        frames=frames
    )

    fig.show()