from pydoc import classname
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import math
import os

# Project
import utils.ntg_data as ntg_data
import utils.ntg_colors as ntg_colors

app = Dash(__name__)

df = ntg_data.load_data()

app.layout = html.Div([
    html.Div([
        html.Div([html.H1("LISE Analyzer")],className="app-header--title"),
    ], className="app-header"
    ),
    # Data Picker
    html.Div([
        html.Div([
            html.H4("Y axis"),
            dcc.Dropdown(
                ntg_data.col_results[1:],
                'Total Energy',
                id='yaxis-data'
            ),
            html.Div([
                dcc.RadioItems(
                    ['linear', 'log'],
                    'linear',
                    id='yaxis-type',
                    inline=True
                )], className="data-picker--yaxis-type"
            ),
        ], className="data-picker--yaxis"),


        html.Div([
            html.H4("X axis"),
            dcc.Dropdown(
                ['Time', 'Distance'],  # ntg_data.col_results,
                'Time',
                id='xaxis-data'
            ),
            html.Div([
                dcc.RadioItems(
                    ['linear', 'log'],
                    'linear',
                    id='xaxis-type',
                    inline=True
                )], className="data-picker--xaxis-type"
            ),
        ], className="data-picker--xaxis"),

        html.Div([
            html.H4("Colorscale"),
            html.Div([
            dcc.Dropdown(
                id='colorscale',
                options=ntg_colors.colorscales,
                value='ntg',
            )],className="data-picker-colorscale"),
        ], className="data-picker-colorscale-div")

    ], className="data-picker"
    ),  # Data Picker

    # Graph
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id="indicator-graphic")],className="graph-graph"),
        ], className="graph"),

        # html.Div([
        #     dcc.Slider(
        #         df[0]['Total Energy'].min(),
        #         df[0]['Total Energy'].max(),
        #         step=None,
        #         id='xrange-slider',
        #         value=df['Total Energy'].max(),
        #         marks=None,
        #     )
        # ], style={'width': '80%', 'flush': 'center', 'display': 'inline-block',
        #           'marginLeft': '32px', 'marginRight': '32px', 'marginBottom': '16px', 'marginTop': '8px'}),
    ],className="graph-div"),  # Graph
])



def range_plus(start, stop, num_steps):
    range_size=stop-start
    step_size=float(range_size)/(num_steps-1)
    for step in range(num_steps):
        yield start + step*step_size


@ app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-data', 'value'),
    Input('yaxis-data', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('colorscale', 'value'))
def update_graph(xaxis_data_name, yaxis_data_name,
                 xaxis_type, yaxis_type,
                 colorscale):

    if colorscale == 'ntg':
        colorscale=ntg_colors.ntg
    elif colorscale == 'ntg_map':
        colorscale=ntg_colors.ntg_map
    elif colorscale == 'ntg_av':
        colorscale=ntg_colors.ntg_av

    # dff = df[df['Year'] == xrange_value]
    dff=df
    xrange_min=-50 if xaxis_data_name == 'Time' else -1
    xrange_max=[]
    fig=go.Figure()
    for key, it in zip(dff, range(len(dff))):
        dataname=key.split(".")[0].split(os.sep)[1].split("_")
        ydata=list(dff[key][yaxis_data_name])
        if yaxis_data_name == "Total Energy":
            for i in range(len(ydata)):
                ydata[i] -= dff[key][yaxis_data_name][0]
        fig.add_trace(go.Scatter(
            x=list(dff[key][xaxis_data_name]),
            y=ydata,
            mode='lines',
            line=dict(width=5, color=px.colors.sample_colorscale(
                colorscale, it/len(dff))[0]),
            name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
            # hover_name=dff[key][yaxis_data_name]
            )
        )
        xrange_max.append(max(dff[key][xaxis_data_name]))
    
    fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
                                 font=dict(size=22, family="Times New Roman")),
                      autosize=False,height=540,
                      template='simple_white',paper_bgcolor='#B4A0AA',plot_bgcolor='#B4A0AA',
                      margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=dict(text=xaxis_data_name,
                                font=dict(size=20, family="Times New Roman")),
                     range=[xrange_min, max(xrange_max)],
                     type=xaxis_type, linewidth=4, mirror=True, side='bottom',
                     ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                     minor=dict(ticklen=10, tickwidth=2))

    fig.update_yaxes(title=dict(text=yaxis_data_name,
                                font=dict(size=20, family="Times New Roman")),
                     type=yaxis_type, linewidth=4, mirror=True, side='left',
                     ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                     minor=dict(ticklen=10, tickwidth=2))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)