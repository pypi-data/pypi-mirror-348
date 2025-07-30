import plotly.graph_objects as go
import colorsys
import random

# HEX to RGB conversion
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Add lightness for sorting
def add_lightness(colors):
    for c in colors:
        r, g, b = hex_to_rgb(c["hex"])
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        c["lightness"] = round(l, 2)
    return colors

# Create shuffle frames
def create_shuffled_frames(colors, num_frames=10):
    frames = []
    for i in range(num_frames):
        shuffled = colors.copy()
        random.shuffle(shuffled)
        names = [c["name"] for c in shuffled]
        lightness = [c["lightness"] for c in shuffled]
        hexes = [c["hex"] for c in shuffled]
        frames.append(go.Frame(
            data=[go.Bar(x=names, y=lightness, marker_color=hexes)],
            name=f"Shuffle-{i}"
        ))
    return frames

# 🎮 Launch the game with one function call
def launch_vibgyor_game():
    vibgyor_colors = [
        {"name": "Violet", "hex": "#8F00FF"},
        {"name": "Indigo", "hex": "#4B0082"},
        {"name": "Blue",   "hex": "#0000FF"},
        {"name": "Green",  "hex": "#00FF00"},
        {"name": "Yellow", "hex": "#FFFF00"},
        {"name": "Orange", "hex": "#FF7F00"},
        {"name": "Red",    "hex": "#FF0000"},
    ]

    base_with_lightness = add_lightness(vibgyor_colors.copy())
    initial = sorted(base_with_lightness, key=lambda x: x["lightness"])
    x_init = [c["name"] for c in initial]
    y_init = [c["lightness"] for c in initial]
    colors_init = [c["hex"] for c in initial]

    frames = create_shuffled_frames(base_with_lightness, num_frames=20)

    fig = go.Figure(
        data=[go.Bar(x=x_init, y=y_init, marker_color=colors_init)],
        layout=go.Layout(
            title="🌈 VIBGYOR Shuffle Game",
            xaxis_title="Color",
            yaxis_title="Lightness",
            yaxis=dict(range=[0, 1]),
            updatemenus=[{
                "type": "buttons",
                "x": 0.1,
                "y": 1.2,
                "direction": "right",
                "buttons": [
                    {
                        "label": "🔀 Shuffle!",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": 0, "redraw": True},
                            "fromcurrent": True,
                            "mode": "immediate",
                            "transition": {"duration": 300}
                        }]
                    }
                ]
            }]
        ),
        frames=frames
    )

    fig.show()