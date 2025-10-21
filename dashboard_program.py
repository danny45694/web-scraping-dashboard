import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Load data from database
conn = sqlite3.connect('weather.db')
df = pd.read_sql_query("SELECT * FROM weather", conn)
conn.close()

# min and max temp for slider
min_temp = int(df['temp values'].min())
max_temp = int(df['temp values'].max())

# Start Dash app
app = dash.Dash(__name__)
server = app.server

# Layout 
app.layout = html.Div([
    
    # Header
    html.Div([
        html.H1("Weather Dashboard"),
        html.P("Weather data from around the world")
    ], style={'padding': '20px', 'backgroundColor': '#2c3e50', 'color': 'white', 'textAlign': 'center'}),
    
    # Filters on the left side
    html.Div([
        html.H3("Filters"),
        html.Br(),
        
        # Category dropdown
        html.Label("Pick a category:"),
        dcc.Dropdown(
            id='my-category',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'Very Cold', 'value': 'very cold'},
                {'label': 'Cold', 'value': 'cold'},
                {'label': 'Comfortable', 'value': 'comfortable'},
                {'label': 'Hot', 'value': 'hot'},
                {'label': 'Very Hot', 'value': 'very hot'}
            ],
            value='all'
        ),
        html.Br(),
        
        # City search box
        html.Label("Search for a city:"),
        dcc.Input(id='my-city', type='text', placeholder='Type here...'),
        html.Br(),
        html.Br(),
        
        # Temperature slider
        html.Label("Temperature range:"),
        dcc.RangeSlider(
            id='my-slider',
            min=min_temp,
            max=max_temp,
            value=[min_temp, max_temp],
            marks={min_temp: str(min_temp), max_temp: str(max_temp)}
        )
        
    ], style={'width': '25%', 'float': 'left', 'padding': '20px', 'backgroundColor': 'white'}),
    
    # Charts on the right side
    html.Div([
        
        # Chart 1
        html.H3("Top 10 Hottest Cities"),
        dcc.Graph(id='chart1'),
        html.Br(),
        
        # Chart 2
        html.H3("Category Breakdown"),
        dcc.Graph(id='chart2'),
        html.Br(),
        
        # Chart 3
        html.H3("All Cities"),
        dcc.Graph(id='chart3'),
        html.Br(),
        
        # cities
        html.H3("City List"),
        html.Div(id='my-list', style={'padding': '10px', 'backgroundColor': 'white'})
        
    ], style={'width': '70%', 'float': 'right', 'padding': '20px'}),
    
    
])

# Function to update everything
@app.callback(
    [Output('chart1', 'figure'),
     Output('chart2', 'figure'),
     Output('chart3', 'figure'),
     Output('my-list', 'children')],
    [Input('my-category', 'value'),
     Input('my-city', 'value'),
     Input('my-slider', 'value')]
)
def update_everything(selected_category, search_text, slider_values):
    
    # Copy all the data
    data = df.copy()
    
    # Filter by category if selected
    if selected_category != 'all':
        data = data[data['temp category'] == selected_category]
    
    # Filter by city type
    if search_text:
        data = data[data['City'].str.contains(search_text, case=False)]
    
    # temperature slider
    low = slider_values[0]
    high = slider_values[1]
    data = data[data['temp values'] >= low]
    data = data[data['temp values'] <= high]
    
    # bar chart
    top10 = data.nlargest(10, 'temp values')
    chart1 = px.bar(top10, x='City', y='temp values', title="Hottest Cities")
    
    # pie chart
    counts = data['temp category'].value_counts()
    chart2 = px.pie(values=counts.values, names=counts.index, title="Categories")
    
    # scatter plot
    chart3 = px.scatter(data, x='City', y='temp values', color='temp category', title="All Cities")
    
    # Make the city list
    list_items = []
    for i in range(len(data)):
        if i < 20:  # only show first 20
            row = data.iloc[i]
            city_name = row['City']
            temp = row['Temperature']
            category = row['temp category']
            
            # Make one line for each city
            one_line = html.Div([
                html.B(city_name),
                html.Span(" - " + temp + " - " + category)
            ])
            list_items.append(one_line)
    
    # If there are more than 20 cities, say so
    if len(data) > 20:
        extra = html.P("... plus " + str(len(data) - 20) + " more cities")
        list_items.append(extra)
    
    # If no cities, show a message
    if len(data) == 0:
        list_items = [html.P("No cities found")]
    
    # Send everything back
    return chart1, chart2, chart3, list_items

# Start the app
if __name__ == '__main__':
    app.run_server(debug=True)