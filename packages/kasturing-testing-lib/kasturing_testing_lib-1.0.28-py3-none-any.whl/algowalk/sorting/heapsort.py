import plotly.graph_objects as go

def heap_sort_with_steps(arr):
    steps = []
    array = arr.copy()
    n = len(array)

    def record_step(note="", highlight=[], swapped=[], fixed=[]):
        steps.append({
            "heap": array.copy(),
            "note": note,
            "highlight": highlight.copy(),
            "swapped": swapped.copy(),
            "fixed": fixed.copy()
        })

    def heapify(heap, n, i, fixed_indices):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        highlight = [i]
        if l < n:
            highlight.append(l)
        if r < n:
            highlight.append(r)

        if l < n and heap[l] > heap[largest]:
            largest = l
        if r < n and heap[r] > heap[largest]:
            largest = r

        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            record_step(f"Swap {i} ⇄ {largest}", highlight=[i, largest], swapped=[i, largest], fixed=fixed_indices)
            heapify(heap, n, largest, fixed_indices)
        else:
            record_step(f"Compare {i} with children", highlight=highlight, fixed=fixed_indices)

    fixed = []

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i, fixed)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        fixed.append(i)
        record_step(f"Move max to position {i}", swapped=[0, i], fixed=fixed.copy())
        heapify(array, i, 0, fixed)

    # Final mark
    record_step("Final Heap", fixed=list(range(n)))

    return array, steps



def generate_heap_frames(steps):
    frames = []

    for i, step in enumerate(steps):
        heap = step["heap"]
        note = step["note"]
        highlight = set(step.get("highlight", []))
        swapped = set(step.get("swapped", []))
        fixed = set(step.get("fixed", []))

        x = []
        y = []
        text = []
        colors = []
        edges_x = []
        edges_y = []

        def add_node(i, depth, pos):
            if i >= len(heap):
                return
            x_pos = pos
            y_pos = -depth
            x.append(x_pos)
            y.append(y_pos)
            text.append(str(heap[i]))

            if i in swapped:
                colors.append("red")
            elif i in highlight:
                colors.append("orange")
            elif i in fixed:
                colors.append("green")
            else:
                colors.append("lightgray")

            l = 2 * i + 1
            if l < len(heap):
                x_l = pos - 1 / (2 ** (depth + 1))
                y_l = -(depth + 1)
                edges_x.extend([x_pos, x_l, None])
                edges_y.extend([y_pos, y_l, None])
                add_node(l, depth + 1, x_l)

            r = 2 * i + 2
            if r < len(heap):
                x_r = pos + 1 / (2 ** (depth + 1))
                y_r = -(depth + 1)
                edges_x.extend([x_pos, x_r, None])
                edges_y.extend([y_pos, y_r, None])
                add_node(r, depth + 1, x_r)

        add_node(0, 0, 0)

        frames.append(go.Frame(
            data=[
                go.Scatter(x=edges_x, y=edges_y, mode="lines", line=dict(color="gray")),
                go.Scatter(
                    x=x, y=y,
                    mode="markers+text",
                    text=text,
                    textposition="middle center",
                    marker=dict(size=40, color=colors, line=dict(width=2, color='darkblue'))
                )
            ],
            name=str(i),
            layout=go.Layout(title=note)
        ))

    return frames


def visualize_heap_sort_steps(steps):
    frames = generate_heap_frames(steps)

    fig = go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            title=steps[0]['note'],
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            updatemenus=[{
                "type": "buttons",
                "x": 0.25,
                "y": -0.25,
                "direction": "right",
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