import plotly.graph_objects as go
def bubble_sort_with_steps(arr):
    steps = []
    array = arr.copy()
    n = len(array)

    def record_step(highlight=[], swapped=False, sorted_idx=None):
        steps.append({
            "array": array.copy(),
            "highlight": highlight.copy(),
            "swapped": swapped,
            "sorted_idx": sorted_idx if sorted_idx else []
        })

    record_step()  # Initial state

    for i in range(n):
        for j in range(0, n - i - 1):
            # Comparing
            record_step([j, j + 1], swapped=False)
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                # Swapped
                record_step([j, j + 1], swapped=True)
        # Mark the last element of this round as sorted
        record_step(sorted_idx=list(range(n - i, n)))

    return array, steps


import plotly.graph_objects as go

def visualize_bubble_sort_plotly(steps):
    x = list(range(len(steps[0]['array'])))
    frames = []

    for i, step in enumerate(steps):
        arr = step["array"]
        highlight = step["highlight"]
        swapped = step["swapped"]
        sorted_idx = step["sorted_idx"]

        # Color scheme
        colors = []
        for idx in range(len(arr)):
            if idx in highlight:
                colors.append("red" if swapped else "orange")  # swap = red, compare = orange
            elif idx in sorted_idx:
                colors.append("green")  # sorted = green
            else:
                colors.append("gray")  # default

        frame_title = (
            f"Step {i}: {'Swapped' if swapped else 'Comparing'} {highlight}"
            if highlight else f"Step {i}: No Action"
        )

        frames.append(go.Frame(
            data=[go.Bar(
                x=x,
                y=arr,
                marker_color=colors,
                text=[f"Value: {val}" for val in arr],
                hoverinfo="text"
            )],
            name=f"Step-{i}",
            layout=go.Layout(title=frame_title)
        ))

    # Initial state (same as first step)
    fig = go.Figure(
        data=[go.Bar(x=x, y=steps[0]['array'], marker_color='gray')],
        layout=go.Layout(
            title="Bubble Sort Visualization - Step 0",
            xaxis=dict(title='Index'),
            yaxis=dict(title='Value'),
            updatemenus=[{
                "type": "buttons",
                "buttons": [{
                    "label": "▶️ Play",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 1000, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 1000}
                    }]
                }]
            }]
        ),
        frames=frames
    )

    fig.show()