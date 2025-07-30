import plotly.graph_objects as go

def heap_sort_with_steps(arr):
    """
    Perform heap sort and record heap state after each operation.
    Returns:
        sorted array, steps (list of heap snapshots)
    """
    steps = []

    def record_step(heap, note=""):
        steps.append({
            "heap": heap.copy(),
            "note": note
        })

    def heapify(heap, n, i):
        largest = i
        l = 2*i + 1
        r = 2*i + 2

        if l < n and heap[l] > heap[largest]:
            largest = l
        if r < n and heap[r] > heap[largest]:
            largest = r
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            record_step(heap, f"Heapify swap: {i} ⇄ {largest}")
            heapify(heap, n, largest)

    n = len(arr)
    array = arr.copy()

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i)
        record_step(array, f"Heapify at {i}")

    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]  # move max to end
        record_step(array, f"Swap max with index {i}")
        heapify(array, i, 0)

    return array, steps




def visualize_heap_tree(heap, note=""):
    """
    Visualizes a binary heap as a tree using Plotly.
    """
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

        # Left child
        l = 2*i + 1
        if l < len(heap):
            x_l = pos - 1/(2**(depth+1))
            y_l = -(depth + 1)
            edges_x.extend([x_pos, x_l, None])
            edges_y.extend([y_pos, y_l, None])
            add_node(l, depth + 1, x_l)

        # Right child
        r = 2*i + 2
        if r < len(heap):
            x_r = pos + 1/(2**(depth+1))
            y_r = -(depth + 1)
            edges_x.extend([x_pos, x_r, None])
            edges_y.extend([y_pos, y_r, None])
            add_node(r, depth + 1, x_r)

    add_node(0, 0, 0)

    edge_trace = go.Scatter(
        x=edges_x, y=edges_y,
        line=dict(width=2, color='gray'),
        hoverinfo='none',
        mode='lines'
    )

    node_trace = go.Scatter(
        x=x, y=y,
        mode='markers+text',
        text=text,
        textposition="middle center",
        marker=dict(size=40, color='skyblue', line=dict(width=2, color='darkblue')),
        hoverinfo='text'
    )

    layout = go.Layout(
        title=note,
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=60, b=0),
        height=500
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    fig.show()