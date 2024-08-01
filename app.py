from dash import Dash, Output, Input, State, dcc, html, callback

# Project
import utils.ntg_data as ntg_data
import utils.ntg_layout as ntg_layout
import utils.ntg_graph as ntg_graph

from utils.querystring_methods import encode_state
from utils.querystring_methods import parse_state

#create app
app = Dash(__name__)
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-layout')
])

#create data frame
data, metadata = ntg_data.load_data()

component_ids = [
    ('filter_set', 'value'),
    ('filter_system', 'value'),
    ('filter_functional', 'value'),
    ('filter_ecms', 'value'),
    ('filter_phase', 'value'),
    ('filter_b', 'value'),
    ('list-of-graphs', 'options'),
    ('list-of-graphs', 'value'),
]
component_ids_zipped= list(zip(*component_ids))

@callback(
    Output('page-layout', 'children'),
    Input('url', 'href'),
)
def page_load(href):
    """
    Upon page load, take the url, parse the querystring, and use the
    resulting state dictionary to build up the layout.
    """
    if not href:
        return []
    state = parse_state(href)
    return ntg_layout.create_layout(metadata, state)

@callback(
    Output('url', 'search'),
    Input('URL-copy', 'n_clicks'),
    State('filter_set', 'value'),
    State('filter_system', 'value'),
    State('filter_functional', 'value'),
    State('filter_ecms', 'value'),
    State('filter_phase', 'value'),
    State('filter_b', 'value'),
    State('list-of-graphs', 'options'),
    State('list-of-graphs', 'value'),
    prevent_initial_call = True, # Leaves the URL clean for the first application run
)
def update_url_state(_, fset, fsys, ffunc, fecms, fphase, fb, list_graphs_opt, list_graphs_val):
    """
    When any of the (id, param) values changes, this callback gets triggered.

    Passes the list of component id's, the list of component parameters
    (zipped together in component_ids_zipped), and the value to encode_state()
    and return a properly formed querystring.
    """
    values = (fset, fsys, ffunc, fecms, fphase, fb, list_graphs_opt, list_graphs_val)
    return encode_state(component_ids_zipped, values)

@callback(
    Output('clipboard', 'content'),
    Output('clipboard', 'n_clicks'),
    Input('URL-copy', 'n_clicks'),
    State('url', 'href'),
    State('clipboard', 'n_clicks'),
    prevent_initial_call = True,
)
def custom_copy(_, url, clpbrd_clicks):
    return url, clpbrd_clicks+1

ntg_graph.get_callbacks(data)

if __name__ == '__main__':
    app.run(debug=True)
