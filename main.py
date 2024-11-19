import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Local Data Dashboard"

# Global variable to cache data
data_cache = {}

# Layout
app.layout = html.Div([
    html.H1("Local Data Dashboard", style={'textAlign': 'center'}),

    # File upload to load data
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV Files', style={'fontSize': 16}),
        multiple=True
    ),

    html.Div(id='upload-status', style={'color': 'green', 'fontSize': 14}),

    # Dropdown to select cached data
    dcc.Dropdown(id='select-dataset', placeholder="Select Dataset", style={'width': '50%'}),

    # Graph
    dcc.Graph(id='data-visualization'),

    # Debug output
    html.Div(id='debug-output', style={'whiteSpace': 'pre-wrap'})
])


# Callback to handle file upload
@app.callback(
    [Output('upload-status', 'children'),
     Output('select-dataset', 'options')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def upload_files(contents, filenames):
    if contents is None:
        return "", []

    for content, filename in zip(contents, filenames):
        # Simulate loading and caching the data
        data_cache[filename] = pd.read_csv(filename)

    return f"Uploaded {len(filenames)} files successfully!", [{'label': f, 'value': f} for f in filenames]


# Callback to update graph based on selected dataset
@app.callback(
    Output('data-visualization', 'figure'),
    [Input('select-dataset', 'value')]
)
def update_graph(selected_dataset):
    if selected_dataset is None:
        return {}

    df = data_cache[selected_dataset]
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title=f"Visualization for {selected_dataset}")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

