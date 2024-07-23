from dash import Dash

# Project
import utils.ntg_data as ntg_data
import utils.ntg_layout as layout
import utils.ntg_graph as ntg_graph

#create app
app = Dash(__name__)

#create data frame
data, metadata = ntg_data.load_data()

#set app's layout
layout.sett(app, metadata)

#get graphs callbacks
ntg_data.pipe_data(metadata)
ntg_graph.get_callbacks(data)

if __name__ == '__main__':
    app.run_server(debug=True)
