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

import plotly.graph_objects as go

def visualize_bubble_sort_plotly(steps):
    x = list(range(len(steps[0]['array'])))
    frames = []

    for i, step in enumerate(steps):
        arr = step["array"]
        highlight = step["highlight"]
        swapped = step["swapped"]
        sorted_idx = step["sorted_idx"]

        colors = []
        for idx in range(len(arr)):
            if idx in highlight:
                colors.append("red" if swapped else "orange")
            elif idx in sorted_idx:
                colors.append("green")
            else:
                colors.append("gray")

        frames.append(go.Frame(
            data=[go.Bar(
                x=x,
                y=arr,
                marker_color=colors,
                text=[f"Val: {val}" for val in arr],
                hoverinfo="text"
            )],
            name=f"{i}",
            layout=go.Layout(title_text=f"Step {i}: {'Swapped' if swapped else 'Comparing'} {highlight}")
        ))

    fig = go.Figure(
        data=[go.Bar(
            x=x,
            y=steps[0]['array'],
            marker_color=['gray'] * len(x),
            text=[f"Val: {val}" for val in steps[0]['array']],
            hoverinfo="text"
        )],
        layout=go.Layout(
            title="Bubble Sort Visualization - Step 0",
            xaxis=dict(title='Index'),
            yaxis=dict(title='Value'),
            updatemenus=[{
                "type": "buttons",
                "direction": "right",
                "x": 0.1,
                "y": 1.15,
                "showactive": False,
                "buttons": [
                    {
                        "label": "▶️ Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": 1000, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 1000}
                        }]
                    },
                    {
                        "label": "⏸️ Pause",
                        "method": "animate",
                        "args": [[None], {
                            "mode": "immediate",
                            "frame": {"duration": 0, "redraw": False},
                            "transition": {"duration": 0}
                        }]
                    }
                ]
            }]
        ),
        frames=frames
    )

    fig.show()