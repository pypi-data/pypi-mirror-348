import plotly.graph_objects as go
import colorsys

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

    # Add lightness value to each color
    for color in vibgyor_colors:
        r, g, b = hex_to_rgb(color["hex"])
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        color["lightness"] = l

    # Sort colors by lightness
    sorted_colors = sorted(vibgyor_colors, key=lambda x: x["lightness"])

    # Prepare plot data
    names = [c["name"] for c in sorted_colors]
    lightness = [c["lightness"] for c in sorted_colors]
    colors = [c["hex"] for c in sorted_colors]

    # Plot
    fig = go.Figure(
        data=[go.Bar(x=names, y=lightness, marker_color=colors, text=colors, hoverinfo='text+y')]
    )
    fig.update_layout(
        title="VIBGYOR Colors Sorted by Lightness",
        xaxis_title="Color",
        yaxis_title="Lightness",
        yaxis=dict(range=[0, 1]),
        plot_bgcolor="white"
    )
    fig.show()