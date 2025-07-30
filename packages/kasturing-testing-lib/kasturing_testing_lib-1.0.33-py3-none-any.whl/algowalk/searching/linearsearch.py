# ------------------------------
# 1. Linear Search Code
# ------------------------------
def linear_search(arr, target):
    steps = []
    for i in range(len(arr)):
        steps.append((i, arr[i]))
        if arr[i] == target:
            return i, steps
    steps.append((-1, None))  # Not found
    return -1, steps

# ------------------------------
# 2. Static Time Complexity
# ------------------------------
# Best Case: O(1)
# Average Case: O(n)
# Worst Case: O(n)

def static_time_complexity():
    return {
        "Best Case": "O(1)",
        "Average Case": "O(n)",
        "Worst Case": "O(n)"
    }

# ------------------------------
# 3. Runtime Time Complexity (step count)
# ------------------------------
def runtime_time_complexity(steps):
    return f"O({len(steps)}) comparisons"

# ------------------------------
# 4. Space Complexity
# ------------------------------
# Static: O(1) - no extra data structures
# Dynamic: based on steps list

def space_complexity_static():
    return "O(1)"

def space_complexity_dynamic(steps):
    from sys import getsizeof
    return getsizeof(steps)  # in bytes

# ------------------------------
# 5. Plotly Step-by-Step Execution
# ------------------------------
import plotly.graph_objects as go

def visualize_linear_search(arr, steps, target):
    x = list(range(len(arr)))
    frames = []
    runtime_complexity = runtime_time_complexity(steps)
    dynamic_space = f"{space_complexity_dynamic(steps)} bytes"
    time_complexity = static_time_complexity()
    complexity_text = (
        f"<b>Time Complexity</b><br>Best: {time_complexity['Best Case']}, "
        f"Average: {time_complexity['Average Case']}, Worst: {time_complexity['Worst Case']}<br>"
        f"<b>Runtime:</b> {runtime_complexity}<br>"
        f"<b>Space:</b> Static: O(1), Dynamic: {dynamic_space}"
    )

    for step_num, (idx, val) in enumerate(steps):
        colors = ['lightgray'] * len(arr)
        if idx >= 0 and idx < len(arr):
            for i in range(idx):
                colors[i] = 'gray'  # Already checked
            colors[idx] = 'green' if val == target else 'orange'  # Current check
        title_text = f"Step {step_num + 1}: {'Found' if val == target else f'Checking index {idx}'}"
        frames.append(go.Frame(
            data=[go.Bar(x=x, y=arr, marker_color=colors)],
            name=str(step_num),
            layout=go.Layout(title_text=title_text)
        ))

    fig = go.Figure(
        data=[go.Bar(x=x, y=arr, marker_color='lightgray')],
        layout=go.Layout(
            title="Linear Search Visualization",
            xaxis_title="Index",
            yaxis_title="Value",
            margin=dict(t=80, b=160),
            annotations=[
                dict(
                    text=complexity_text,
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.25,
                    y=-0.25,
                    xanchor='center',
                    align='center',
                    font=dict(size=14)
                )
            ],
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 1000, "redraw": True}}]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}}]
                    }
                ]
            }]
        ),
        frames=frames
    )
    fig.show()