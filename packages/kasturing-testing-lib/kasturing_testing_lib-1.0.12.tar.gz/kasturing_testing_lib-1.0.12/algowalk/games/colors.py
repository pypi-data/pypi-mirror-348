import plotly.graph_objects as go
import colorsys
import random

def visualize_vibgyor():
    vibgyor_colors = [
        {"name": "Violet", "hex": "#8F00FF"},
        {"name": "Indigo", "hex": "#4B0082"},
        {"name": "Blue",   "hex": "#0000FF"},
        {"name": "Green",  "hex": "#00FF00"},
        {"name": "Yellow", "hex": "#FFFF00"},
        {"name": "Orange", "hex": "#FF7F00"},
        {"name": "Red",    "hex": "#FF0000"},
    ]

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    for color in vibgyor_colors:
        r, g, b = hex_to_rgb(color["hex"])
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        color["lightness"] = l

    # Sort by lightness
    sorted_colors = sorted(vibgyor_colors, key=lambda x: x["lightness"])
    names_sorted = [c["name"] for c in sorted_colors]
    lightness_sorted = [c["lightness"] for c in sorted_colors]
    colors_sorted = [c["hex"] for c in sorted_colors]

    # Shuffle version
    shuffled_colors = sorted_colors.copy()
    random.shuffle(shuffled_colors)
    names_shuffled = [c["name"] for c in shuffled_colors]
    lightness_shuffled = [c["lightness"] for c in shuffled_colors]
    colors_shuffled = [c["hex"] for c in shuffled_colors]

    # Create the figure
    fig = go.Figure()

    # Add initial (sorted) bar chart
    fig.add_trace(go.Bar(x=names_sorted, y=lightness_sorted, marker_color=colors_sorted, name="Sorted"))

    # Add shuffle and reset frames
    fig.frames = [
        go.Frame(
            data=[go.Bar(x=names_shuffled, y=lightness_shuffled, marker_color=colors_shuffled)],
            name="Shuffle"
        ),
        go.Frame(
            data=[go.Bar(x=names_sorted, y=lightness_sorted, marker_color=colors_sorted)],
            name="Reset"
        )
    ]

    # Add Play + Shuffle + Reset buttons
    fig.update_layout(
        title="VIBGYOR Colors: Sorted vs Shuffled (Interactive)",
        xaxis_title="Color",
        yaxis_title="Lightness",
        yaxis=dict(range=[0, 1]),
        updatemenus=[
            {
                "type": "buttons",
                "direction": "right",
                "x": 0.1,
                "y": 1.15,
                "showactive": False,
                "buttons": [
                    {
                        "label": "Shuffle",
                        "method": "animate",
                        "args": [["Shuffle"], {"frame": {"duration": 500, "redraw": True}}]
                    },
                    {
                        "label": "Reset",
                        "method": "animate",
                        "args": [["Reset"], {"frame": {"duration": 500, "redraw": True}}]
                    }
                ]
            }
        ],
        plot_bgcolor="white"
    )

    fig.show()