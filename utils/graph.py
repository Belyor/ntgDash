from dash import Dash, dcc, html, ctx, Input, Output, State
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
import math
import os

#Types of available data
symbols = {
    #Conservation
    "Total Energy": "total_E",
    "Number of Protons": "N_p",
    "Number of Neutrons": "N_n",
    #Center of mass
    "X_cm": "x_rcm",
    "Y_cm": "y_rcm",
    "Z_cm": "z_rcm",
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
    "Pairing gap for Protons": "delta_grad_p",
    "Pairing gap for  Neutrons": "delta_grad_n",
    #x axis
    "in time": "(t)",
    "in distance": "(dist)",
    "as maps": "map",
    #y axis
    "linear": "lin",
    "log": "log"
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
        label = symbols[y_type] + " " + symbols[data] + " " + symbols[x_type]
        option = {'label': label, 'value': value}
        options.append(option)
        values.append(value)
        return options, values


def get_callbacks(app: Dash, df: pd.DataFrame, colorscales: list[str]):
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
        State(component_id='conservation-xaxis-type', component_property='value'),
        #conservation y-axis
        State(component_id='conservation-yaxis-type', component_property='value'),
        #conservation data
        State(component_id='conservation-data', component_property='value'),
        #center of mass x-axis
        State(component_id='center-of-mass-xaxis-type', component_property='value'),
        #center of mass y-axis
        State(component_id='center-of-mass-yaxis-type', component_property='value'),
        #center of mass data
        State(component_id='center-of-mass-data', component_property='value'),
        #deformation x-axis
        State(component_id='deformation-xaxis-type', component_property='value'),
        #deformation y-axis
        State(component_id='deformation-yaxis-type', component_property='value'),
        #deformation data
        State(component_id='deformation-data', component_property='value'),
        #pairing x-axis
        State(component_id='pairing-xaxis-type', component_property='value'),
        #pairing y-axis
        State(component_id='pairing-yaxis-type', component_property='value'),
        #pairing data
        State(component_id='pairing-data', component_property='value')
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
        #Input(component_id='graphs', component_property='children')
    )
    def update_graphs(values#, graphs):
    ):
        graphs = []
#        graphs_temp = graphs
#        #when no graph was added to the list
#        if len(graphs_temp) == len(values):
#            return graphs_temp
#        #when a graph was deleted from the list
#        elif len(graphs_temp) > len(values):
#            #if list of graphs is empty
#            if len(values) == 0:
#                graphs_temp.clear()
#            #if one graph was deleted from the list
#            else:
#                to_remove = None
#                for graph in graphs_temp:
#                    #print(graph.keys())
#                    id = graph.id
#                    id.replace('graph--','')
#                    id.replace('--','|')
#                    id.replace('-',' ')
#
#                    delete = True
#
#                    for value in values:
#                        if id == value:
#                            delete = False
#                            break
#                    
#                    if delete == True:
#                        to_remove = graph
#                        break
#                
#                graphs_temp.remove(to_remove)
#            
#            return graphs_temp
#        elif len(graphs_temp) < len(values):
#            value = values[-1] #last added value
#            info = value.split('|')
#            yaxis_type = info[0] #[linear/log]
#            xaxis_type = 'linear'
#            yaxis_data_name = info[1]
#            #[in time/in distance/as maps]
#            if info[2] == 'in time':
#                xaxis_data_name = 'Time'
#            elif info[2] == 'in distance':
#                xaxis_data_name = 'distance'
#            elif info[2] == 'as maps':
#                xaxis_data_name = 'maps'
#            
#            colorscale = colorscales[0]
#
#            dff=df
#            xrange_min=-50 if xaxis_data_name == 'Time' else -1
#            xrange_max=[]
#            fig=go.Figure()
#            for key, it in zip(dff, range(len(dff))):
#                dataname=key.split(".")[0].split(os.sep)[1].split("_")
#                ydata=list(dff[key][yaxis_data_name])
#                if yaxis_data_name == "Total Energy":
#                    for i in range(len(ydata)):
#                        ydata[i] -= dff[key][yaxis_data_name][0]
#                fig.add_trace(go.Scatter(
#                    x=list(dff[key][xaxis_data_name]),
#                    y=ydata,
#                    mode='lines',
#                    line=dict(width=5, color=px.colors.sample_colorscale(
#                        colorscale, it/len(dff))[0]),
#                    name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
#                    # hover_name=dff[key][yaxis_data_name]
#                    )
#                )
#                xrange_max.append(max(dff[key][xaxis_data_name]))
#
#            fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
#                                         font=dict(size=22, family="Times New Roman")),
#                              autosize=True,height=540,
#                              template='simple_white',paper_bgcolor='#B4A0AA',plot_bgcolor='#B4A0AA',
#                              margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, hovermode='closest')
#
#            fig.update_xaxes(title=dict(text=xaxis_data_name,
#                                        font=dict(size=20, family="Times New Roman")),
#                             range=[xrange_min, max(xrange_max)],
#                             type=xaxis_type, linewidth=4, mirror=True, side='bottom',
#                             ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
#                             minor=dict(ticklen=10, tickwidth=2))
#
#            fig.update_yaxes(title=dict(text=yaxis_data_name,
#                                        font=dict(size=20, family="Times New Roman")),
#                             type=yaxis_type, linewidth=4, mirror=True, side='left',
#                             ticklen=15, tickwidth=3, tickfont=dict(size=18, family="Times New Roman"),
#                             minor=dict(ticklen=10, tickwidth=2))
#            
#            graph_id = 'graph--' + yaxis_type + '--' + yaxis_data_name.replace(' ', '-') + '--' + info[2].replace(' ', '-')
#
#            graph = dcc.Graph(figure=fig, id = graph_id, className='graph-graph')
#
#            graphs_temp.append(graph)
#            print(type(graph))
#        
#            return graphs_temp

        for value in values:
            info = value.split('|')
            yaxis_type = info[0] #[linear/log]
            xaxis_type = 'linear'
            yaxis_data_name = info[1]
            #[in time/in distance/as maps]
            if info[2] == 'in time':
                xaxis_data_name = 'Time'
            elif info[2] == 'in distance':
                xaxis_data_name = 'distance'
            elif info[2] == 'as maps':
                xaxis_data_name = 'maps'
            
            colorscale = colorscales[0]

            dff=df
            xrange_min=-50 if xaxis_data_name == 'Time' else -1
            xrange_max=[]
            fig=go.Figure()
            for key, it in zip(dff, range(len(dff))):
                dataname=key.split(".")[0].split(os.sep)[1].split("_")
                ydata=list(dff[key][yaxis_data_name])
                if yaxis_data_name == "Total Energy":
                    for i in range(len(ydata)):
                        ydata[i] -= dff[key][yaxis_data_name][0]
                fig.add_trace(go.Scatter(
                    x=list(dff[key][xaxis_data_name]),
                    y=ydata,
                    mode='lines',
                    line=dict(width=5, color=px.colors.sample_colorscale(
                        colorscale, it/len(dff))[0]),
                    name=f"{dataname[0]:12} {dataname[4].replace('-','.'):5} {dataname[5].replace('-','/'):10} {dataname[6]:6}",
                    # hover_name=dff[key][yaxis_data_name]
                    )
                )
                xrange_max.append(max(dff[key][xaxis_data_name]))

            fig.update_layout(title=dict(text=yaxis_data_name+" ("+xaxis_data_name+")",
                                         font=dict(size=22, family="Times New Roman")),
                              autosize=True,height=540,
                              template='simple_white',paper_bgcolor='#B4A0AA',plot_bgcolor='#B4A0AA',
                              margin={'l': 0, 'b': 0, 't': 32, 'r': 0}, hovermode='closest')

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

            graphs.append(graph)
        
        return graphs