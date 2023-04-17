from dash import Dash, dcc, html
import math
from utils.ntg_graph import GraphPickerAIO
def fun (data):
    one=[]
    two=[]
    three=[]
    four=[]
    five=[]
    six= []
    seven=[]
    tab =[one, two, three,four, five,six, seven]
    for j in range (7):
        for i in range (len(data)):
            tab[j].append(data[i][j])
    tab1 = list(set(tab[0]))
    tab2 = list(set(tab[1]))
    tab3 = list(set(tab[2]))
    tab4 = list(set(tab[3]))
    tab5 = list(set(tab[4]))
    tab6 = list(set(tab[5]))
    tab7 = list(set(tab[6]))
    tab7 = min(tab7),max(tab7)
    return(tab1,tab2,tab3,tab4,tab5,tab6,tab7)
#sets application's layout
def sett(app: Dash,metadata):
    dane=fun(metadata)
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
                        GraphPickerAIO(
                            data_type_props = {'children':'Conservation'},
                            data_props = {'options':["Total Energy", "Number of Protons","Number of Neutrons"]},
                            x_axis_type_props = {'options':['in time']},
                            y_axis_type_props = {'options':['linear', 'log']},
                            aio_id = "conservation"
                        ),
                        # Center of mass
                        GraphPickerAIO(
                            data_type_props = {'children':'Center of mass'},
                            data_props = {'options':["X_cm", "Y_cm", "Z_cm",
                                "X_cm for Protons", "Y_cm for Protons", "Z_cm for Protons",
                                "X_cm for Neutrons", "Y_cm for Neutrons", "Z_cm for Neutrons",
                                #"Center of Mass Energy"
                                ]},
                            x_axis_type_props = {'options':['in time']},
                            y_axis_type_props = {'options':['linear']},
                            aio_id = "center-of-mass"
                        ),
                        # Deformation
                        GraphPickerAIO(
                            data_type_props = {'children':'Deformation'},
                            data_props = {'options':["Beta", "Quadrupole Moment Q20",
                                "Octupole Moment Q30", "Hexadecupole Moment Q40"]},
                            x_axis_type_props = {'options':['in time', 'in distance', 'as maps']},
                            y_axis_type_props = {'options':['linear','log']},
                            aio_id = "deformation"
                        ),
                        # Pairing
                        GraphPickerAIO(
                            data_type_props = {'children':'Pairing'},
                            data_props = {'options':["Pairing gap for Protons",
                                    "Pairing gap for Neutrons"]},
                            x_axis_type_props = {'options':['in time', 'in distance', 'as maps']},
                            y_axis_type_props = {'options':['linear','log']},
                            aio_id = "pairing"
                        ),
                        # Miscellaneous
                        GraphPickerAIO(
                            data_type_props = {'children':'Miscellaneous'},
                            data_props = {'options':["?"]},
                            x_axis_type_props = {'options':['in time', 'in distance', 'as maps']},
                            y_axis_type_props = {'options':['linear','log']},
                            aio_id = "misc"
                        )
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
                                                    dane[0], '', id='filter_system', multi=True)], className="filters--list"),
                                                    ])
                                            ])

                                ], className="filters--column"),
                        # 2st column
                        html.Div([
                                    html.Div([html.H3("Method"),
                                        html.Div([
                                                html.Div([dcc.Checklist(
                                                        options = [{'label':'HF','value':'HF','disabled':True}, {'label':'HFB','value':'HFB','disabled':True}], id='filter_method',labelStyle={'display': 'block'}
                                                        )], className="filtersr--radio-items")
                                                ])
                                    ])


                                ], className="filters--column"),
                        # 3rd column
                        html.Div([
                                    html.Div([html.H3("Functional"),
                                html.Div([
                                    html.Div([dcc.Dropdown(
                                        dane[1], '', id='filter_filter', multi=True)], className="filters--list2"),
                                        ])
                                            ])
                                ], className="filters--column")

                    ], className="filters--options"),                 # dcc.RangeSlider(0, 20, tooltip = { 'always_visible': True }, value=20,className="filter--slider")
                    html.H3("Ecm [MeV]", className="filters--text"),
                dcc.RangeSlider(int(dane[6][0]),int(dane[6][1]), tooltip={'always_visible': True, "placement": "bottom"}, value=[int(dane[6][0]),int(dane[6][1])], id='filter_ecms', marks=None), html.H3("Phase", className="filters--text"), 
                dcc.RangeSlider(0, 2*math.pi, tooltip={'always_visible': True, "placement": "bottom"}, value=[0,2*math.pi], className="filter--slider", id='filter_phase', marks={
                0: {'label': '0', 'style': {'color': 'black'}},
                math.pi/2: {'label': 'π/2', 'style': {'color': 'black'}},
                math.pi: {'label': 'π', 'style': {'color': 'black'}},
                3*math.pi/2: {'label': '3π/2', 'style': {'color': 'black'}},
                2*math.pi: {'label': '2π', 'style': {'color': 'black'}}
        })  # 2*math.pi
                    , html.H3("b", className="filters--text"),
                      dcc.RangeSlider(0, 4, tooltip={'always_visible': True, "placement": "bottom"}, value=[0,4], className="filter--slider", id='filter_D', marks={
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
        ,html.Div([
            dcc.Dropdown([],id = 'files_out')
            ],style={"display":"none"})
    ])