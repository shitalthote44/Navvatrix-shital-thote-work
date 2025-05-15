import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Generate example sales data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-03-31')
regions = ['North', 'South', 'East', 'West']
products = ['WidgetA', 'WidgetB', 'WidgetC']

data = []
for date in dates:
    for region in regions:
        for product in products:
            sales = np.random.randint(1000, 5000)
            quantity = np.random.randint(1, 20)
            data.append({'Date': date, 'Region': region, 'Product': product, 'Sales': sales, 'Quantity': quantity})

df = pd.DataFrame(data)

# Color map for regions
region_colors = {
    'North': '#1f77b4',  # blue
    'South': '#ff7f0e',  # orange
    'East': '#2ca02c',   # green
    'West': '#d62728'    # red
}

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Sales Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Sales Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Label("Select Region(s):"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
                value=regions,
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block', 'paddingRight': '20px'}),

        html.Div([
            html.Label("Select Product(s):"),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': p, 'value': p} for p in sorted(df['Product'].unique())],
                value=products,
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block', 'paddingRight': '20px'}),

        html.Div([
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=df['Date'].min(),
                max_date_allowed=df['Date'].max(),
                start_date=df['Date'].min(),
                end_date=df['Date'].max()
            )
        ], style={'width': '35%', 'display': 'inline-block'}),
    ], style={'paddingBottom': '30px'}),

    # Bar chart for sales by Region
    dcc.Graph(id='bar-chart'),

    # Pie chart for sales distribution by Product
    dcc.Graph(id='pie-chart'),

    # Dropdown and line chart for sales trend over time by Product
    html.Div([
        html.Label("Select Product for Sales Trend:"),
        dcc.Dropdown(
            id='trend-product-dropdown',
            options=[{'label': p, 'value': p} for p in sorted(df['Product'].unique())],
            value='WidgetA',
            clearable=False
        ),
        dcc.Graph(id='line-chart')
    ], style={'paddingTop': '30px'})
], style={'padding': '20px'})


# Callback to update bar and pie charts based on filters
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('product-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_bar_pie(selected_regions, selected_products, start_date, end_date):
    # Filter dataframe based on selections
    filtered_df = df[
        (df['Region'].isin(selected_regions)) &
        (df['Product'].isin(selected_products)) &
        (df['Date'] >= start_date) &
        (df['Date'] <= end_date)
    ]

    # Bar chart: total sales by region with custom colors
    bar_data = filtered_df.groupby('Region', as_index=False)['Sales'].sum()
    bar_fig = px.bar(
        bar_data,
        x='Region',
        y='Sales',
        title='Total Sales by Region',
        labels={'Sales': 'Sales Amount'},
        color='Region',
        color_discrete_map=region_colors
    )

    # Pie chart: sales distribution by product
    pie_data = filtered_df.groupby('Product', as_index=False)['Sales'].sum()
    pie_fig = px.pie(
        pie_data,
        names='Product',
        values='Sales',
        title='Sales Distribution by Product'
    )

    return bar_fig, pie_fig


# Callback to update line chart based on selected product and date range
@app.callback(
    Output('line-chart', 'figure'),
    [Input('trend-product-dropdown', 'value'),
     Input('region-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_line_chart(selected_product, selected_regions, start_date, end_date):
    # Filter for selected product, regions and date range
    filtered_df = df[
        (df['Product'] == selected_product) &
        (df['Region'].isin(selected_regions)) &
        (df['Date'] >= start_date) &
        (df['Date'] <= end_date)
    ]

    # Aggregate sales by date
    trend_data = filtered_df.groupby('Date', as_index=False)['Sales'].sum()

    # Line chart: sales trend over time
    line_fig = px.line(
        trend_data,
        x='Date',
        y='Sales',
        title=f'Sales Trend Over Time: {selected_product}',
        labels={'Sales': 'Sales Amount', 'Date': 'Date'}
    )

    return line_fig


if __name__ == '__main__':
    app.run(debug=True)
