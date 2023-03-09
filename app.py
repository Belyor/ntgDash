from dash import Dash

# Project
import utils.ntg_data as ntg_data
import utils.ntg_layout as layout
import utils.ntg_graph as ntg_graph

#create app
app = Dash(__name__)
#create data frame
df = ntg_data.load_data()
#set app's layout
layout.set(app)
#get graphs callbacks
ntg_graph.get_callbacks(app, df)

if __name__ == '__main__':
    app.run_server(debug=False)
