from dash import dcc, html, callback, ctx, Input, Output, State, MATCH, Patch
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import uuid
import dash_bootstrap_components as dbc

from . import ntg_colors
colorscales=ntg_colors.colorscales

#groups of data
groups = {
    "conservation" : [
        "Total Energy",
        "Number of Protons",
        "Number of Neutrons"
    ],
    "center of mass" : [
        "X_cm",
        "Y_cm",
        "Z_cm",
        "X_cm for Protons",
        "Y_cm for Protons",
        "Z_cm for Protons",
        "X_cm for Neutrons",
        "Y_cm for Neutrons",
        "Z_cm for Neutrons",
        # "Center of Mass Energy",
    ],
    "deformation" : [
        "Beta",
        "Quadrupole Moment Q20",
        "Octupole Moment Q30",
        "Hexadecupole Moment Q40"
    ],
    "pairing" : [
        "Pairing gap for Protons",
        "Pairing gap for Neutrons"
    ],
    "misc" : ["?"]
}

units = {
    # Conservation
    "Total Energy": "MeV",
    "Number of Protons": "",
    "Number of Neutrons": "",
    # Center of mass
    "X_cm": "fm",
    "Y_cm": "fm",
    "Z_cm": "fm",
    "X_cm for Protons": "fm",
    "Y_cm for Protons": "fm",
    "Z_cm for Protons": "fm",
    "X_cm for Neutrons": "fm",
    "Y_cm for Neutrons": "fm",
    "Z_cm for Neutrons": "fm",
    "Center of Mass Energy": "MeV",
    # Deformation
    "Beta": "",
    "Quadrupole Moment Q20": "b",
    "Octupole Moment Q30": "b^3/2",
    "Hexadecupole Moment Q40": "b^2",
    # Pairing
    "Pairing gap for Protons": "MeV",
    "Pairing gap for Neutrons": "MeV",
    # Misc
    # x axis
    "Time": "fm/c",
    "Distance": "fm"
}

# Button with popover text
def create_help_tip(header_text, body_text):
    id = str(uuid.uuid4())
    tooltip = html.Div([
        dbc.Button(
            "?",
            id=id,
            className = 'help-tip',
        ),
        dbc.Popover(
            [
                dbc.PopoverHeader(header_text, className='popover-head'),
                dbc.PopoverBody(body_text, className='popoever-body'),
            ],
            target=id,
            body=True,
            placement='right',
            trigger="hover",
            className='popover'
        ),
    ])
    return tooltip

# GraphPickerAIO - a component which stores settings available in Graph Picker panel in main menu
class GraphPickerAIO(html.Div):
    """
    A class for an All-in-one component which stores components for graph settings available in Graph-Picker panel of main menu.

    Args:
        html.Div (html.Div): the parent component
    """
    class ids:
        """
        A subclass of GraphPickerAIO containing ids of each subcomponent of GraphPickerAIO.
        """
        data_type = lambda aio_id: {
            'component': 'GraphPickerAIO',
            'subcomponent': 'markdown',
            'aio_id': aio_id
        }
        y_axis_type = lambda aio_id: {
            'component': 'GraphPickerAIO',
            'subcomponent': 'yRadioItems',
            'aio_id': aio_id
        }
        data = lambda aio_id: {
            'component': 'GraphPickerAIO',
            'subcomponent': 'dataDropdown',
            'aio_id': aio_id
        }
        x_axis_type = lambda aio_id: {
            'component': 'GraphPickerAIO',
            'subcomponent': 'xRadioItems',
            'aio_id': aio_id
        }
        add_button = lambda aio_id: {
            'component': 'GraphPickerAIO',
            'subcomponent': 'addButton',
            'aio_id': aio_id
        }
    ids = ids

    # Arguments definition
    def __init__(
        self,
        data_type_props   : dict = {},
        data_props        : dict = {},
        x_axis_type_props : dict = {},
        y_axis_type_props : dict = {},
        add_button_props  : dict = {},
        tooltip_head = None,
        tooltip_body = None,
        aio_id : str = str(uuid.uuid4())
        ):
        """
        An init function for GraphPickerAIO component.

        Args:
            data_type_props (dict, optional): a dictionary with properties for a markdown describing a data type (one of five: conservation, center of mass, deformation, pairing, misc).
            data_props (dict, optional): a dictionary with properties for a dropdown containing names of datas available for a given data type.
            x_axis_type_props (dict, optional): a dictionary with properties for radioitems component containing information about what value is on an x axis of a graph (a subset of these three available values: in time, in distance, as maps).
            y_axis_type_props (dict, optional): a dictionary with properties for radioitems component containng information about what the type of y axis is (linear or logarithmic).
            add_button_properties (dict, optional): a dictionary with properties for a button which adds a graph to a graph list.
            aio_id (string, optional): an id of GraphPickerAIO component.
        """
        #set components properties
        data_type_props = data_type_props.copy()
        if 'style' not in data_type_props:
            data_type_props['style'] = {'color': 'black'}
        if 'children' not in data_type_props:
            data_type_props['children'] = 'No data type'

        data_props = data_props.copy()
        if 'options' not in data_props:
            data_props['options'] = ["?"]
        if 'value' not in data_props:
            data_props['value'] = data_props['options'][0]

        x_axis_type_props = x_axis_type_props.copy()
        if 'options' not in x_axis_type_props:
            x_axis_type_props['options'] = ['in time']
        if 'value' not in x_axis_type_props:
            x_axis_type_props['value'] = x_axis_type_props['options'][0]

        y_axis_type_props = y_axis_type_props.copy()
        if 'options' not in y_axis_type_props:
            y_axis_type_props['options'] = ['linear']
        if 'value' not in y_axis_type_props:
            y_axis_type_props['value'] = y_axis_type_props['options'][0]

        add_button_props = add_button_props.copy()
        if 'children' not in add_button_props:
            add_button_props['children'] = 'Add'

        layout = [
            dcc.Markdown(
                id = self.ids.data_type(aio_id),
                className = "graph-picker--header",
                **data_type_props,
            ),
            create_help_tip(tooltip_head, tooltip_body),
            html.H3('Plot', className="graph-picker--text"),
            dcc.RadioItems(
                id = self.ids.y_axis_type(aio_id),
                className = 'graph-picker--radioItems',
                **y_axis_type_props
            ),
            html.Div(
                dcc.Dropdown(
                    id = self.ids.data(aio_id),
                    **data_props,
                    clearable=False
                ),
                className="graph-picker--list",
            ),
            dcc.RadioItems(
                id=self.ids.x_axis_type(aio_id),
                className='graph-picker--radioItems',
                **x_axis_type_props
            ),
            html.Button(
                'Add',
                id=self.ids.add_button(aio_id),
                className="graph-picker--addButton"
            )
        ]

        super().__init__(layout, className='graph-picker--settings')



#function returning an element for the list of graphs
def create_element(
        data : str,
        x_type : str,
        y_type : str,
        list_options : list,
        list_values : list):
    """
    Function to create elements in a list of graphs.

    Args:
        data (str): The name of the dataset to be plotted.
        x_type (str): The type of x-axis representation; must be one of the following: 'in time', 'in distance', or 'as maps'.
        y_type (str): The scale type of the y-axis; must be either 'linear' or 'log'.
        list_options (list of str): A list of options corresponding to the graphs that the function will update.
        list_values (list of str): A list of values corresponding to the graphs that the function will update.

    Returns:
        tuple of lists of str: A tuple containing two lists:
            - The first list is the updated list of options.
            - The second list is the updated list of values.
    """
    value = y_type + '|' +  data + '|' + x_type

    if value in list_values: #if option exists return unchanged lists
        return list_options, list_values
    else: #if option doesn't exist add a new option to lists and return them
        option = {'label': data + f' ({x_type}) [{y_type}]', 'value': value}
        list_options.append(option)
        list_values.append(value)
        return list_options, list_values


def create_figure(
    data, # Dictionary with DataFrame's
    files,
    xaxis_data_name : str,
    xaxis_type,
    yaxis_data_name : str,
    yaxis_type,
    relative : bool,
    colorscale,
    unit_x : str,
    unit_y : str,
    mode   : str,
    ) -> go.Figure:

    fig = go.Figure()

    if not files:
        files = data.keys()

    for it, key in enumerate(files):
        dataname=key.split(".")[0].split(os.sep)[1].split("_")
        data_x = np.array(data[key][xaxis_data_name])
        data_y = np.array(data[key][yaxis_data_name])

        if relative:
            data_y -= data_y[0]

        fig.add_trace(
            go.Scattergl(
                x = data_x,
                y = data_y,
                mode=mode,
                line=dict(
                    width=5,
                    color=px.colors.sample_colorscale(colorscale, it/len(files))[0]
                ),
                name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
                hovertemplate='%{y:3.2e} ' + unit_y,
                xhoverformat='%{x:3.2e} ' + unit_x,
                hoverlabel={
                    'bgcolor' : px.colors.sample_colorscale(colorscale, it/len(files))[0]
                }
            )
        )

    fig.update_layout(
        title=dict(
            text=yaxis_data_name+" ("+xaxis_data_name+")",
            font=dict(size=22, family="Times New Roman")
        ),
        autosize=True,
        height=540,
        template='simple_white',
        paper_bgcolor='#B4A0AA',
        plot_bgcolor='#B4A0AA',
        margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, 
        hovermode='closest',
        hoverlabel=dict(
            font_size=16,
            font_family="Times New Roman"
        ),
    )

    fig.update_xaxes(
        title=dict(
            text=xaxis_data_name + " [" + unit_x + "]",
            font=dict(size=20, family="Times New Roman")
        ),
        type=xaxis_type,
        linewidth=4,
        mirror=True,
        side='bottom',
        ticklen=15,
        tickwidth=3,
        tickfont=dict(size=18, family="Times New Roman"),
        tickformat='%{y:3.2e} ' + unit_x,
        minor=dict(ticklen=10, tickwidth=2),
        showspikes=True,
    )

    fig.update_yaxes(
        title=dict(
            text = yaxis_data_name + " [" + unit_y + "]",
            font=dict(
                size=20,
                family="Times New Roman"
            )
        ),
        type = yaxis_type,
        linewidth=4,
        mirror=True,
        side='left',
        ticklen=15,
        tickwidth=3,
        tickfont=dict(
            size=18,
            family="Times New Roman"
        ),
        tickformat='f',
        minor=dict(
            ticklen=10,
            tickwidth=2
        ),
        showspikes=True,
    )

    return fig


def get_callbacks(data: dict):
    """
    A function that stores application callbacks responsible for updating the list of graphs and the graphs themselves.

    This function defines and registers the callbacks needed to dynamically update
    the list of graph options and the corresponding graph values within a Dash application.

    Args:
        df (dict): A DataFrame containing all the data from the specified directory with data files.
    """

    # GraphComponentAIO - a component which stores a graph and its settings.
    # A component is added to the list of graphs by using a Graph Picker panel.
    class GraphComponentAIO(html.Div):
        """
        A component that stores a graph component along with components responsible for updating the graph.

        This class extends html.Div and integrates a graph with its corresponding update mechanisms,
        allowing for dynamic updates and interactions within the Dash application.

        Args:
            html.Div (html.Div): The parent component from Dash's HTML library.
        """

        class ids:
            """
            A subclass of GraphComponentAIO class which stores ids for subcomomponents of GraphComenentAIO.
            """
            colorscale = lambda aio_id: {
                'component': 'GraphComponentAIO',
                'subcomponent': 'colorscaleDropdown',
                'aio_id': aio_id
            }
            relative = lambda aio_id: {
                'component': 'GraphComponentAIO',
                'subcomponent': 'relativeCheckbox',
                'aio_id': aio_id
            }
            line = lambda aio_id: {
                'component': 'GraphComponentAIO',
                'subcomponent': 'lineChecklist',
                'aio_id': aio_id
            }
            hovermode = lambda aio_id: {
                'component': 'GraphComponentAIO',
                'subcomponent': 'hovermodeRadioItems',
                'aio_id': aio_id
            }
            graph = lambda aio_id: {
                'component': 'GraphComponentAIO',
                'subcomponent': 'graph',
                'aio_id': aio_id
            }

        ids = ids #public class

        def __init__(
            self,
            xaxis_type        : str  = 'linear', # type of x axis
            xaxis_data_name   : str  = '', # data name of x axis
            yaxis_type        : str  = 'linear', # type of y axis
            yaxis_data_name   : str  = '', # data name of y axis
            colorscale_props  : dict = {}, # dropdown with available colorscales in ntg_colors
            colorscale_type   : str  = '', # type of colorscale
            relative_props    : dict = {}, # relative/normal checkbox
            line_props        : dict = {}, # lines/markers checklist
            hovermode_props   : dict = {}, # x unified/closest
            files             : list[str] = [], # files
            aio_id            : str = str(uuid.uuid4()) # id of All-in-one component
            ):
            """
            An init function for GraphComponentAIO.

            Args:
                xaxis_type (str, optional): a type of x axis (linear).
                xaxis_data_name (str, optional): a data name of x axis (one of three: in time, in distance, as maps).
                yaxis_type (str, optional): a type of y axis (linear or log).
                yaxis_data_name (str, optional): a data name of y axis (depends on data type).
                colorscale_props (dict, optional): a dictionary with properties for a dropdown storing available colorscales.
                colorscale_type (str, optional): name of colorscale.
                relative_props (dict, optional): a dictionary with properties for a checklist component, which sets or unsets relative values on the graph.
                line_props (dict, optional): a dictionary with properties for a checklost component storing information about if the data series on the graph should be displayed as lines, points or both.
                hovermode_props (dict, optional): a dictionary with properties for a radioitems component responsible for setting the hovermode of a graph (two available: closest, x unified).
            """
            # Initialize components' properties
            colorscale_props = colorscale_props.copy()
            if 'options' not in colorscale_props:
                colorscale_props['options'] = colorscales
            if 'value' not in colorscale_props:
                if colorscale_type == '':
                    colorscale_props['value'] = 'ntg_av'
                else:
                    colorscale_props['value'] = colorscale_type

            relative_props = relative_props.copy()
            if 'options' not in relative_props:
                relative_props['options'] = ['relative']
            if 'value' not in relative_props:
                if yaxis_data_name == "Total Energy":
                    relative_props['value'] = ['relative']
                else:
                    relative_props['value'] = []

            line_props = line_props.copy()
            if 'options' not in line_props:
                line_props['options'] = ['lines', 'markers']
            if 'value' not in line_props:
                line_props['value'] = ['lines']

            hovermode_props = hovermode_props.copy()
            if 'options' not in hovermode_props:
                hovermode_props['options'] = ['closest', 'x unified']
            if 'value' not in hovermode_props:
                hovermode_props['value'] = 'closest'

            # create a figure
            # [in time/in distance/as maps]
            if xaxis_data_name == 'in time':
                xaxis_data_name = 'Time'
            elif xaxis_data_name == 'in distance':
                xaxis_data_name = 'Distance'
            elif xaxis_data_name == 'as maps':
                xaxis_data_name = 'Maps'

            # TODO: When we plot in time give minimum value -1
            # xrange_min = -50 if xaxis_data_name == 'Time' else -1

            fig = create_figure(
                data = data,
                files = files,
                xaxis_data_name = xaxis_data_name,
                xaxis_type = xaxis_type,
                yaxis_data_name = yaxis_data_name,
                yaxis_type = yaxis_type,
                relative = relative_props['value'] == ['relative'],
                colorscale = ntg_colors.ntg_av,
                unit_x = units[xaxis_data_name],
                unit_y = units[yaxis_data_name],
                mode = 'lines'
            )

            layout = [
                dcc.Graph(
                    figure=fig,
                    id=self.ids.graph(aio_id),
                    className='graph-graph'
                ),
                html.H3("Graph settings", className="graph-settings--title"),
                html.Div([
                    html.Div([
                        dcc.Markdown("Colorscale"),
                        dcc.Dropdown(id = self.ids.colorscale(aio_id), **colorscale_props, clearable=False)
                    ], className = "graph-settings--colorscale"),
                    html.Div([
                        html.Div([
                            dcc.Markdown("Data:"),
                            dcc.Checklist(id = self.ids.relative(aio_id), **relative_props)
                        ], className="graph-settings--additional-data"),
                        html.Div([
                            dcc.Markdown("Show:"),
                            dcc.Checklist(id = self.ids.line(aio_id), **line_props)
                        ], className="graph-settings--additional-show"),
                        html.Div([
                            dcc.Markdown("Hovermode:"),
                            dcc.RadioItems(id = self.ids.hovermode(aio_id), **hovermode_props)
                        ], className="graph-settings--additional-hovermode")
                    ], className = "graph-settings--additional")
                ], className = "graph-settings--container"),
            ]

            super().__init__(layout)

        # Callback fired when user changes settings or filters are updated
        @callback(
            Output(ids.graph(MATCH), 'figure'),
            # Options for user
            Input(ids.relative(MATCH), 'value'),
            Input(ids.line(MATCH), 'value'),
            Input(ids.hovermode(MATCH), 'value'),
            Input(ids.colorscale(MATCH), 'value'),
            # Files from filter
            Input('filtered_files', 'data'),
            State(ids.graph(MATCH), 'figure'),
            prevent_initial_call = True
        )
        def update_graph(relative, line, hovermode, colorscale, files, figure):
            """
            A function for updating a graph. The function is a callback assigned to a specific GraphComponentAIO.

            Args:
                relative (list of strings): information whether data are relative or not. If a checkbox for relative is not set, the list is empty, otherwise it contains a string 'relative'.
                line (list of strings): contains information about how to draw the series on graph (available values: lines, markers. Can be one of these, a combination of these two or none).
                hovermode (string): name of a hovermode (one of two: closest, x unified).
                colorscale (string): name of a colorscale.
                files (list of strings): contains all names of data files after filtering. Only data from these files will be displayed.
                figure (go.Figure): a figure of a graph before an update.

            Returns:
                go.Figure: a figure of an updated graph.
            """
            xaxis_data_name = figure['layout']['xaxis']['title']['text'].split(" [")[0]
            yaxis_data_name = figure['layout']['yaxis']['title']['text'].split(" [")[0]

            if colorscale == 'ntg':
                colorscale = ntg_colors.ntg
            elif colorscale == 'ntg_map':
                colorscale = ntg_colors.ntg_map
            elif colorscale == 'ntg_av':
                colorscale = ntg_colors.ntg_av

            mode = 'lines'
            if line == ['markers']:
                mode = 'markers'
            elif 'lines' in line and 'markers' in line:
                mode = 'lines+markers'

            # TODO: If the files is empty we might want to print info
            # instead of just displaying everything
            if not files:
                files = data.keys()

            # If the callback was trggered by changed filters,
            # we want to create new figure and return it,
            # otherwise quicker Patch() will be better
            if (ctx.triggered_id == 'filtered_files'):
                fig = create_figure(
                    data = data,
                    files = files,
                    xaxis_data_name = xaxis_data_name,
                    xaxis_type = figure['layout']['xaxis']['type'],
                    yaxis_data_name = yaxis_data_name,
                    yaxis_type = figure['layout']['yaxis']['type'],
                    relative = relative == ['relative'],
                    colorscale = ntg_colors.ntg_av,
                    unit_x = units[xaxis_data_name],
                    unit_y = units[yaxis_data_name],
                    mode = mode,
                )
                fig.update_layout(hovermode = hovermode)
                return fig

            # Simpler settings can use patching funcionality,
            # we do not have to create figure from scrach,
            # TODO: Maybe filters can also use Patch() ?
            patched_figure = Patch()
            patched_figure.layout.hovermode = hovermode

            for it, key in enumerate(files):
                data_x = data[key][xaxis_data_name]
                data_y = data[key][yaxis_data_name]

                patched_figure.data[it].x = data_x
                if relative == ['relative']:
                    patched_figure.data[it].y = data_y - data_y[0]
                else:
                    patched_figure.data[it].y = data_y

                patched_figure.data[it].line.color = px.colors.sample_colorscale(colorscale, it/len(files))[0]
                patched_figure.data[it].mode = mode

            return patched_figure


    # Updating list of graphs
    @callback(
        #list of graphs
        Output('list-of-graphs', 'options'),
        Output('list-of-graphs', 'value'),
        # Buttons
        Input(GraphPickerAIO.ids.add_button('conservation'), 'n_clicks'),
        Input(GraphPickerAIO.ids.add_button('center-of-mass'), 'n_clicks'),
        Input(GraphPickerAIO.ids.add_button('deformation'), 'n_clicks'),
        Input(GraphPickerAIO.ids.add_button('pairing'), 'n_clicks'),
        Input('list-of-graphs', 'options'),
        Input('list-of-graphs', 'value'),
        # conservation
        State(GraphPickerAIO.ids.x_axis_type('conservation'), 'value'),
        State(GraphPickerAIO.ids.y_axis_type('conservation'), 'value'),
        State(GraphPickerAIO.ids.data('conservation'), 'value'),
        # center of mass
        State(GraphPickerAIO.ids.x_axis_type('center-of-mass'), 'value'),
        State(GraphPickerAIO.ids.y_axis_type('center-of-mass'), 'value'),
        State(GraphPickerAIO.ids.data('center-of-mass'), 'value'),
        # deformation
        State(GraphPickerAIO.ids.x_axis_type('deformation'), 'value'),
        State(GraphPickerAIO.ids.y_axis_type('deformation'), 'value'),
        State(GraphPickerAIO.ids.data('deformation'), 'value'),
        # pairing
        State(GraphPickerAIO.ids.x_axis_type('pairing'), 'value'),
        State(GraphPickerAIO.ids.y_axis_type('pairing'), 'value'),
        State(GraphPickerAIO.ids.data('pairing'), 'value'),
        prevent_initial_call = True,
    )
    # function for updating a dropdown component storing the list of graphs
    def update_list_of_graphs(b1, b2, b3, b4, 
                              list_options, list_values,
                              cx, cy, cdata,
                              cmx, cmy, cmdata,
                              dx, dy, ddata,
                              px, py, pdata):
        #check which button was trigerred
        """A callback for updating a list of graphs.

        Args:
            b1 (int): number of clicks of button 1.
            b2 (int): number of clicks of button 2.
            b3 (int): number of clicks of button 3.
            b4 (int): number of clicks of button 4.
            list_options (list of strings): list of options of a list of graphs dropdown.
            list_values (list of string): list of values of a list of graphs dropdown.
            cx (string): name of x axis data for conservation data type.
            cy (string): name of y axis type for conservation data type.
            cdata (string): name of y axis data for conservation data type.
            cmx (string): name of x axis data for center of mass data type.
            cmy (string): name of y axis type for center of mass data type.
            cmdata (string): name of y axis data for center of mass data type.
            dx (string): name of x axis data for deformation data type.
            dy (string): name of y axis type for deformation data type.
            ddata (string): name of y axis data for deformation data type.
            px (string): name of x axis data for pairing data type.
            py (string): name of y axis type for pairing data type.
            pdata (string): name of y axis data for pairing data type.

        Raises:
            PreventUpdate: prevents from firing a callback when application is opened for the first time.

        Returns:
            tuple of two lists of strings/empty lists: lists contain options and values for a list of graphs dropdown after adding them by pressing a certain add button on Graph picker panel of main menu. 
        """
        trigerred_id = ctx.triggered_id

        #add new graph to the list
        if trigerred_id == GraphPickerAIO.ids.add_button('conservation'):
            return create_element(cdata, cx, cy , list_options, list_values)
        elif trigerred_id == GraphPickerAIO.ids.add_button('center-of-mass'):
            return create_element(cmdata, cmx, cmy, list_options, list_values)
        elif trigerred_id == GraphPickerAIO.ids.add_button('deformation'):
            return create_element(ddata, dx, dy, list_options, list_values)
        elif trigerred_id == GraphPickerAIO.ids.add_button('pairing'):
            return create_element(pdata, px, py, list_options, list_values)

        # In case every value was cleared, there is are no options
        if list_values == []:
            return [], []

        to_remove = {}
        for option in list_options:
            for value in list_values:
                if option["value"] != value:
                    to_remove = option
                    break;

        list_options.remove(to_remove)
        return list_options, list_values


    @callback(
        Output('graphs', 'children'),
        Input('list-of-graphs', 'value'),
        Input('filtered_files', 'data'),
        State('graphs', 'children'),
        prevent_initial_call=True,
    )
    def update_graphs(values, files, graphs):
        """
        A callback responsible for updating a div with graphs. The callback can be fired by 
        a) adding a new graph to the list with add button on a graph picker panel,
        b) removing elements from a list of graphs dropdown by clicking on one
           specific element or by pressing an x in the right side of the component.

        Args:
            values (list[str]): a list containing values of list of graphs dropdown.
            graphs (list[GraphComponentAIOs]): the state of a div containing all the graphs before an update.
            files (list[str]): contains the names of files after filtering. Only data from the files will be displayed on a graph.

        Returns:
            a div containing GraphComponentAIOs: an updated state of a div storing all graphs that are mentioned in a list of graphs dropdown.
        """
        if len(graphs) == len(values):
            return Patch()

        # When a graph was deleted from the list.
        if len(graphs) > len(values):
            if len(values) == 0:
                return []

            for gcomp_aio in graphs:
                # GraphComponentAIO's first child is a graph, take it's aio_id
                id = gcomp_aio['props']['children'][0]['props']['id']['aio_id']

                if id not in values:
                    graphs.remove(gcomp_aio)

            return graphs

        # When pressing add user adds only one graph at the end of list,
        # and this for loop is equvalent to just taking i = -1,
        # but when loading from url this just len(values) graphs,
        for i in range(len(graphs), len(values)):
            value = values[i]
            info = value.split('|')
            yaxis_type = info[0] # [linear/log]
            xaxis_type = 'linear'
            yaxis_data_name = info[1]
            xaxis_data_name = info[2]

            aio_id = yaxis_type + '|' + yaxis_data_name + '|' + info[2]

            graph_component = GraphComponentAIO(
                xaxis_type=xaxis_type,
                xaxis_data_name=xaxis_data_name,
                yaxis_type=yaxis_type,
                yaxis_data_name= yaxis_data_name,
                colorscale_type='ntg_av',
                files=files,
                aio_id=aio_id
            )

            graphs.append(graph_component)

        return graphs
