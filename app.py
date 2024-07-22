from dash import Dash
# from pydoc import classname
# from dash import Dash, dcc, html, Input, Output
# import plotly.express as px
# import pandas as pd
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import numpy as np
# import math
# import os

# Project
import utils.ntg_data as ntg_data
import utils.ntg_layout as layout
import utils.ntg_graph as ntg_graph

#create app
app = Dash(__name__)

#create data frame
df, metadata = ntg_data.load_data()

#set app's layout
layout.sett(app, metadata)

#get graphs callbacks
ntg_data.pipe_data(metadata)
ntg_graph.get_callbacks(df)

if __name__ == '__main__':
    app.run_server(debug=True)
