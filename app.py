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
    html.Div([
        #Menu
        html.Div([
            #Graph picker menu
            html.Div([
                #Headline
                html.H2("Graph picker")],className="graph-picker--header"),
                #Options
                html.Div([
                    #1st column
                    html.Div([
                        html.Div([
                            html.H3("Conservation"),
                            html.Div([
                                html.Div([
                                    html.H4("Y value"),
                                    dcc.Dropdown(
                                        ["Total Energy", "Number of Protons", "Number of Neutrons"],
                                        'Total Energy',
                                        id = 'conservation-data'
                                    )
                                ],className="graph-picker--list"),
                                html.Div([
                                    html.H4("Axis type"),
                                    dcc.RadioItems(
                                        ['linear', 'log'],
                                        'linear',
                                        id = 'conservation-axis-type'
                                    )
                                ],className="graph-picker--radio-items"),
                                html.Button('Add', id='button-add-conservation', className="graph-picker--button")
                            ], className="graph-picker--data"),
                        ]),
                        html.Div([
                            html.H3("Deformation"),
                            html.Div([
                                html.Div([
                                    html.H4("Y value"),
                                    dcc.Dropdown(
                                        ["Beta", "Quadrupole Moment Q20", 
                                        "Octupole Moment Q30", "Hexadecupole Moment Q40"],
                                        'Beta',
                                        id = 'deformation-data'
                                    )
                                ],className="graph-picker--list"),
                                html.Div([
                                    html.H4("Axis type"),
                                    dcc.RadioItems(
                                        ['in time', 'in distance', 'maps'],
                                        'in time',
                                        id = 'deformation-axis-type'
                                    )
                                ],className="graph-picker--radio-items"),
                                html.Button('Add', id='button-add-deformation', className="graph-picker--button")
                            ], className="graph-picker--data"),
                        ]),
                    ],className="graph-picker--column"),
                    #2nd column
                    html.Div([
                        html.Div([
                            html.H3("Center of mass"),
                            html.Div([
                                html.Div([
                                    html.H4("Y value"),
                                    dcc.Dropdown(
                                        ["X_cm", "Y_cm", "Z_cm",
                                        "X_cm for Protons", "Y_cm for Protons", "Z_cm for Protons",
                                        "X_cm for Neutrons", "Y_cm for Neutrons", "Z_cm for Neutrons",
                                        "Center of Mass Energy"],
                                        'Center of Mass Energy',
                                        id = 'center-of-mass-data'
                                    )
                                ],className="graph-picker--list"),
                                html.Div([
                                    html.H4("Axis type"),
                                    dcc.RadioItems(
                                        ['linear'],
                                        'linear',
                                        id = 'center-of-mass-axis-type'
                                    )
                                ],className="graph-picker--radio-items"),
                                html.Button('Add', id='button-add-center-of-mass', className="graph-picker--button")
                            ], className="graph-picker--data"),
                        ]),
                        html.Div([
                            html.H3("Pairing"),
                            html.Div([
                                html.Div([
                                    html.H4("Y value"),
                                    dcc.Dropdown(
                                        ["Pairing gap for Protons", "Pairing gap for  Neutrons"],
                                        'Pairing gap for Protons',
                                        id = 'pairing-data'
                                    )
                                ],className="graph-picker--list"),
                                html.Div([
                                    html.H4("Axis type"),
                                    dcc.RadioItems(
                                        ['in time', 'in distance', 'maps'],
                                        'in time',
                                        id = 'pairing-axis-type'
                                    )
                                ],className="graph-picker--radio-items"),
                                html.Button('Add', id='button-add-pairing', className="graph-picker--button")
                            ], className="graph-picker--data"),
                        ])
                    ],className="graph-picker--column")
                ],className="graph-picker--options")
            ],className="graph-picker"),
        #Filters menu
        html.Div([
            #headline
            html.Div([html.H2("Filters")],className="filters--header"),
            #options
                html.Div([
                    #1st column
                    html.Div([
                                html.Div([html.H3("System"),
                                        html.Div([
                                            html.Div([dcc.Dropdown([],'',id='list-of-filters',multi=True)],className="filters--list"),
                                                ])
                                        ])
                   
                            ],className="filters--column")
                    ,
                     #2st column
                    html.Div([
                                html.Div([html.H3("Method"),
                                    html.Div([
                                            html.Div([dcc.RadioItems(
                                                ['1', '2'],
                                                '1',
                                                id = '???',labelStyle={'display': 'block'}
                                                )],className="filtersr--radio-items")
                                            ])
                                ])

                   
                            ],className="filters--column")
                            ,
                    # 3rd column
                    html.Div([
                                html.Div([html.H3("Filters"),
                            html.Div([
                                html.Div([dcc.Dropdown([],'',id='middle',multi=True)],className="filters--list2"),
                                    ])
                                        ])
                            ],className="filters--column")
               
                ],className="filters--options")    
                 ,html.H3("Ecm", className="filters--text"), #dcc.RangeSlider(0, 20, tooltip = { 'always_visible': True }, value=20,className="filter--slider")
                  dcc.RangeSlider(0, 20,tooltip = { 'always_visible': True }, value=[4, 16])
                ,html.H3("Phase",className="filters--text"), dcc.Slider(0, 6.28 , tooltip = { 'always_visible': True },value=10,className="filter--slider") #2*math.pi
                ,html.H3("D",className="filters--text")
                 , dcc.Slider(0,4 , tooltip = { 'always_visible': True }, value=10,className="filter--slider")  
                 ,html.Button('Apply', className="filters--button")
        ],className="filters")           
    ],className="menu"),
    html.Div([
        html.H2("List of graphs", className="list-of-graphs--header"),
        dcc.Dropdown([],'',id='list-of-graphs',multi=True,className='list-of-graphs--list')
    ])  
#    # Data Picker
#    html.Div([
#        html.Div([
#            html.H4("Y axis"),
#            dcc.Dropdown(
#                ntg_data.col_results[1:],
#                'Total Energy',
#                id='yaxis-data'
#            ),
#            html.Div([
#                dcc.RadioItems(
#                    ['linear', 'log'],
#                    'linear',
#                    id='yaxis-type',
#                    inline=True
#                )], className="data-picker--yaxis-type"
#            ),
#        ], className="data-picker--yaxis"),
#
#
#        html.Div([
#            html.H4("X axis"),
#            dcc.Dropdown(
#                ['Time', 'Distance'],  # ntg_data.col_results,
#                'Time',
#                id='xaxis-data'
#            ),
#            html.Div([
#                dcc.RadioItems(
#                    ['linear', 'log'],
#                    'linear',
#                    id='xaxis-type',
#                    inline=True
#                )], className="data-picker--xaxis-type"
#            ),
#        ], className="data-picker--xaxis"),
#
#        html.Div([
#            html.H4("Colorscale"),
#            html.Div([
#            dcc.Dropdown(
#                id='colorscale',
#                options=ntg_colors.colorscales,
#                value='ntg',
#            )],className="data-picker-colorscale"),
#        ], className="data-picker-colorscale-div")
#
#    ], className="data-picker"
#    ),  # Data Picker
#
#    # Graph
#    html.Div([
#                dcc.Graph(id="indicator-graphic")],className="graph-graph"),
#        # ] #className="graph"
#    #,className="graph-div"),  # Graph
])



#def range_plus(start, stop, num_steps):
#    range_size=stop-start
#    step_size=float(range_size)/(num_steps-1)
#    for step in range(num_steps):
#        yield start + step*step_size
#
#
#@ app.callback(
#    Output('indicator-graphic', 'figure'),
#    Input('xaxis-data', 'value'),
#    Input('yaxis-data', 'value'),
#    Input('xaxis-type', 'value'),
#    Input('yaxis-type', 'value'),
#    Input('colorscale', 'value'))
#def update_graph(xaxis_data_name, yaxis_data_name,
#                 xaxis_type, yaxis_type,
#                 colorscale):
#
#    if colorscale == 'ntg':
#        colorscale=ntg_colors.ntg
#    elif colorscale == 'ntg_map':
#        colorscale=ntg_colors.ntg_map
#    elif colorscale == 'ntg_av':
#        colorscale=ntg_colors.ntg_av
#
#    # dff = df[df['Year'] == xrange_value]
#    dff=df
#    xrange_min=-50 if xaxis_data_name == 'Time' else -1
#    xrange_max=[]
#    fig=go.Figure()
#    for key, it in zip(dff, range(len(dff))):
#        dataname=key.split(".")[0].split(os.sep)[1].split("_")
#        ydata=list(dff[key][yaxis_data_name])
#        if yaxis_data_name == "Total Energy":
#            for i in range(len(ydata)):
#                ydata[i] -= dff[key][yaxis_data_name][0]
#        fig.add_trace(go.Scatter(
#            x=list(dff[key][xaxis_data_name]),
#            y=ydata,
#            mode='lines',
#            line=dict(width=5, color=px.colors.sample_colorscale(
#                colorscale, it/len(dff))[0]),
#            name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
#            # hover_name=dff[key][yaxis_data_name]
#            )
#        )
#        xrange_max.append(max(dff[key][xaxis_data_name]))
#    
#    fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
#                                 font=dict(size=22, family="Times New Roman")),
#                      autosize=False,height=540,
#                      template='simple_white',paper_bgcolor='#B4A0AA',plot_bgcolor='#B4A0AA',
#                      margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, hovermode='closest')
#
#    fig.update_xaxes(title=dict(text=xaxis_data_name,
#                                font=dict(size=20, family="Times New Roman")),
#                     range=[xrange_min, max(xrange_max)],
#                     type=xaxis_type, linewidth=4, mirror=True, side='bottom',
#                     ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
#                     minor=dict(ticklen=10, tickwidth=2))
#
#    fig.update_yaxes(title=dict(text=yaxis_data_name,
#                                font=dict(size=20, family="Times New Roman")),
#                     type=yaxis_type, linewidth=4, mirror=True, side='left',
#                     ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
#                     minor=dict(ticklen=10, tickwidth=2))
#
#    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
