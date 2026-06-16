import random
import string
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import math

def convertToFt(v):
    a = v / 2.54
    b = math.floor(a / 12)
    c = round(a - (b * 12))
    return str(b) + "'" + str(c)

def makeText(v):
    return str(v) + " cm / " + convertToFt(v)

def makeHoverText(v):
    return (
        f"<b>{v['name']}</b><br>"
        f"{makeText(v['height'])}<br>"
        f"By: {v['creator_name']}"
    )

def getColor(v):
    if v < 90:
        return "blue"
    elif v < 180:
        return "lime"
    else:
        return "red"

data = pd.read_csv("data.csv")
data = pd.DataFrame(data)
data = data.sort_values(by=['height'])
color = [getColor(i) for i in data["height"]]
texts = [makeText(i) for i in data["height"]]
hovertexts = data.apply(makeHoverText, axis=1)

fig = make_subplots(
    rows=2, 
    cols=2, 
    subplot_titles=("All", "Regular", "Micro", "Colossal")
)

fig.add_trace(go.Bar(
    x=data["height"],
    y=data["name"],
    orientation='h',
    marker_color = color,
    text = texts,
    hovertext=hovertexts,
    hovertemplate="%{hovertext}<extra></extra>"
), row=1, col=1)

ndata = data[(data['height'] < 90)]
ncolor = [getColor(i) for i in ndata["height"]]
ntexts = [makeText(i) for i in ndata["height"]]
nhovertexts = ndata.apply(makeHoverText, axis=1)

fig.add_trace(go.Bar(
    x=ndata["height"],
    y=ndata["name"],
    orientation='h',
    marker_color = ncolor,
    text = ntexts,
    hovertext=nhovertexts,
    hovertemplate="%{hovertext}<extra></extra>"
), row=2, col=1)

ndata = data[(data['height'] >= 90) & (data['height'] < 180)]
ncolor = [getColor(i) for i in ndata["height"]]
ntexts = [makeText(i) for i in ndata["height"]]
nhovertexts = ndata.apply(makeHoverText, axis=1)

fig.add_trace(go.Bar(
    x=ndata["height"],
    y=ndata["name"],
    orientation='h',
    marker_color = ncolor,
    text = ntexts,
    hovertext=nhovertexts,
    hovertemplate="%{hovertext}<extra></extra>"
), row=1, col=2)

ndata = data[(data['height'] >= 180)]
ncolor = [getColor(i) for i in ndata["height"]]
ntexts = [makeText(i) for i in ndata["height"]]
nhovertexts = ndata.apply(makeHoverText, axis=1)

fig.add_trace(go.Bar(
    x=ndata["height"],
    y=ndata["name"],
    orientation='h',
    marker_color = ncolor,
    text = ntexts,
    hovertext=nhovertexts,
    hovertemplate="%{hovertext}<extra></extra>"
), row=2, col=2)

fig.add_vline(
    x=90,
    line_width=3,
    line_dash="dash",
    line_color="blue",
    layer="below",
    row=1, col=1
)
fig.add_vline(
    x=180,
    line_width=3,
    line_dash="dash",
    line_color="lime",
    layer="below",
    row=1, col=1
)

fig.update_yaxes(
    row=2, col=1, 
    type='category', 
    categoryorder='array', 
    categoryarray=ndata["name"]
)

fig.update_layout(
    title_text="ZOR Community Protogen Height Chart",
    width=1200*2,
    height=900*2,
    margin=dict(l=40, r=40, t=80, b=40),
    showlegend=False
)

fig.write_html("index.html")
print("Done")
