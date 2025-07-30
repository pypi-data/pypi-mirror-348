import streamlit as st
import plotly.graph_objects as go
import colorsys
import random

# Define VIBGYOR color palette
vibgyor_colors = [
    {"name": "Violet", "hex": "#8F00FF"},
    {"name": "Indigo", "hex": "#4B0082"},
    {"name": "Blue",   "hex": "#0000FF"},
    {"name": "Green",  "hex": "#00FF00"},
    {"name": "Yellow", "hex": "#FFFF00"},
    {"name": "Orange", "hex": "#FF7F00"},
    {"name": "Red",    "hex": "#FF0000"},
]

# Convert HEX to RGB and calculate lightness
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def add_lightness(colors):
    for c in colors:
        r, g, b = hex_to_rgb(c["hex"])
        h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
        c["lightness"] = round(l, 2)
    return colors

# Plot shuffled colors using Plotly
def plot_colors(colors):
    names = [c["name"] for c in colors]
    lightness = [c["lightness"] for c in colors]
    hexes = [c["hex"] for c in colors]

    fig = go.Figure(
        data=[go.Bar(x=names, y=lightness, marker_color=hexes, text=hexes, hoverinfo="text+y")],
    )

    fig.update_layout(
        title="🌈 VIBGYOR Shuffle — Click to Mix the Rainbow!",
        xaxis_title="Colors",
        yaxis_title="Lightness (Fun Meter 🌟)",
        yaxis=dict(range=[0, 1]),
        plot_bgcolor="white",
        font=dict(size=18),
    )
    return fig

# 🎮 Streamlit App Layout
st.set_page_config(page_title="Rainbow Shuffle", page_icon="🌈")
st.title("🌈 VIBGYOR Color Shuffler")
st.markdown("Let’s **play with colors!** Click the shuffle button to mix the rainbow!")

if st.button("🔀 Shuffle Rainbow!"):
    shuffled = add_lightness(vibgyor_colors.copy())
    random.shuffle(shuffled)
else:
    shuffled = add_lightness(vibgyor_colors.copy())

# Display the chart
fig = plot_colors(shuffled)
st.plotly_chart(fig, use_container_width=True)