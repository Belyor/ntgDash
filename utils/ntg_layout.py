from dash import dcc, html
import math
from utils.ntg_graph import GraphPickerAIO, groups

# from utils.querystring_methods import encode_state
# from utils.querystring_methods import parse_state
from utils.querystring_methods import apply_value_from_querystring

from pandas import DataFrame

# sets application's layout
def create_layout(metadata : DataFrame, params):
    menu_graph_picker = html.Div([
        # Conservation
        GraphPickerAIO(
            data_type_props = {'children':'Conservation'},
            data_props = {'options':groups["conservation"]},
            x_axis_type_props = {'options': ['in time']},
            y_axis_type_props = {'options': ['linear', 'log']},
            aio_id = "conservation"
        ),
        # Center of mass
        GraphPickerAIO(
            data_type_props = {'children':'Center of mass'},
            data_props = {'options':groups['center of mass']},
            x_axis_type_props = {'options':['in time']},
            y_axis_type_props = {'options':['linear']},
            aio_id = "center-of-mass"
        ),
        # Deformation
        GraphPickerAIO(
            data_type_props = {'children':'Deformation'},
            data_props = {'options':groups["deformation"]},
            x_axis_type_props = {'options':['in time', 'in distance', 'as maps']},
            y_axis_type_props = {'options':['linear','log']},
            aio_id = 'deformation'
        ),
        # Pairing
        GraphPickerAIO(
            data_type_props = {'children':'Pairing'},
            data_props = {'options':groups["pairing"]},
            x_axis_type_props = {'options':['in time', 'in distance', 'as maps']},
            y_axis_type_props = {'options':['linear','log']},
            aio_id = "pairing"
        ),
        # Miscellaneous
        GraphPickerAIO(
            data_type_props = {'children':'Miscellaneous'},
            data_props = {'options':groups["misc"]},
            x_axis_type_props = {'options':['in time', 'in distance', 'as maps']},
            y_axis_type_props = {'options':['linear','log']},
            aio_id = "misc"
        )
    ], className="graph-picker")


    menu_filter = html.Div([
        # headline
        html.Div([html.H2("Filters")], className="filters--header"),

        # options
        html.Div([
            html.Div([
                html.H3("System"),
                html.Div(
                    apply_value_from_querystring(params)(dcc.Dropdown)(
                        options=list(metadata['system'].unique()) + ['All'],
                        value=['All'],
                        id='filter_system',
                        multi=True
                    ), className="filters--list"),
            ], className="filters--column"),

            html.Div([
                html.H3("Method"),
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
                html.H3("Functional"),
                apply_value_from_querystring(params)(dcc.Dropdown)(
                    options=list(metadata['functional'].unique()) + ['All'],
                    value=['All'],
                    id='filter_functional',
                    multi=True
                ),
            ], className="filters--column")
        ], className="filters--options"),

        # Slider for energy
        html.H3("Ecm [MeV]", className="filters--text"),
        apply_value_from_querystring(params)(dcc.RangeSlider)(
            min=metadata['energy'].min(),
            max=metadata['energy'].max(),
            tooltip={'always_visible' : True, "placement" : "bottom"},
            value=[metadata['energy'].min(), metadata['energy'].max()],
            id='filter_ecms',
            marks=None,
        ),

        # Slider for phase
        html.H3("Phase", className="filters--text"), 
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
        html.H3("b", className="filters--text"),
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

        html.Button('Apply', id='apply', n_clicks=0, className="filters--button")
    ], className="filters")



    # Fit together everything
    layout = html.Div([
        html.Div([
            html.Div([html.H1("LISE Analyzer")], className="app-header--title"),
        ], className="app-header"),
        html.Div([
            # Menu
            html.Div([
                menu_graph_picker,
                menu_filter,
            ], className="menu"),

            # List of selected graphs from graph_pickers menu
            html.Div([
                html.H2("List of graphs", className="list-of-graphs--header"),
                apply_value_from_querystring(params)(dcc.Dropdown)(
                    options=[],
                    value=[],
                    id='list-of-graphs',
                    multi=True,
                    className='list-of-graphs--list'
                ),
            ]),
            html.Div([], id='graphs', className='graph-div'),
        ]),
        dcc.Store(id = 'filtered_files'),
    ], id='page-layout')

    return layout
