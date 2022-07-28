from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import math

# Project
import utils.ntg_data as ntg_data
import utils.ntg_colors as ntg_colors

app = Dash(__name__)

df = ntg_data.load_data()

app.layout = html.Div([
    # Date Picker
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
                )], style={'flush': 'left', 'display': 'inline-block',
                           'marginLeft': '16px', 'marginRight': '16px', 'marginBottom': '8px', 'marginTop': '8px'}
            ),
        ], style={'width': '28%', 'flush': 'left', 'display': 'inline-block',
                  'marginLeft': '32px', 'marginRight': '32px', 'marginBottom': '16px', 'marginTop': '16px'}),


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
                )], style={'flush': 'left', 'display': 'inline-block',
                           'marginLeft': '16px', 'marginRight': '16px', 'marginBottom': '8px', 'marginTop': '8px'}
            ),
        ], style={'width': '18%', 'flush': 'right', 'display': 'inline-block',
                  'marginLeft': '32px', 'marginRight': '32px', 'marginBottom': '16px', 'marginTop': '16px'}),

    ], style={'width': '100%', 'display': 'inline-block',
              'marginLeft': '32px', 'marginRight': '32px', 'marginBottom': '8px', 'marginTop': '16px'},
    ),  # Date Picker

    # Graph
    html.Div([
        html.Div([
            html.H4("Colorscale"),
            dcc.Dropdown(
                id='colorscale',
                options=ntg_colors.colorscales,
                value='ntg',
            ),
        ], style={'width': '20%', 'float': 'left', 'display': 'inline-block',
                  'marginLeft': '32px', 'marginRight': '32px', 'marginBottom': '16px', 'marginTop': '8px'}),

        html.Div([
            html.Div([
                dcc.RangeSlider(min=-40, max=0, step=0.25, value=[-2, 2], vertical=True,
                                tooltip={"placement": "left", "always_visible": True}, id='yrange-slider')],
                     style={"width": "4%", "height": "100%", 'flush': 'left',  "display": "inline-block",
                            'marginLeft': '16px', 'marginRight': '16px', 'marginBottom': '16px', 'marginTop': '8px'}),
            html.Div([
                dcc.Graph(id="indicator-graphic")],
                style={'width': '90%', "height": "100%", 'flush': 'right', 'display': 'inline-block',
                       'marginLeft': '16px', 'marginRight': '16px', 'marginBottom': '8px', 'marginTop': '8px'}),
        ], style={'width': '100%', 'flush': 'center', 'display': 'inline-block',
                  'marginLeft': '32px', 'marginRight': '32px', 'marginBottom': '16px', 'marginTop': '8px'}),

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
    ], style={'width': '90%', 'float': 'left', 'display': 'inline-block',
              'marginLeft': '32px', 'marginRight': '32px', 'marginBottom': '16px', 'marginTop': '8px'}),  # Graph
])


@app.callback(
    Output('yrange-slider', 'min'),
    Output('yrange-slider', 'max'),
    Input('yaxis-data', 'value'),
)
def update_yminmax(yaxis_data_name):
    if yaxis_data_name == "Total Energy":
        return -5, 5
    else:
        tmp_min = []
        tmp_max = []
        for key in df:
            tmp_min.append(min(df[key][yaxis_data_name]))
            tmp_max.append(max(df[key][yaxis_data_name]))
        y_min = min(tmp_min)-0.05*min(tmp_min)
        y_max = max(tmp_max)+0.05*max(tmp_max)

        return y_min, y_max


def range_plus(start, stop, num_steps):
    range_size = stop-start
    step_size = float(range_size)/(num_steps-1)
    for step in range(num_steps):
        yield start + step*step_size


@app.callback(
    Output('yrange-slider', 'marks'),
    Input('yrange-slider', 'min'),
    Input('yrange-slider', 'max'))
def update_marks(ymin_value, ymax_value):
    marks = {}
    for i in range_plus(math.ceil(ymin_value), math.ceil(ymax_value), 12):
        marks[i] = str(math.ceil(i))
    return marks


@ app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-data', 'value'),
    Input('yaxis-data', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('yrange-slider', 'value'),
    Input('colorscale', 'value'))
def update_graph(xaxis_data_name, yaxis_data_name,
                 xaxis_type, yaxis_type,
                 yrange_value,
                 colorscale):

    if colorscale == 'ntg':
        colorscale = ntg_colors.ntg
    elif colorscale == 'ntg_map':
        colorscale = ntg_colors.ntg_map
    elif colorscale == 'ntg_av':
        colorscale = ntg_colors.ntg_av

    # dff = df[df['Year'] == xrange_value]
    dff = df
    xrange_min = -50 if xaxis_data_name == 'Time' else -1
    xrange_max=[]
    fig = go.Figure()
    for key, it in zip(dff, range(len(dff))):

        ydata = list(dff[key][yaxis_data_name])
        if yaxis_data_name == "Total Energy":
            for i in range(len(ydata)):
                ydata[i] -= dff[key][yaxis_data_name][0]
        fig.add_trace(go.Scatter(
            x=list(dff[key][xaxis_data_name]),
            y=ydata,
            mode='lines+markers',
            line=dict(width=3, color=px.colors.sample_colorscale(
                colorscale, it/len(dff))[0])
            # hover_name=dff[key][yaxis_data_name]
            )
        )
        xrange_max.append(max(dff[key][xaxis_data_name]))
    
    fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
                                 font=dict(size=22, family="Times New Roman")),
                      template='simple_white',
                      margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=dict(text=xaxis_data_name,
                                font=dict(size=20, family="Times New Roman")),
                     range=[xrange_min, max(xrange_max)],
                     type=xaxis_type, linewidth=4, mirror=True, side='bottom',
                     ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                     minor=dict(ticklen=10, tickwidth=2))

    fig.update_yaxes(title=dict(text=yaxis_data_name,
                                font=dict(size=20, family="Times New Roman")),
                     range=yrange_value,
                     type=yaxis_type, linewidth=4, mirror=True, side='left',
                     ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                     minor=dict(ticklen=10, tickwidth=2))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
