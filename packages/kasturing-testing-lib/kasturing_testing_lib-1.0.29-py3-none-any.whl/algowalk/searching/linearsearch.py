import plotly.graph_objects as go


def linear_search_with_steps(arr, target):
    steps = []
    comparisons = 0
    complexity_formula = f"O(n)"

    for i in range(len(arr)):
        comparisons += 1
        status = "found" if arr[i] == target else "searching"
        steps.append({
            "array": arr.copy(),
            "current": i,
            "target": target,
            "status": status,
            "step_num": comparisons
        })
        if arr[i] == target:
            return i, steps, comparisons, complexity_formula

    # Not found
    steps.append({
        "array": arr.copy(),
        "current": -1,
        "target": target,
        "status": "not_found",
        "step_num": comparisons
    })

    return -1, steps, comparisons, complexity_formula

import plotly.graph_objects as go

def visualize_linear_search(steps, comparisons, complexity):
    x = list(range(len(steps[0]['array'])))
    frames = []

    for i, step in enumerate(steps):
        array = step["array"]
        current = step["current"]
        status = step["status"]
        step_num = step["step_num"]

        colors = ['gray'] * len(array)
        if 0 <= current < len(array):
            colors[current] = 'green' if status == 'found' else 'red'

        title_text = (
            f"Step {i}: Checking index {current}"
            if current >= 0 else "Element not found"
        )

        explanation = (
            f"🔁 Iterations: {step_num}<br>"
            f"🔍 Target: {step['target']}<br>"
            f"📈 Worst-case Complexity: {complexity}"
        )

        frames.append(go.Frame(
            data=[go.Bar(x=x, y=array, marker_color=colors)],
            name=str(i),
            layout=go.Layout(
                title_text=title_text,
                annotations=[
                    dict(
                        text=explanation,
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.28,
                        xanchor='center',
                        align='center',
                        font=dict(size=14)
                    )
                ]
            )
        ))

    fig = go.Figure(
        data=[go.Bar(x=x, y=steps[0]["array"], marker_color="gray")],
        layout=go.Layout(
            title="Linear Search Visualization",
            xaxis_title="Index",
            yaxis_title="Value",
            margin=dict(t=80, b=120),
            annotations=[
                dict(
                    text=f"🔁 Iterations: 1<br>🔍 Target: {steps[0]['target']}<br>📈 Worst-case Complexity: {complexity}",
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=-0.28,
                    xanchor='center',
                    align='center',
                    font=dict(size=14)
                )
            ],
            updatemenus=[{
                "type": "buttons",
                "direction": "right",
                "x": 0.25,
                "y": -0.4,
                "buttons": [
                    {
                        "label": "▶️ Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": 700, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 300}
                        }]
                    },
                    {
                        "label": "⏮️ Prev",
                        "method": "animate",
                        "args": [["-1"], {
                            "mode": "immediate",
                            "frame": {"duration": 0, "redraw": True},
                            "transition": {"duration": 0}
                        }]
                    },
                    {
                        "label": "⏭️ Next",
                        "method": "animate",
                        "args": [["1"], {
                            "mode": "immediate",
                            "frame": {"duration": 0, "redraw": True},
                            "transition": {"duration": 0}
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