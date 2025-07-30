import plotly.graph_objects as go

def heap_sort_with_steps(arr):
    steps = []
    array = arr.copy()
    n = len(array)

    def record_step(heap, note=""):
        steps.append({
            "heap": heap.copy(),
            "note": note
        })

    def heapify(heap, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and heap[l] > heap[largest]:
            largest = l
        if r < n and heap[r] > heap[largest]:
            largest = r
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            record_step(heap, f"Heapify: swap {i} ⇄ {largest}")
            heapify(heap, n, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i)
        record_step(array, f"Build max-heap: heapify at index {i}")

    # Extract max elements
    for i in range(n - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        record_step(array, f"Swap max with index {i}")
        heapify(array, i, 0)

    return array, steps




def generate_heap_frames(steps):
    frames = []

    for i, step in enumerate(steps):
        heap = step["heap"]
        note = step["note"]

        x = []
        y = []
        text = []
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

            # left child
            l = 2 * i + 1
            if l < len(heap):
                x_l = pos - 1 / (2 ** (depth + 1))
                y_l = -(depth + 1)
                edges_x.extend([x_pos, x_l, None])
                edges_y.extend([y_pos, y_l, None])
                add_node(l, depth + 1, x_l)

            # right child
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
                go.Scatter(x=x, y=y, mode="markers+text", text=text,
                           textposition="middle center",
                           marker=dict(size=40, color='skyblue', line=dict(width=2, color='darkblue')))
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