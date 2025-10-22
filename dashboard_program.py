import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Connect to database and get data
conn = sqlite3.connect('weather.db')
df = pd.read_sql_query("SELECT * FROM weather", conn)
conn.close()

# Start the app
app = dash.Dash(__name__)
server = app.server

# min and max temp for slider
min_temp = int(df['TempValues'].min())
max_temp = int(df['TempValues'].max())

# Make the layout
app.layout = html.Div([
    
    # Title at top
    html.Div([
        html.H1("Weather Dashboard"),
        html.P("Weather data from around the world")
    ], style={'padding': '20px', 'backgroundColor': '#2c3e50', 'color': 'white', 'textAlign': 'center'}),
    
    # Left side - filters
    html.Div([
        html.H3("Filters"),
        html.Br(),
        
        # Category dropdown
        html.Label("Pick category:"),
        dcc.Dropdown(
            id='category',
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
        
        # City search
        html.Label("Search city:"),
        dcc.Input(id='city', type='text', placeholder='Type city...'),
        html.Br(),
        html.Br(),
        
        # Temperature slider
        html.Label("Temperature range:"),
        dcc.RangeSlider(
            id='slider',
            min=min_temp,
            max=max_temp,
            value=[min_temp, max_temp],
            marks={min_temp: str(min_temp), max_temp: str(max_temp)}
        )
        
    ], style={'width': '25%', 'float': 'left', 'padding': '20px', 'backgroundColor': 'white'}),
    
    # Right side - charts
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
        
        # City list
        html.H3("City List"),
        html.Div(id='list')
        
    ], style={'width': '70%', 'float': 'right', 'padding': '20px'}),
    
    # Footer
    html.Div([
        html.P("Made by me")
    ], style={'clear': 'both', 'textAlign': 'center', 'padding': '20px'})
    
])

# Update everything when filters change
@app.callback(
    [Output('chart1', 'figure'),
     Output('chart2', 'figure'),
     Output('chart3', 'figure'),
     Output('list', 'children')],
    [Input('category', 'value'),
     Input('city', 'value'),
     Input('slider', 'value')]
)
def update_charts(category, city, slider):
    
    # Start with all data
    data = df.copy()
    
    # Filter by category
    if category != 'all':
        filtered = data[data['TempCategory'] == category]
        data = filtered
    
    # Filter by city
    if city:
        filtered = data[data['City'].str.contains(city, case=False)]
        data = filtered
    
    # Get slider values
    low = slider[0]
    high = slider[1]
    
    # Filter by temperature - low
    filtered = data[data['TempValues'] >= low]
    data = filtered
    
    # Filter by temperature - high
    filtered = data[data['TempValues'] <= high]
    data = filtered
    
    # Make chart 1 - bar chart
    top10 = data.nlargest(10, 'TempValues')
    chart1 = px.bar(top10, x='City', y='TempValues', title="Top 10 Hottest")
    
    # Make chart 2 - pie chart
    counts = data['TempCategory'].value_counts()
    chart2 = px.pie(values=counts.values, names=counts.index, title="Categories")
    
    # Make chart 3 - scatter
    chart3 = px.scatter(data, x='City', y='TempValues', color='TempCategory', title="Temperature by City")
    
    # Make city list
    list_items = []
    
    # Counter
    count = 0
    
    # Loop through cities
    for i in range(len(data)):
        # Check if less than 20
        if count < 20:
            # Get the row
            row = data.iloc[i]
            
            # Get city name
            name = row['City']
            
            # Get temperature
            temp = row['TemperatureText']
            
            # Get category
            cat = row['TempCategory']
            
            # Make one line
            line = html.Div([
                html.B(name),
                html.Span(" - " + temp + " - " + cat)
            ])
            
            # Add line to list
            list_items.append(line)
            
            # Increase counter
            count = count + 1
    
    # Check if more than 20 cities
    if len(data) > 20:
        # Calculate extra
        extra_cities = len(data) - 20
        
        # Make message
        more = html.P("... plus " + str(extra_cities) + " more")
        
        # Add message
        list_items.append(more)
    
    # Check if no cities
    if len(data) == 0:
        # Make no cities message
        list_items = [html.P("No cities found")]
    
    # Return everything
    return chart1, chart2, chart3, list_items

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)