import os
import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Lazy Loading Dashboard"

# Global variable to store folder structure and cached data
folder_structure = {}
data_cache = {}


def parse_folder_structure(base_path):
    """
    Parse folder structure without loading data.
    """
    global folder_structure
    folder_structure = {}  # Reset folder structure

    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)
        if os.path.isdir(year_path):
            folder_structure[year_folder] = {}
            for month_folder in os.listdir(year_path):
                month_path = os.path.join(year_path, month_folder)
                if os.path.isdir(month_path):
                    folder_structure[year_folder][month_folder] = [
                        file.split('-')[0] for file in os.listdir(month_path) if file.endswith('.csv')
                    ]


def load_selected_data(year, month, csv_type, base_path):
    """
    Load the selected data on-demand.
    """
    global data_cache
    if year in data_cache and month in data_cache[year] and csv_type in data_cache[year][month]:
        return data_cache[year][month][csv_type]  # Return cached data if available

    # Construct file path and load the CSV
    year_folder = f"{year}"
    month_folder = f"{month}"
    file_name = f"{csv_type}-{month_folder}.csv"
    file_path = os.path.join(base_path, year_folder, month_folder, file_name)

    try:
        df = pd.read_csv(file_path)
        # Cache the loaded data
        if year not in data_cache:
            data_cache[year] = {}
        if month not in data_cache[year]:
            data_cache[year][month] = {}
        data_cache[year][month][csv_type] = df
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return pd.DataFrame()


# Layout
app.layout = html.Div([
    html.H1("Lazy Loading Data Dashboard", style={'textAlign': 'center'}),

    # Folder path input
    html.Div([
        dcc.Input(
            id='folder-path',
            type='text',
            placeholder='Enter folder path...',
            style={'width': '80%'}
        ),
        html.Button('Load Folder', id='load-folder', style={'fontSize': 16}),
    ], style={'textAlign': 'center', 'padding': '10px'}),

    html.Div(id='folder-status', style={'color': 'green', 'fontSize': 14}),

    # Dropdowns for selecting Year, Month, and CSV Type
    html.Div([
        dcc.Dropdown(id='select-year', placeholder="Select Year", style={'width': '30%', 'display': 'inline-block'}),
        dcc.Dropdown(id='select-month', placeholder="Select Month", style={'width': '30%', 'display': 'inline-block'}),
        dcc.Dropdown(id='select-csv', placeholder="Select CSV Type", style={'width': '30%', 'display': 'inline-block'}),
    ], style={'textAlign': 'center', 'padding': '10px'}),

    # Graph for visualizing data
    dcc.Graph(id='data-visualization'),

    # Debug output
    html.Div(id='debug-output', style={'whiteSpace': 'pre-wrap', 'padding': '10px'})
])


# Callback to parse folder structure
@app.callback(
    [Output('folder-status', 'children'),
     Output('select-year', 'options')],
    [Input('load-folder', 'n_clicks')],
    [State('folder-path', 'value')]
)
def load_folder(n_clicks, folder_path):
    if n_clicks is None or not folder_path:
        return "", []

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return "Invalid folder path. Please try again.", []

    # Parse folder structure
    parse_folder_structure(folder_path)

    # Populate year dropdown
    years = list(folder_structure.keys())
    return f"Loaded folder structure: {folder_path}", [{'label': year, 'value': year} for year in years]


# Callback to update month dropdown based on selected year
@app.callback(
    Output('select-month', 'options'),
    [Input('select-year', 'value')]
)
def update_month_dropdown(selected_year):
    if not selected_year or selected_year not in folder_structure:
        return []
    months = list(folder_structure[selected_year].keys())
    return [{'label': month, 'value': month} for month in months]


# Callback to update CSV dropdown based on selected month
@app.callback(
    Output('select-csv', 'options'),
    [Input('select-year', 'value'),
     Input('select-month', 'value')]
)
def update_csv_dropdown(selected_year, selected_month):
    if not selected_year or not selected_month or selected_year not in folder_structure:
        return []
    if selected_month not in folder_structure[selected_year]:
        return []
    csv_types = folder_structure[selected_year][selected_month]
    return [{'label': csv_type, 'value': csv_type} for csv_type in csv_types]


# Callback to update graph based on selected CSV
@app.callback(
    Output('data-visualization', 'figure'),
    [Input('select-year', 'value'),
     Input('select-month', 'value'),
     Input('select-csv', 'value'),
     State('folder-path', 'value')]
)
def update_graph(selected_year, selected_month, selected_csv, folder_path):
    if not selected_year or not selected_month or not selected_csv:
        return {}

    # Load the selected data on-demand
    df = load_selected_data(selected_year, selected_month, selected_csv, folder_path)
    if df.empty:
        return {}

    # Create a simple plot (customize as needed)
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title=f"{selected_year} {selected_month} {selected_csv}")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
