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
import utils.graph as graph

app = Dash(__name__)

df = ntg_data.load_data()

app.layout = html.Div([
    html.Div([
        html.Div([html.H1("LISE Analyzer")],className="app-header--title"),
    ], className="app-header"),
    html.Div([
        #Menu
        html.Div([
            #Graph picker menu
            html.Div([
                #Options
                html.Div([
                    #Conservation
                    html.Div([
                        html.H3("Conservation: ", className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id = 'conservation-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["Total Energy", "Number of Protons", "Number of Neutrons"],
                                'Total Energy',
                                id = 'conservation-data'
                            )
                        ],className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time'],
                                'in time',
                                id = 'conservation-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsOneOption"),
                        html.Button('Add', id='addButton-conservation', className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    #Center of mass
                    html.Div([
                        html.H3("Center of mass:", className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear'],
                                'linear',
                                id = 'center-of-mass-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsOneOption"),
                        html.Div([
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
                            dcc.RadioItems(
                                ['in time'],
                                'in time',
                                id = 'center-of-mass-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsOneOption"),
                        html.Button('Add', id='addButton-center-of-mass', className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    #Deformation
                    html.Div([
                        html.H3("Deformation:", className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id = 'deformation-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["Beta", "Quadrupole Moment Q20", 
                                "Octupole Moment Q30", "Hexadecupole Moment Q40"],
                                'Beta',
                                id = 'deformation-data'
                            )
                        ],className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time', 'in distance', 'as maps'],
                                'in time',
                                id = 'deformation-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsThreeOptions"),
                        html.Button('Add', id='addButton-deformation', className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    #Pairing
                    html.Div([
                        html.H3("Pairing:", className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id = 'pairing-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["Pairing gap for Protons", "Pairing gap for  Neutrons"],
                                'Pairing gap for Protons',
                                id = 'pairing-data'
                            )
                        ],className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time', 'in distance', 'as maps'],
                                'in time',
                                id = 'pairing-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsThreeOptions"),
                        html.Button('Add', id='addButton-pairing', className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    #Miscellaneous
                    html.Div([
                        html.H3("Miscellaneous:", className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id = 'miscellaneous-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["?"],
                                '?',
                                id = 'miscellaneous-data'
                            )
                        ],className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time', 'in distance', 'as maps'],
                                'in time',
                                id = 'miscellaneous-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ],className="graph-picker--radioItemsThreeOptions"),
                        html.Button('Add', id='addButton-miscellaneous', className="graph-picker--addButton")
                    ], className="graph-picker--container")
                ],className="graph-picker--options")
            ],className="graph-picker"),
            #Filters menu
            html.Div([
                html.Div([html.H2("Filters")],className="filters--header")
            ],className="filters") 
        ],className="menu"),
        html.Div([
            #headline
            html.Div([html.H2("Filters")],className="filters--header"),
            #options
                html.Div([
                    #1st column
                    html.Div([
                                html.Div([html.H3("System"),
                                        html.Div([
                                            html.Div([dcc.Dropdown([],'',id='filters_system',multi=True)],className="filters--list"),
                                                ])
                                        ])
                   
                            ],className="filters--column")
                    ,
                     #2st column
                    html.Div([
                                html.Div([html.H3("Method"),
                                    html.Div([
                                            html.Div([dcc.Checklist(
    ['HF', 'HFB'],labelStyle={'display': 'block'}
)],className="filtersr--radio-items")
                                            ])
                                ])

                   
                            ],className="filters--column")
                            ,
                    # 3rd column
                    html.Div([
                                html.Div([html.H3("Functional"),
                            html.Div([
                                html.Div([dcc.Dropdown([],'',id='filter_filter',multi=True)],className="filters--list2"),
                                    ])
                                        ])
                            ],className="filters--column")
               
                ],className="filters--options")    
                 ,html.H3("Ecm [MeV]", className="filters--text"), #dcc.RangeSlider(0, 20, tooltip = { 'always_visible': True }, value=20,className="filter--slider")
            dcc.RangeSlider(0, 20,tooltip = { 'always_visible': True, "placement": "bottom" }, value=[0, 20],id='filter_ecms',marks=None)
                ,html.H3("Phase",className="filters--text"), dcc.Slider(0, 2*math.pi , tooltip = { 'always_visible': True, "placement": "bottom" },value=2*math.pi,className="filter--slider",id='filter_phase',marks={
        0: {'label': '0', 'style': {'color': 'black'}},
        math.pi/2: {'label': 'π/2','style': {'color': 'black'} },
        math.pi: {'label': 'π','style': {'color': 'black'}},
        3*math.pi/2: {'label': '3π/2','style': {'color': 'black'}},
        2*math.pi: {'label': '2π', 'style': {'color': 'black'}}
    }) #2*math.pi
                ,html.H3("b",className="filters--text")
                 , dcc.Slider(0,4 , tooltip = { 'always_visible': True , "placement": "bottom"}, value=10,className="filter--slider", id='filter_D', marks={
        0: {'label': '0', 'style': {'color': 'black'}},
        1: {'label': '1','style': {'color': 'black'} },
        2: {'label': '2','style': {'color': 'black'}},
        3: {'label': '3','style': {'color': 'black'}},
        4: {'label': '4','style': {'color': 'black'}}})  
                 ,html.Button('Apply', id ='apply' ,n_clicks=0 ,className="filters--button")
        ],className="filters")           
    ],className="menu"),
            html.H2("List of graphs", className="list-of-graphs--header"),
            dcc.Dropdown([],[],id='list-of-graphs',multi=True, className='list-of-graphs--list')
        ]),
        html.Div([], id='graphs', className='graph-div') 
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
])

graph.get_callbacks(app,df,ntg_colors.colorscales)

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
#@app.callback(
 #   Input('filter_systems', 'systems'),
 #   Input('filter_ecms', 'ecms'),
 #   Input('filter_D', 'D'),
 ##   Input('filter_systems', 'systems'),
  #  Input('filter_ecms', 'ecms'),
#)

if __name__ == '__main__':
    app.run_server(debug=True)
