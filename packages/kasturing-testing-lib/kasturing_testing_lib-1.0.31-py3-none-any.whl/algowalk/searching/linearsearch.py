import time
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display

# ========================
# Step Tracker Class
# ========================
class StepTracker:
    def __init__(self):
        self.steps = []

    def log(self, arr, index, current):
        self.steps.append({
            'arr': arr.copy(),
            'index': index,
            'current': current
        })

    def get_steps(self):
        return self.steps

# ========================
# Linear Search Algorithm
# ========================
def linear_search(arr, target, tracker=None):
    for idx, val in enumerate(arr):
        if tracker:
            tracker.log(arr, idx, val)
        if val == target:
            return idx
    return -1

# ========================
# Plotly Visualization
# ========================
def visualize_linear_search_plotly(steps, target):
    slider = widgets.IntSlider(value=0, min=0, max=len(steps)-1, step=1, description='Step')
    out = widgets.Output()

    def plot_step(step):
        with out:
            out.clear_output(wait=True)
            step_data = steps[step]
            arr = step_data['arr']
            index = step_data['index']
            current = step_data['current']
            colors = ['gray'] * len(arr)
            colors[index] = 'green' if current == target else 'blue'

            fig = go.Figure(
                data=[
                    go.Bar(y=arr, marker_color=colors)
                ],
                layout_title_text=f"Step {step+1}: Checking index {index} (value = {current})"
            )
            fig.update_layout(
                xaxis_title="Index",
                yaxis_title="Value",
                bargap=0.2,
                showlegend=False
            )
            fig.show()

    widgets.interact(plot_step, step=slider)
    display(out)

# ========================
def linear_search_with_steps(arr, target):
    tracker = StepTracker()
    result = linear_search(arr, target, tracker)
    return result, tracker.get_steps()
# ========================


