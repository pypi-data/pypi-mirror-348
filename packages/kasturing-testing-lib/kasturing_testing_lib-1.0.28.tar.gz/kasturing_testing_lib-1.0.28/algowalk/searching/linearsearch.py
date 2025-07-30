import plotly.graph_objects as go


def linear_search_with_steps(arr, target):
    steps = []

    for i in range(len(arr)):
        status = "found" if arr[i] == target else "searching"
        steps.append({
            "array": arr.copy(),
            "current": i,
            "target": target,
            "status": status
        })
        if arr[i] == target:
            return i, steps

    # Not found
    steps.append({
        "array": arr.copy(),
        "current": -1,
        "target": target,
        "status": "not_found"
    })

    return -1, steps


def visualize_linear_search(steps):
    x = list(range(len(steps[0]['array'])))
    frames = []

    for i, step in enumerate(steps):
        array = step["array"]
        current = step["current"]
        status = step["status"]

        colors = ['gray'] * len(array)
        if 0 <= current < len(array):
            colors[current] = 'green' if status == 'found' else 'red'

        title_text = (
            f"Step {i}: Element {'found' if status == 'found' else 'checking'} at index {current}"
            if current >= 0 else "Element not found"
        )

        frames.append(go.Frame(
            data=[go.Bar(x=x, y=array, marker_color=colors)],
            name=str(i),
            layout=go.Layout(title_text=title_text)
        ))

    # Initial bar
    fig = go.Figure(
        data=[go.Bar(x=x, y=steps[0]["array"], marker_color="gray")],
        layout=go.Layout(
            title="Linear Search Visualization",
            xaxis_title="Index",
            yaxis_title="Value",
            margin=dict(t=80, b=100),
            updatemenus=[{
                "type": "buttons",
                "direction": "right",
                "x": 0.25,
                "y": -0.25,
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
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }]
                    }
                ]
            }]
        ),
        frames=frames
    )

    fig.show()