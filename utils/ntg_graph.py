from dash import Dash, dcc, html, callback, ctx, Input, Output, State, MATCH
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
import math
import os
import uuid

from . import ntg_colors
colorscales=ntg_colors.colorscales

class GraphSettingsAIO(html.Div):
    class ids:
        data_type = lambda aio_id: {
            'component': 'GraphSettingsAIO',
            'subcomponent': 'markdown',
            'aio_id': aio_id
        }
        y_axis_type = lambda aio_id: {
            'component': 'GraphSettingsAIO',
            'subcomponent': 'yRadioItems',
            'aio_id': aio_id
        }
        data = lambda aio_id: {
            'component': 'GraphSettingsAIO',
            'subcomponent': 'dataDropdown',
            'aio_id': aio_id
        }
        x_axis_type = lambda aio_id: {
            'component': 'GraphSettingsAIO',
            'subcomponent': 'xRadioItems',
            'aio_id': aio_id
        }
        colorscale = lambda aio_id: {
            'component': 'GraphSettingsAIO',
            'subcomponent': 'colorscaleDropdown',
            'aio_id': aio_id
        }
        update = lambda aio_id: {
            'component': 'GraphSettingsAIO',
            'subcomponent': 'button',
            'aio_id': aio_id
        }
    ids = ids #public class

    #Arguments definition
    def __init__(
        self,
        #properties
        data_type_props = None, #one of five: conservation, center of mass, deformation, pairing, misc
        data_props = None, #available datas for certain data type
        x_axis_type_props = None, #one of three: in time, in distance, as maps
        y_axis_type_props = None, #one of two: linear, log
        colorscale_props = None, #dropdown with available colorscales in ntg_colors
        update_props = None, #update button
        is_picker = False, #weather graph_settings component is located under a graph or in graph picker
        aio_id = None #id of All-in-one component
    ):
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

        data = data_props['value'][0]
        
        x_axis_type_props = x_axis_type_props.copy() if x_axis_type_props else {}
        if 'options' not in x_axis_type_props:
            x_axis_type_props['options'] = {'disabled': False, 'label': 'in time', 'value': 'in time'}
        if 'value' not in x_axis_type_props:
            x_axis_type_props['value'] = x_axis_type_props['options'][0]

        xaxis = x_axis_type_props['value'][0]

        y_axis_type_props = y_axis_type_props.copy() if y_axis_type_props else {}
        if 'options' not in y_axis_type_props:
            y_axis_type_props['options'] = {'disabled': False, 'label': 'linear', 'value': 'linear'}
        if 'value' not in y_axis_type_props:
            y_axis_type_props['value'] = y_axis_type_props['options'][0]
        
        yaxis = y_axis_type_props['value'][0]

        colorscale_props = colorscale_props.copy() if colorscale_props else {}
        if 'options' not in colorscale_props:
            colorscale_props['options'] = colorscales
        if 'value' not in colorscale_props:
            colorscale_props['value'] = 'ntg'

        update_props = update_props.copy() if update_props else {}
        if 'children' not in update_props:
            update_props['children'] = 'Update'

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        #id of a graph
        self.graph_id = "graph--" + yaxis + "--" + data.replace(' ', '-') + "--" + xaxis.replace(' ', '-')

        radio_items_class_x = ''
        radio_items_class_y = ''

        if len(x_axis_type_props['options']) == 3:
            radio_items_class_x = "graph-picker--radioItemsThreeOptions"
        elif len(x_axis_type_props['options']) == 1:
            radio_items_class_x = "graph-picker--radioItemsOneOption"
        
        if len(y_axis_type_props['options']) == 3:
            radio_items_class_y = "graph-picker--radioItemsThreeOptions"
        elif len(x_axis_type_props['options']) == 2:
            radio_items_class_y = "graph-picker--radioItemsTwoOptions"
        elif len(x_axis_type_props['options']) == 1:
            radio_items_class_y = "graph-picker--radioItemsOneOption"

        if is_picker:
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
                    dcc.Dropdown(id = self.ids.data(aio_id), **data_props)
                ], className="graph-picker--list"),
                html.Div([
                    dcc.RadioItems(id = self.ids.x_axis_type(aio_id), **x_axis_type_props)
                ], className = radio_items_class_x)
            ], className='graph-picker--settings')
        else:
            layout = html.Div([
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
                    dcc.Dropdown(id = self.ids.colorscale(aio_id), **colorscale_props)
                ], className = "graph-settings--colorscale"),
                html.Button(id = self.ids.update(aio_id), **update_props, className="graph-settings--updateButton")
            ], className = "graph-settings--container")

        super().__init__(layout)

    #def get_graph_id(self):
    #    return self.graph_id
    #
    #@callback(
    #    #Output(component_id=get_graph_id(), component_property='figure'),
    #    Input(ids.update(MATCH),'n_clicks'),
    #    State(component_id=get_graph_id(), component_property='figure')
    #)
    #def update_graph(clicks, figure):
    #    print(figure)

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
}

#function returning an element for the list of graphs
def create_element(data, x_type, y_type, list_options, list_values):
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
    #Updating list of graphs
    @app.callback(
        #list of graphs
        Output(component_id='list-of-graphs', component_property='options'),
        Output(component_id='list-of-graphs', component_property='value'),
        #conservation add button
        Input(component_id='addButton-conservation', component_property='n_clicks'),
        Input(component_id='addButton-center-of-mass', component_property='n_clicks'),
        Input(component_id='addButton-deformation', component_property='n_clicks'),
        Input(component_id='addButton-pairing', component_property='n_clicks'),
        #graphs' list of options
        Input(component_id='list-of-graphs', component_property='options'),
        Input(component_id='list-of-graphs', component_property='value'),
        #conservation x-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'conservation'}, component_property='value'),
        #conservation y-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'conservation'}, component_property='value'),
        #conservation data
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'conservation'}, component_property='value'),
        #center of mass x-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'center-of-mass'}, component_property='value'),
        #center of mass y-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'center-of-mass'}, component_property='value'),
        #center of mass data
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'center-of-mass'}, component_property='value'),
        #deformation x-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'deformation'}, component_property='value'),
        #deformation y-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'deformation'}, component_property='value'),
        #deformation data
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'deformation'}, component_property='value'),
        #pairing x-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'xRadioItems', 'aio_id': 'pairing'}, component_property='value'),
        #pairing y-axis
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'yRadioItems', 'aio_id': 'pairing'}, component_property='value'),
        #pairing data
        State({'component': 'GraphSettingsAIO', 'subcomponent': 'dataDropdown', 'aio_id': 'pairing'}, component_property='value'),
    )
    def update_list_of_graphs(b1, b2, b3, b4, 
                  list_options, list_values,
                  cx, cy, cdata,
                  cmx, cmy, cmdata,
                  dx, dy, ddata,
                  px, py, pdata):
        #check which button was trigerred
        trigerred_id = ctx.triggered_id

        #add new graph to the list
        if trigerred_id == 'addButton-conservation':
            return create_element(cdata, cx, cy , list_options, list_values)
        elif trigerred_id == 'addButton-center-of-mass':
            return create_element(cmdata, cmx, cmy, list_options, list_values)
        elif trigerred_id == 'addButton-deformation':
            return create_element(ddata, dx, dy, list_options, list_values)
        elif trigerred_id == 'addButton-pairing':
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
    
    #Updating graphs
    @app.callback(
        Output(component_id='graphs', component_property='children'),
        Input(component_id='list-of-graphs', component_property='value'),
        State(component_id='graphs', component_property='children')
    )
    def update_graphs(values, graphs):
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
                    id = id.replace('container--','')
                    id = id.replace('--','|')
                    id = id.replace('-',' ')
                    print(id)

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
            #[in time/in distance/as maps]
            if info[2] == 'in time':
                xaxis_data_name = 'Time'
            elif info[2] == 'in distance':
                xaxis_data_name = 'Distance'
            elif info[2] == 'as maps':
                xaxis_data_name = 'Maps'
            
            colorscale = colorscales[-4]

            dff=df
            xrange_min=-50 if xaxis_data_name == 'Time' else -1
            xrange_max=[]
            fig=go.Figure()
            for key, it in zip(dff, range(len(dff))):
                dataname=key.split(".")[0].split(os.sep)[1].split("_")
                # Choose the plot type. Relative or not. Relative is in `if` statement,
                # while Normal is right below. 
                # # todo 1 this would also be in the Div graph option - the one that appears after plotting. 
                # # todo 1 For some reason User might use it for plotting.
                # # todo 2 This is somehow unoptimized. Loading data should return a list, also this done for every 
                # # todo 2 data point instead of reducing whole list as one. Try having np.array in dict (`dff`) isntead of lists
                ydata=list(dff[key][yaxis_data_name])
                if yaxis_data_name == "Total Energy":
                    print(key)
                    for i in range(len(ydata)):
                        ydata[i] -= dff[key][yaxis_data_name][0]
                fig.add_trace(go.Scatter(
                    x=list(dff[key][xaxis_data_name]),
                    y=ydata,
                    mode='lines', # todo this might be added to graph options (the one appears after plotting)
                    line=dict(width=5, color=px.colors.sample_colorscale(
                        colorscale, it/len(dff))[0]),
                    name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
                    )
                )
                xrange_max.append(max(dff[key][xaxis_data_name]))

            fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
                                         font=dict(size=22, family="Times New Roman")),
                              autosize=True,height=540,
                              template='simple_white',paper_bgcolor='#B4A0AA',plot_bgcolor='#B4A0AA',
                              margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, 
                              hovermode='closest',
                            #   hover_name=dff[key][yaxis_data_name],
                            #   hover_data=[dff[key][yaxis_data_name]]
                              )

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
            
            graph_id = 'graph--' + yaxis_type + '--' + yaxis_data_name.replace(' ', '-') + '--' + info[2].replace(' ', '-')

            graph = dcc.Graph(figure=fig, id = graph_id, className='graph-graph')

            if yaxis_data_name in groups["conservation"]:
                x_options = ['in time']
                y_options = ['linear','log']
            elif yaxis_data_name in groups["center of mass"]:
                x_options = ['in time']
                y_options = ['linear']
            elif (yaxis_data_name in groups["deformation"]) or (yaxis_data_name in groups["pairing"]):
                x_options = ['in time', 'in distance', 'as maps']
                y_options = ['linear', 'log']
            settings = GraphSettingsAIO(
                                data_type_props = {},
                                data_props = {},
                                x_axis_type_props = {'options':x_options},
                                y_axis_type_props = {'options':y_options},
                                is_picker = False,
                                aio_id = "settings"
                            )
            div_id = 'container--'+ yaxis_type + '--' + yaxis_data_name.replace(' ', '-') + '--' + info[2].replace(' ', '-')

            div = html.Div([
                graph,
                settings
            ], id = div_id)
            graphs_temp.append(div)
            #print(type(graph))
        
            return graphs_temp