from dash import dcc, html
import json
import math
from utils.ntg_graph import GraphPickerAIO, groups, create_help_tip

# from utils.querystring_methods import encode_state
# from utils.querystring_methods import parse_state
from utils.querystring_methods import apply_value_from_querystring

from pandas import DataFrame

# sets application's layout
def create_layout(metadata : DataFrame, params):
    menu_graph_picker = html.Div([
        # Conservation
        GraphPickerAIO(
            data_type_props = {'children': 'Conservation'},
            data_props = {'options': groups["conservation"]},
            x_axis_type_props = {
                'options': [{'label':'in time','value':'in time'}],
                'value': 'in time',
            },
            y_axis_type_props = {
                'options': ['linear', 'log'],
                'value': 'linear'
            },
            tooltip_head = "FILL ME IN",
            tooltip_body = "FILL ME IN",
            aio_id = "conservation"
        ),
        # Center of mass
        GraphPickerAIO(
            data_type_props = {'children': 'Center of mass'},
            data_props = {'options': groups['center of mass']},
            x_axis_type_props = {
                'options': [{'label':'in time','value':'in time'}],
                'value': 'in time',
            },
            y_axis_type_props = {
                'options': ['linear'],
                'value': 'linear'
            },
            tooltip_head = "FILL ME IN",
            tooltip_body = "FILL ME IN",
            aio_id = "center-of-mass"
        ),
        # Deformation
        GraphPickerAIO(
            data_type_props = {'children':'Deformation'},
            data_props = {'options': groups["deformation"]},
            x_axis_type_props = {
                'options':[
                    {'label':'in time','value':'in time'},
                    {'label':'in distance','value':'in distance'},
                    {'label':'as maps','value':'as maps','disabled':True}
                ],
                'value': 'in time',
            },
            y_axis_type_props = {
                'options': ['linear', 'log'],
                'value': 'linear'
            },
            tooltip_head = "FILL ME IN",
            tooltip_body = "FILL ME IN",
            aio_id = 'deformation'
        ),
        # Pairing
        GraphPickerAIO(
            data_type_props = {'children':'Pairing'},
            data_props = {'options':groups["pairing"]},
            x_axis_type_props = {
                'options':[
                    {'label':'in time','value':'in time'},
                    {'label':'in distance','value':'in distance'},
                    {'label':'as maps','value':'as maps','disabled':True}
                ],
                'value': 'in time',
            },
            y_axis_type_props = {
                'options': ['linear', 'log'],
                'value': 'linear'
            },
            tooltip_head = "FILL ME IN",
            tooltip_body = "FILL ME IN",
            aio_id = "pairing"
        ),
        # Miscellaneous
        GraphPickerAIO(
            data_type_props = {'children':'Miscellaneous'},
            data_props = {'options':groups["misc"]},
            x_axis_type_props = {
                'options':[
                    {'label':'in time','value':'in time'},
                    {'label':'in distance','value':'in distance'},
                    {'label':'as maps','value':'as maps','disabled':True}
                ],
                'value': 'in time',
            },
            y_axis_type_props = {
                'options': ['linear', 'log'],
                'value': 'linear'
            },
            tooltip_head = "FILL ME IN",
            tooltip_body = "FILL ME IN",
            aio_id = "misc"
        )
    ], className="graph-picker")

    custom_opt = ['All Data']
    with open('./custom_filters.json') as file:
        for entry in json.load(file):
            custom_opt.append(entry['label'])

    menu_filter = html.Div([
        # headline
        html.H2("Filters", className="filters--header"),

        # Custom set filter
        html.H3("Dataset"),
        apply_value_from_querystring(params)(dcc.Dropdown)(
            options=custom_opt,
            value='All Data',
            id='filter_set',
        ),

        # options
        html.Div([
            html.Div([
                html.Div([
                    html.H3("System"),
                    create_help_tip("FILL ME IN", "FILL ME IN"),
                ], className='filters--row'),
                html.Div(
                    apply_value_from_querystring(params)(dcc.Dropdown)(
                        options=metadata['system'].unique(),
                        value=[],
                        placeholder='All',
                        id='filter_system',
                        multi=True
                    ), className="filters--list"),
            ], className="filters--column"),

            html.Div([
                html.Div([
                    html.H3("Method"),
                    create_help_tip("FILL ME IN", "FILL ME IN"),
                ], className='filters--row'),
                html.Div(
                    dcc.Checklist(
                        [
                            {'label':'HF','value':'HF','disabled':True},
                            {'label':'HFB','value':'HFB','disabled':True}
                        ],
                        id='filter_method',
                        labelStyle={'display': 'block'}
                    ), className="filters--radio-items")
            ], className="filters--column"),

            html.Div([
                html.Div([
                    html.H3("Functional"),
                    create_help_tip("FILL ME IN", "FILL ME IN"),
                ], className='filters--row'),
                apply_value_from_querystring(params)(dcc.Dropdown)(
                    options=metadata['functional'].unique(),
                    value=[],
                    placeholder='All',
                    id='filter_functional',
                    multi=True
                ),
            ], className="filters--column")
        ], className="filters--options"),

        # Slider for energy
        html.Div([
            html.H3("Ecm [MeV]", className="filters--text"),
            create_help_tip("FILL ME IN", "FILL ME IN"),
        ], className='filters--row'),
        apply_value_from_querystring(params)(dcc.RangeSlider)(
            min=metadata['energy'].min(),
            max=metadata['energy'].max(),
            tooltip={'always_visible' : True, "placement" : "bottom"},
            value=[metadata['energy'].min(), metadata['energy'].max()],
            id='filter_ecms',
            marks=None,
        ),

        # Slider for phase
        html.Div([
            html.H3("Phase", className="filters--text"), 
            create_help_tip("FILL ME IN", "FILL ME IN"),
        ], className='filters--row'),
        apply_value_from_querystring(params)(dcc.RangeSlider)(
            min=0,
            max=2*math.pi,
            tooltip={
                'always_visible':True,
                "placement": "bottom"
            },
            value=[0,2*math.pi], className="filter--slider", id='filter_phase',
            marks={
                0:           {'label': '0',    'style': {'color': 'black'}},
                math.pi/2:   {'label': 'π/2',  'style': {'color': 'black'}},
                math.pi:     {'label': 'π',    'style': {'color': 'black'}},
                3*math.pi/2: {'label': '3π/2', 'style': {'color': 'black'}},
                2*math.pi:   {'label': '2π',   'style': {'color': 'black'}}
            }
        ),

        # Slider for impact parameter
        html.Div([
            html.H3("b", className="filters--text"),
            create_help_tip("FILL ME IN", "FILL ME IN"),
        ], className='filters--row'),
        apply_value_from_querystring(params)(dcc.RangeSlider)(
            min=0,
            max=4,
            value=[0,4], 
            tooltip={'always_visible': True, "placement": "bottom"},
            className="filter--slider", id='filter_b',
            marks={
                0: {'label': '0', 'style': {'color': 'black'}},
                1: {'label': '1', 'style': {'color': 'black'}},
                2: {'label': '2', 'style': {'color': 'black'}},
                3: {'label': '3', 'style': {'color': 'black'}},
                4: {'label': '4', 'style': {'color': 'black'}}
            },
        ),

        html.Button('Apply', id='apply', n_clicks=0, className="filters--button"),
        dcc.Store(id='filtered_files'),
    ], className="filters")



    # Fit together everything
    layout = html.Div([
        html.Div([html.H1("LISE Analyzer")], className="app-header"),
        html.Div([
            # Menu
            html.Div([
                menu_graph_picker,
                menu_filter,
            ], className="menu"),

            # List of selected graphs from graph_pickers menu
            html.Div([
                html.Button(
                    'Update and copy URL',
                    id='URL-copy',
                    className='list-of-graphs--button',
                ),
                dcc.Clipboard(
                    id='clipboard',
                    n_clicks=0,
                    style={ 'display' : 'none' },
                ),
                html.H2("List of graphs", className="list-of-graphs--header"),
                apply_value_from_querystring(params)(dcc.Dropdown)(
                    options=[],
                    value=[],
                    placeholder='',
                    id='list-of-graphs',
                    multi=True,
                    className='list-of-graphs--list'
                ),
            ]),
            html.Div([], id='graphs', className='graph-div'),
        ]),
    ], id='page-layout')

    return layout
