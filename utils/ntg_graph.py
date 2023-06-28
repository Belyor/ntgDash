from dash import Dash, dcc, html, callback, ctx, Input, Output, State, MATCH
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
import os
import uuid

from . import ntg_colors
colorscales=ntg_colors.colorscales

#Types of available data
symbols = {
    #Conservation
    "Total Energy": "Total_E",
    "Number of Protons": "N_p",
    "Number of Neutrons": "N_n",
    #Center of mass
    "X_cm": "X_rcm",
    "Y_cm": "X_rcm",
    "Z_cm": "Z_rcm",
    "X_cm for Protons": "X_rcm_p",
    "Y_cm for Protons": "Y_rcm_p",
    "Z_cm for Protons": "Z_rcm_p",
    "X_cm for Neutrons": "X_rcm_n",
    "Y_cm for Neutrons": "Y_rcm_n",
    "Z_cm for Neutrons": "Z_rcm_n",
    "Center of Mass Energy": "E_cm",
    #Deformation
    "Beta": "Beta",
    "Quadrupole Moment Q20": "Q20",
    "Octupole Moment Q30": "Q30",
    "Hexadecupole Moment Q40": "Q40",
    #Pairing
    "Pairing gap for Protons": "av_delta_p",
    "Pairing gap for Neutrons": "av_delta_n",
    #Misc
    #x axis
    "in time": "(t)",
    "in distance": "(dist)",
    "as maps": "map",
    #y axis
    "linear": "lin",
    "log": "log"
}
#groups of data
groups = {
    "conservation": ["Total Energy","Number of Protons","Number of Neutrons"],
    "center of mass": ["X_cm","Y_cm","Z_cm","X_cm for Protons","Y_cm for Protons","Z_cm for Protons",
                    "X_cm for Neutrons","Y_cm for Neutrons","Z_cm for Neutrons","Center of Mass Energy"],
    "deformation": ["Beta","Quadrupole Moment Q20","Octupole Moment Q30","Hexadecupole Moment Q40"],
    "pairing": ["Pairing gap for Protons","Pairing gap for Neutrons"]
    #'mics'
}

units = {
    #Conservation
    "Total Energy": "MeV",
    "Number of Protons": "",
    "Number of Neutrons": "",
    #Center of mass
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
    #Deformation
    "Beta": "",
    "Quadrupole Moment Q20": "b",
    "Octupole Moment Q30": "b^3/2",
    "Hexadecupole Moment Q40": "b^2",
    #Pairing
    "Pairing gap for Protons": "MeV",
    "Pairing gap for Neutrons": "MeV",
    #Misc
    #x axis
    "Time": "fm/c",
    "Distance": "fm"
}

#GraphPickerAIO - a component which stores settings available in Graph Picker panel in main menu
class GraphPickerAIO(html.Div):
    """A class for an All-in-one component whcich stores components for graph settings available in Graph-Picker panel of main menu.

    Args:
        html.Div (html.Div): the parent component
    """
    class ids:
        """A subclass of GraphPickerAIO containing ids of each subcomponent of GraphPickerAIO.
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
    ids = ids #public class

    #Arguments definition
    def __init__(
        self,
        data_type_props = None,
        data_props = None,
        x_axis_type_props = None,
        y_axis_type_props = None,
        add_button_props = None,
        aio_id = None
    ):
        """An init function for GraphPickerAIO component.

        Args:
            data_type_props (dict, optional): a dictionary with properties for a markdown describing a data type (one of five: conservation, center of mass, deformation, pairing, misc).
            data_props (dict, optional): a dictionary with properties for a dropdown containing names of datas available for a given data type.
            x_axis_type_props (dict, optional): a dictionary with properties for radioitems component containing information about what value is on an x axis of a graph (a subset of these three available values: in time, in distance, as maps).
            y_axis_type_props (dict, optional): a dictionary with properties for radioitems component containng information about what the type of y axis is (linear or logarithmic).
            add_button_properties (dict, optional): a dictionary with properties for a button which adds a graph to a graph list. Defaults to None.
            aio_id (string, optional): an id of GraphPickerAIO component. Defaults to None.
        """
        #set components properties
        data_type_props = data_type_props.copy() if data_type_props else {}
        if 'style' not in data_type_props:
            data_type_props['style'] = {'color': 'black'}
        if 'children' not in data_type_props:
            data_type_props['children'] = 'No data type'

        data_props = data_props.copy() if data_props else {}
        if 'options' not in data_props:
            data_props['options'] = ["?"]
        if 'value' not in data_props:
            data_props['value'] = data_props['options'][0]
        
        x_axis_type_props = x_axis_type_props.copy() if x_axis_type_props else {}
        if 'options' not in x_axis_type_props:
            x_axis_type_props['options'] = {'disabled': False, 'label': 'in time', 'value': 'in time'}
        if 'value' not in x_axis_type_props:
            x_axis_type_props['value'] = x_axis_type_props['options'][0]

        y_axis_type_props = y_axis_type_props.copy() if y_axis_type_props else {}
        if 'options' not in y_axis_type_props:
            y_axis_type_props['options'] = {'disabled': False, 'label': 'linear', 'value': 'linear'}
        if 'value' not in y_axis_type_props:
            y_axis_type_props['value'] = y_axis_type_props['options'][0]
        
        add_button_props = add_button_props.copy() if add_button_props else {}
        if 'children' not in add_button_props:
            add_button_props['children'] = 'Add'

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        radio_items_class_x = ''
        radio_items_class_y = ''

        if len(x_axis_type_props['options']) == 3:
            x_axis_type_props['options'] = [{'label':'in time','value':'in time'},
                                            {'label':'in distance','value':'in distance'},
                                            {'label':'as maps','value':'as maps','disabled':True}]
            radio_items_class_x = "graph-picker--radioItemsThreeOptions"
        elif len(x_axis_type_props['options']) == 1:
            radio_items_class_x = "graph-picker--radioItemsOneOption"
        
        if len(y_axis_type_props['options']) == 3:
            radio_items_class_y = "graph-picker--radioItemsThreeOptions"
        elif len(x_axis_type_props['options']) == 2:
            radio_items_class_y = "graph-picker--radioItemsTwoOptions"
        elif len(x_axis_type_props['options']) == 1:
            radio_items_class_y = "graph-picker--radioItemsOneOption"
            
        layout = html.Div([
            html.Div([
                dcc.Markdown(id = self.ids.data_type(aio_id), **data_type_props)
            ], className = "graph-picker--header"),
            html.Div([
                html.H3('Plot')
            ], className="graph-picker--text"),
            html.Div([
                dcc.RadioItems(id = self.ids.y_axis_type(aio_id), **y_axis_type_props)
            ], className = radio_items_class_y),
            html.Div([
                dcc.Dropdown(id = self.ids.data(aio_id), **data_props, clearable=False)
            ], className="graph-picker--list"),
            html.Div([
                dcc.RadioItems(id = self.ids.x_axis_type(aio_id), **x_axis_type_props)
            ], className = radio_items_class_x),
            html.Button('Add', id=self.ids.add_button(aio_id),className="graph-picker--addButton")
        ], className='graph-picker--settings')

        super().__init__(layout)



#function returning an element for the list of graphs
def create_element(data, x_type, y_type, list_options, list_values):
    """A function for creating elements for list of graphs.

    Args:
        data (string): name of data (the one on y axis).
        x_type (string): name of x axis (one of three: in time, in distance, as maps).
        y_type (string): name of y axis type (one of two: linear, log).
        list_options (list of strings): options from list of graphs, which a function will update.
        list_values (list of strings): values from list of graphs, which a function will update.

    Returns:
        tuple of lists of strings: first value is an updated list of options, and second is an updated list of values.
    """
    options = list_options
    values = list_values
    value = y_type + '|' +  data + '|' + x_type
    exists = False #does an option already exist?
    for v in values:
        if value == v:
            exists = True
            break
    
    if exists: #if option exists return unchanged lists
        return options, values
    else: #if option doesn't exist add a new option to lists and return them
        label = symbols[data]
        option = {'label': label, 'value': value}
        options.append(option)
        values.append(value)
        return options, values


def get_callbacks(app: Dash, df: pd.DataFrame):
    """A function storing applications callbacks responsible for updating list of graphs and graphs themselves.

    Args:
        app (Dash): a Dash application.
        df (pd.DataFrame): a DataFrame storing all the data from a directory with data files.
    """

    # GraphComponentAIO - a component which stores a graph and its settings.
    # A component is added to the list of graphs by using a Graph Picker panel.
    class GraphComponentAIO(html.Div):
        """A component which stores both a graph component and components responsible for updating the graph.

        Args:
            html.Div (html.Div): the parent component
        """
        class ids:
            """A subclass of GraphComponentAIO class which stores ids for subcomomponents of GraphComenentAIO.
            """
            y_axis_type = lambda aio_id: {
                'component': 'GraphComponentAIO',
                'subcomponent': 'yRadioItems',
                'aio_id': aio_id
            }
            x_axis_type = lambda aio_id: {
                'component': 'GraphComponentAIO',
                'subcomponent': 'xRadioItems',
                'aio_id': aio_id
            }
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
            #properties
            x_axis_type_props = None, # one of three: in time, in distance, as maps
            xaxis_type = None, # type of x axis
            xaxis_data_name = None, # data name of x axis
            y_axis_type_props = None, # one of two: linear, log
            yaxis_type = None, # type of y axis
            yaxis_data_name = None, # data name of y axis
            colorscale_props = None, # dropdown with available colorscales in ntg_colors
            colorscale_type = None, # type of colorscale
            relative_props = None, # relative/normal checkbox
            line_props = None, # lines/markers checklist
            hovermode_props = None, # x unified/closest
            files = None, # files
            aio_id = None # id of All-in-one component
        ):
            """An init function for GraphComponentAIO.

            Args:
                x_axis_type_props (dict, optional): a dictionary with properties for radioitems component storing information about x axis value (one of three available: in time, in distance, as maps).
                xaxis_type (string, optional): a type of x axis (linear). Defaults to None.
                xaxis_data_name (string, optional): a data name of x axis (one of three: in time, in distance, as maps). Defaults to None.
                y_axis_type_props (dict, optional): a dictionary with properties for radioitems component storing information about y axis type (linear or log). Defaults to None.
                yaxis_type (string, optional): a type of y axis (linear or log). Defaults to None.
                yaxis_data_name (string, optional): a data name of y axis (depends on data type). Defaults to None.
                colorscale_props (dict, optional): a dictionary with properties for a dropdown storing available colorscales. Defaults to None.
                colorscale_type (string, optional): name of colorscale. Defaults to None.
                relative_props (dict, optional): a dictionary with properties for a checklist component, which sets or unsets relative values on the graph. Defaults to None.
                line_props (dict, optional): a dictionary with properties for a checklost component storing information about if the data series on the graph should be displayed as lines, points or both. Defaults to None.
                hovermode_props (dict, optional): a dictionary with properties for a radioitems component responsible for setting the hovermode of a graph (two available: closest, x unified). Defaults to None.

            """
            # Initialize components' properties
            x_axis_type_props = x_axis_type_props.copy() if x_axis_type_props else {}
            if 'options' not in x_axis_type_props:
                x_axis_type_props['options'] = {'disabled': False, 'label': 'in time', 'value': 'in time'}
            if 'value' not in x_axis_type_props:
                if xaxis_data_name is None:
                    x_axis_type_props['value'] = x_axis_type_props['options'][0]
                else:
                    x_axis_type_props['value'] = xaxis_data_name
    
            y_axis_type_props = y_axis_type_props.copy() if y_axis_type_props else {}
            if 'options' not in y_axis_type_props:
                y_axis_type_props['options'] = {'disabled': False, 'label': 'linear', 'value': 'linear'}
            if 'value' not in y_axis_type_props:
                if yaxis_type is None:
                    y_axis_type_props['value'] = y_axis_type_props['options'][0]
                else:
                    y_axis_type_props['value'] = yaxis_type
    
            colorscale_props = colorscale_props.copy() if colorscale_props else {}
            if 'options' not in colorscale_props:
                colorscale_props['options'] = colorscales
            if 'value' not in colorscale_props:
                if colorscale_type is None:
                    colorscale_props['value'] = 'ntg_av'
                else:
                    colorscale_props['value'] = colorscale_type

            relative_props = relative_props.copy() if relative_props else {}
            if 'options' not in relative_props:
                relative_props['options'] = ['relative']
            if 'value' not in relative_props:
                if yaxis_data_name == "Total Energy":
                    relative_props['value'] = ['relative']
                else:
                    relative_props['value'] = []
            
            line_props = line_props.copy() if line_props else {}
            if 'options' not in line_props:
                line_props['options'] = ['lines', 'markers']
            if 'value' not in line_props:
                line_props['value'] = ['lines']
            
            hovermode_props = hovermode_props.copy() if hovermode_props else {}
            if 'options' not in hovermode_props:
                hovermode_props['options'] = ['closest', 'x unified']
            if 'value' not in hovermode_props:
                hovermode_props['value'] = 'closest'
    
            if aio_id is None:
                aio_id = str(uuid.uuid4())

            #create a figure
            #[in time/in distance/as maps]
            if xaxis_data_name == 'in time':
                xaxis_data_name = 'Time'
            elif xaxis_data_name == 'in distance':
                xaxis_data_name = 'Distance'
            elif xaxis_data_name == 'as maps':
                xaxis_data_name = 'Maps'
            
            colorscale = ntg_colors.ntg_av
            
            unit_x = units[xaxis_data_name]
            unit_y = units[yaxis_data_name]
            
            # filter out keys from dataframe
            xrange_min=-50 if xaxis_data_name == 'Time' else -1
            xrange_max=[]
            fig=go.Figure()

            if not files: # if files is empty
                files = df.keys()
            
            for key, it in zip(files, range(len(files))):
                dataname=key.split(".")[0].split(os.sep)[1].split("_")
                dff_data_x=df[key][xaxis_data_name]
                dff_data_y=df[key][yaxis_data_name]

                ydata=np.array(dff_data_y)
                if relative_props['value'] == ['relative']:
                    for i in range(len(ydata)):
                        ydata[i] -= dff_data_y[0]
                fig.add_trace(go.Scattergl(
                    x=np.array(dff_data_x),
                    y=ydata,
                    mode='lines',
                    line=dict(width=5, color=px.colors.sample_colorscale(
                        colorscale, it/len(files))[0]),
                    name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
                    hovertemplate = '%{y:3.2e} ' + unit_y,
                    xhoverformat='%{x:3.2e} ' + unit_x,
                    hoverlabel=dict(bgcolor=px.colors.sample_colorscale(
                        colorscale, it/len(files))[0])
                    )
                )
                xrange_max.append(max(dff_data_x))
            
            if not xrange_max:
                xrange_max.append(10)

            fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
                                         font=dict(size=22, family="Times New Roman")),
                              autosize=True,height=540,
                              template='simple_white',paper_bgcolor='#B4A0AA',plot_bgcolor='#B4A0AA',
                              margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, 
                              hovermode='closest',
                              hoverlabel=dict(
                                font_size=16,
                                font_family="Times New Roman"),
                              )

            fig.update_xaxes(title=dict(text=xaxis_data_name + " [" + unit_x + "]",
                                        font=dict(size=20, family="Times New Roman")),
                             range=[xrange_min, max(xrange_max)],
                             type=xaxis_type, linewidth=4, mirror=True, side='bottom',
                             ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                             tickformat='%{y:3.2e} ' + unit_x,
                             minor=dict(ticklen=10, tickwidth=2),
                             showspikes=True)

            fig.update_yaxes(title=dict(text=yaxis_data_name + " [" + unit_y + "]",
                                        font=dict(size=20, family="Times New Roman")),
                             type=yaxis_type, linewidth=4, mirror=True, side='left',
                             ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                             tickformat='f',
                             minor=dict(ticklen=10, tickwidth=2),
                             showspikes=True)

            layout = html.Div([
                html.Div(dcc.Graph(figure=fig, id = self.ids.graph(aio_id) ,className='graph-graph')),
                html.Div(html.H3("Graph settings"), className="graph-settings--title"),
                html.Div([
                    html.Div([
                        dcc.Markdown('Y axis:'), 
                        dcc.RadioItems(id = self.ids.y_axis_type(aio_id), **y_axis_type_props),
                    ], className="graph-settings--yAxis"),
                    html.Div([
                        dcc.Markdown('X axis:'),
                        dcc.RadioItems(id = self.ids.x_axis_type(aio_id), **x_axis_type_props),
                    ], className="graph-settings--xAxis"),
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
                ], className = "graph-settings--container")
            ])
    
            super().__init__(layout)
    
        @callback(
            Output(ids.graph(MATCH), component_property='figure'),
            Input(component_id='files_out', component_property='options'),
            Input(ids.x_axis_type(MATCH), 'value'),
            Input(ids.y_axis_type(MATCH), 'value'),
            Input(ids.relative(MATCH), 'value'),
            Input(ids.line(MATCH), 'value'),
            Input(ids.hovermode(MATCH), 'value'),
            Input(ids.colorscale(MATCH), 'value'),
            Input(ids.graph(MATCH), component_property='figure'),
            prevent_initial_call = True
        )
        # method for updating a graph in a GraphComponentAIO
        def update_graph(files, x_data, y_type, relative, line, hovermode, colorscale ,figure: go.Figure):
            """A function for updating a graph. The function is a callback assigned to a specific GraphComponentAIO.

            Args:
                files (list of strings): contains all names of data files after filtering. Only data from these files will be displayed.
                x_data (string): name of x axis data (one of three: in time, in distance, as maps).
                y_type (string): type of y axis (one of two: linear, log).
                relative (list of strings): information whether data are relative or not. If a checkbox for relative is not set, the list is empty, otherwise it contains a string 'relative'.
                line (list of strings): contains information about how to draw the series on graph (available values: lines, markers. Can be one of these, a combination of these two or none).
                hovermode (string): name of a hovermode (one of two: closest, x unified).
                colorscale (string): name of a colorscale.
                figure (go.Figure): a figure of a graph before an update.

            Returns:
                go.Figure: a figure of an updated graph.
            """
            fig = go.Figure()
            yaxis_data_name = figure['layout']['yaxis']['title']['text'].split(" [")[0]
            xaxis_data_name = figure['layout']['xaxis']['title']['text'].split(" [")[0]

            # Change x type + colorscale + lines/markers
            if x_data == 'in time':
                x_data = 'Time'
            elif x_data == 'in distance':
                x_data = 'Distance'
            elif x_data == 'as maps':
                x_data = 'Maps'

            if xaxis_data_name != x_data:
                xaxis_data_name = x_data
            
            # filter out keys from dataframe
            xrange_min=-50 if xaxis_data_name == 'Time' else -1
            xrange_max=[]

            unit_x = units[xaxis_data_name]
            unit_y = units[yaxis_data_name]

            if not files: # if files is empty
                files = df.keys()

            for key, it in zip(files, range(len(files))):
                dataname=key.split(".")[0].split(os.sep)[1].split("_")
                dff_data_x=df[key][xaxis_data_name]
                dff_data_y=df[key][yaxis_data_name]

                # Change colorscale
                if colorscale == 'ntg':
                    colorscale = ntg_colors.ntg
                elif colorscale == 'ntg_map':
                    colorscale = ntg_colors.ntg_map
                elif colorscale == 'ntg_av':
                    colorscale = ntg_colors.ntg_av

                ydata=np.array(dff_data_y)
                if relative == ['relative']:
                    for i in range(len(ydata)):
                        ydata[i] -= dff_data_y[0]
                fig.add_trace(go.Scattergl(
                    x=np.array(dff_data_x),
                    y=ydata,
                    mode='lines',
                    line=dict(width=5, color=px.colors.sample_colorscale(
                        colorscale, it/len(files))[0]),
                    name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
                    hovertemplate = '%{y:3.2e} ' + unit_y,
                    xhoverformat='%{x:3.2e} ' + unit_x,
                    hoverlabel=dict(bgcolor=px.colors.sample_colorscale(
                        colorscale, it/len(files))[0])
                    ) # todo hover label color
                )
                xrange_max.append(max(dff_data_x))
            
            if not xrange_max:
                xrange_max.append(10)

            fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
                                         font=dict(size=22, family="Times New Roman")),
                              autosize=True,height=540,
                              template='simple_white',paper_bgcolor='#B4A0AA',plot_bgcolor='#B4A0AA',
                              margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, 
                              hovermode=hovermode,
                              hoverlabel=dict(
                                font_size=16,
                                font_family="Times New Roman"), # todo fix hover label. color of the hover title background should be the inverted color of the data, i.e. if colro is black then background is white
                              )

            fig.update_xaxes(title=dict(text=xaxis_data_name + " [" + unit_x + "]",
                                        font=dict(size=20, family="Times New Roman")),
                             range=[xrange_min, max(xrange_max)],
                             type='linear', linewidth=4, mirror=True, side='bottom',
                             ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                             tickformat='%{y:3.2e} ' + unit_x,
                             minor=dict(ticklen=10, tickwidth=2),
                             showspikes=True)
            
            fig.update_yaxes(title=dict(text=yaxis_data_name + " [" + unit_y + "]",
                                        font=dict(size=20, family="Times New Roman")),
                             type=y_type, linewidth=4, mirror=True, side='left',
                             ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
                             tickformat='f',
                             minor=dict(ticklen=10, tickwidth=2),
                             showspikes=True)
            
            if line == ['lines']:
                fig.update_traces(mode='lines')
            elif line == ['markers']:
                fig.update_traces(mode='markers')
            elif 'lines' in line and 'markers' in line:
                fig.update_traces(mode='lines+markers')

            return fig


    # Updating list of graphs
    @app.callback(
        #list of graphs
        Output(component_id='list-of-graphs', component_property='options'),
        Output(component_id='list-of-graphs', component_property='value'),
        #conservation add button
        Input(component_id=GraphPickerAIO.ids.add_button('conservation'), component_property='n_clicks'),
        Input(component_id=GraphPickerAIO.ids.add_button('center-of-mass'), component_property='n_clicks'),
        Input(component_id=GraphPickerAIO.ids.add_button('deformation'), component_property='n_clicks'),
        Input(component_id=GraphPickerAIO.ids.add_button('pairing'), component_property='n_clicks'),
        #graphs' list of options
        Input(component_id='list-of-graphs', component_property='options'),
        Input(component_id='list-of-graphs', component_property='value'),
        #conservation x-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'conservation'}, component_property='value'),
        #conservation y-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'conservation'}, component_property='value'),
        #conservation data
        State({'component': 'GraphPickerAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'conservation'}, component_property='value'),
        #center of mass x-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'center-of-mass'}, component_property='value'),
        #center of mass y-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'center-of-mass'}, component_property='value'),
        #center of mass data
        State({'component': 'GraphPickerAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'center-of-mass'}, component_property='value'),
        #deformation x-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'deformation'}, component_property='value'),
        #deformation y-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'deformation'}, component_property='value'),
        #deformation data
        State({'component': 'GraphPickerAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'deformation'}, component_property='value'),
        #pairing x-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'pairing'}, component_property='value'),
        #pairing y-axis
        State({'component': 'GraphPickerAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'pairing'}, component_property='value'),
        #pairing data
        State({'component': 'GraphPickerAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'pairing'}, component_property='value'),
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
        #delete graphs from the list
        elif trigerred_id == 'list-of-graphs':
            if list_values == []:
                return [], []
            else:
                options = list_options
                to_remove = {}
                for i in range(0, len(list_options)):
                    delete = True
                    for value in list_values:
                        if list_options[i]["value"] == value:
                            delete = False
                            break
                    if delete == True:
                        to_remove = list_options[i]
                        break
                
                options.remove(to_remove)
                return options, list_values
        #prevent updating when no add button was pressed
        if (b1 and b2 and b3 and b4) is None:
            raise PreventUpdate
    
    # Updating graphs
    @app.callback(
        Output(component_id='graphs', component_property='children'),
        Input(component_id='list-of-graphs', component_property='value'),
        State(component_id='graphs', component_property='children'),
        State(component_id='files_out', component_property='options')
    )
    # function for updating graphs
    def update_graphs(values, graphs, files):
        """A callback responsible for updating a div with graphs. The callback can be fired by a) adding a new graph to the list with add button on a graph picker panel, b) removing elements from a list of graphs dropdown by clicking on one specific element or by pressing an x in the right side of the component.

        Args:
            values (list of strings): a list containing values of list of graphs dropdown.
            graphs (list of GraphComponentAIOs): the state of a div containing all the graphs before an update.
            files (list of strings): contains the names of files after filtering. Only data from the files will be displayed on a graph.

        Returns:
            a div containing GraphComponentAIOs: an updated state of a div storing all graphs that are mentioned in a list of graphs dropdown.
        """
        graphs_temp = graphs
        #when no graph was added to the list
        if len(graphs_temp) == len(values):
            return graphs_temp
        #when a graph was deleted from the list
        elif len(graphs_temp) > len(values):
            #if list of graphs is empty
            if len(values) == 0:
                graphs_temp.clear()
            #if one graph was deleted from the list
            else:
                to_remove = None
                for graph in graphs_temp:
                    id = graph['props']['id']
                    id = id.replace('-container','')
                    id = id.replace('--','|')
                    id = id.replace('-',' ')

                    delete = True

                    for value in values:
                        if id == value:
                            delete = False
                            break
                    
                    if delete == True:
                        to_remove = graph
                        graphs_temp.remove(to_remove)
                        break
            
            return graphs_temp
        elif len(graphs_temp) < len(values):
            value = values[-1] #last added value
            info = value.split('|')
            yaxis_type = info[0] #[linear/log]
            xaxis_type = 'linear'
            yaxis_data_name = info[1]
            xaxis_data_name = info[2]

            if yaxis_data_name in groups["conservation"]:
                x_options = ['in time']
                y_options = ['linear','log']
            elif yaxis_data_name in groups["center of mass"]:
                x_options = ['in time']
                y_options = ['linear']
            elif (yaxis_data_name in groups["deformation"]) or (yaxis_data_name in groups["pairing"]):
                x_options = [{'label':'in time','value':'in time'},
                            {'label':'in distance','value':'in distance'},
                            {'label':'as maps','value':'as maps','disabled':True}]
                y_options = ['linear', 'log']
            
            aio_id = yaxis_type + '--' + yaxis_data_name.replace(' ', '-') + '--' + info[2].replace(' ', '-')

            graph_component = GraphComponentAIO(
                x_axis_type_props={'options':x_options},
                xaxis_type=xaxis_type,
                xaxis_data_name=xaxis_data_name,
                y_axis_type_props={'options':y_options},
                yaxis_type=yaxis_type,
                yaxis_data_name= yaxis_data_name,
                colorscale_type='ntg_av',
                files=files,
                aio_id=aio_id
            )

            div = html.Div([
                graph_component
            ], id = aio_id + '-container')

            graphs_temp.append(div)
        
            return graphs_temp