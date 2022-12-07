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
import utils.graph as graph

app = Dash(__name__)

df = ntg_data.load_data()

app.layout = html.Div([
    html.Div([
        html.Div([html.H1("LISE Analyzer")], className="app-header--title"),
    ], className="app-header"),
    html.Div([
        # Menu
        html.Div([
            # Graph picker menu
            html.Div([
                # Options
                html.Div([
                    # Conservation
                    html.Div([
                        html.H3("Conservation: ",
                                className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id='conservation-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["Total Energy", "Number of Protons",
                                    "Number of Neutrons"],
                                'Total Energy',
                                id='conservation-data'
                            )
                        ], className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time'],
                                'in time',
                                id='conservation-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsOneOption"),
                        html.Button('Add', id='addButton-conservation',
                                    className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    # Center of mass
                    html.Div([
                        html.H3("Center of mass:",
                                className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear'],
                                'linear',
                                id='center-of-mass-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsOneOption"),
                        html.Div([
                            dcc.Dropdown(
                                ["X_cm", "Y_cm", "Z_cm",
                                "X_cm for Protons", "Y_cm for Protons", "Z_cm for Protons",
                                "X_cm for Neutrons", "Y_cm for Neutrons", "Z_cm for Neutrons",
                                "Center of Mass Energy"],
                                'Center of Mass Energy',
                                id='center-of-mass-data'
                            )
                        ], className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time'],
                                'in time',
                                id='center-of-mass-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsOneOption"),
                        html.Button('Add', id='addButton-center-of-mass',
                                    className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    # Deformation
                    html.Div([
                        html.H3("Deformation:",
                                className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id='deformation-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["Beta", "Quadrupole Moment Q20",
                                "Octupole Moment Q30", "Hexadecupole Moment Q40"],
                                'Beta',
                                id='deformation-data'
                            )
                        ], className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time', 'in distance', 'as maps'],
                                'in time',
                                id='deformation-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsThreeOptions"),
                        html.Button('Add', id='addButton-deformation',
                                    className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    # Pairing
                    html.Div([
                        html.H3("Pairing:", className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id='pairing-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["Pairing gap for Protons",
                                    "Pairing gap for  Neutrons"],
                                'Pairing gap for Protons',
                                id='pairing-data'
                            )
                        ], className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time', 'in distance', 'as maps'],
                                'in time',
                                id='pairing-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsThreeOptions"),
                        html.Button('Add', id='addButton-pairing',
                                    className="graph-picker--addButton")
                    ], className="graph-picker--container"),
                    # Miscellaneous
                    html.Div([
                        html.H3("Miscellaneous:",
                                className="graph-picker--header"),
                        html.H3("Plot ", className="graph-picker--text"),
                        html.Div([
                            dcc.RadioItems(
                                ['linear', 'log'],
                                'linear',
                                id='miscellaneous-yaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsTwoOptions"),
                        html.Div([
                            dcc.Dropdown(
                                ["?"],
                                '?',
                                id='miscellaneous-data'
                            )
                        ], className="graph-picker--list"),
                        html.Div([
                            dcc.RadioItems(
                                ['in time', 'in distance', 'as maps'],
                                'in time',
                                id='miscellaneous-xaxis-type',
                                labelClassName="graph-picker--radioItems-labelStyle"
                            )
                        ], className="graph-picker--radioItemsThreeOptions"),
                        html.Button('Add', id='addButton-miscellaneous',
                                    className="graph-picker--addButton")
                    ], className="graph-picker--container")
                ], className="graph-picker--options")
            ], className="graph-picker"),
            # Filters menu
        html.Div([
            # headline
            html.Div([html.H2("Filters")], className="filters--header"),
            # options
                html.Div([
                    # 1st column
                    html.Div([
                                html.Div([html.H3("System"),
                                        html.Div([
                                            html.Div([dcc.Dropdown(
                                                [], '', id='filters_system', multi=True)], className="filters--list"),
                                                ])
                                        ])

                            ], className="filters--column"),
                     # 2st column
                    html.Div([
                                html.Div([html.H3("Method"),
                                    html.Div([
                                            html.Div([dcc.Checklist(
                                                     ['HF', 'HFB'], labelStyle={'display': 'block'}
                                                    )], className="filtersr--radio-items")
                                            ])
                                ])


                            ], className="filters--column"),
                    # 3rd column
                    html.Div([
                                html.Div([html.H3("Functional"),
                            html.Div([
                                html.Div([dcc.Dropdown(
                                    [], '', id='filter_filter', multi=True)], className="filters--list2"),
                                    ])
                                        ])
                            ], className="filters--column")

                ], className="filters--options"),                 # dcc.RangeSlider(0, 20, tooltip = { 'always_visible': True }, value=20,className="filter--slider")
                 html.H3("Ecm [MeV]", className="filters--text"),
            dcc.RangeSlider(0, 20, tooltip={'always_visible': True, "placement": "bottom"}, value=[0, 20], id='filter_ecms', marks=None), html.H3("Phase", className="filters--text"), dcc.Slider(0, 2*math.pi, tooltip={'always_visible': True, "placement": "bottom"}, value=2*math.pi, className="filter--slider", id='filter_phase', marks={
        0: {'label': '0', 'style': {'color': 'black'}},
        math.pi/2: {'label': 'π/2', 'style': {'color': 'black'}},
        math.pi: {'label': 'π', 'style': {'color': 'black'}},
        3*math.pi/2: {'label': '3π/2', 'style': {'color': 'black'}},
        2*math.pi: {'label': '2π', 'style': {'color': 'black'}}
    })  # 2*math.pi
                , html.H3("b", className="filters--text"), dcc.Slider(0, 4, tooltip={'always_visible': True, "placement": "bottom"}, value=10, className="filter--slider", id='filter_D', marks={
        0: {'label': '0', 'style': {'color': 'black'}},
        1: {'label': '1', 'style': {'color': 'black'}},
        2: {'label': '2', 'style': {'color': 'black'}},
        3: {'label': '3', 'style': {'color': 'black'}},
        4: {'label': '4', 'style': {'color': 'black'}}}),
        html.Button('Apply', id='apply', n_clicks=0,
                    className="filters--button")
        ], className="filters")
    ], className="menu"),
        html.Div([
            html.H2("List of graphs", className="list-of-graphs--header"),
            dcc.Dropdown([], [], id='list-of-graphs', multi=True,
                         className='list-of-graphs--list'),
        ]),
        html.Div([], id='graphs', className='graph-div'),
    ])
])


graph.get_callbacks(app, df)

if __name__ == '__main__':
    app.run_server(debug=True)
