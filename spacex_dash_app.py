# Import required libraries
import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Create a dash application
app = dash.Dash(__name__)

#Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 30}),
	# TASK 1: Add a Launch Site Drop-down Input Component
	# default select value is ALL
    	dcc.Dropdown(id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            ],
            value='ALL',
            placeholder="State",
            searchable=True
            ),

html.Br(),

# Task 2: Add a pie chart
# For selected launch site, specify success vs. failed counts for site
html.Div(dcc.Graph(id='success-pie-chart')),
html.Br(),

html.P("Payload range (Kg):"),
# Task 3: Add range slider to select payload
dcc.RangeSlider(id='payload-slider',
		min=0, max=10000, step=1000,
		marks={0: '0', 100: '100'},
		value=[min_payload, max_payload]),

# Task 4: Add scatter chart
html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2:
# Add a callback function with 'site-dropdown' as input, 'success-pie-chart' as output
# Function decorator to specify input and output
@app.callback(Output(component_id='success-pie-chart',
 component_property='figure'),
    Input(component_id='site-dropdown',
 component_property='value'),
             )
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(spacex_df,
            values='class',
        	names='Launch Site',
        	title='Success Count for All Launch Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        filtered_df = filtered_df.groupby('class').count().reset_index()
        fig = px.pie(filtered_df,
            values='Unidentified: 0',
        	names='class',
     		title='Total Success Launches for Site {}'.format(entered_site))
        return fig
        # return the outcomes piechart for a selected site

# Task 4:
# Add callback function for 'site-dropdown' and 'payload-slider' as inputs, 'success-payload-scatter-chart' as output
@app.callback(Output(component_id='success-payload-scatter-chart',
 component_property='figure'), [Input(component_id='site-dropdown',
 component_property='value'),
            Input(component_id="payload-slider",
 component_property='value')],
             )

def scatter(entered_site, payload_range):
    print('Params: {} {}'.format(entered_site, payload_range))
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= int(payload_range[0])) &
                                 spacex_df['Payload Mass (kg)'] <= int(payload_range[1]))
                                ] 
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category',
                        title="For All Sites: payload mass between {:8,d}kg and {:8,d}kg".format(int(payload_range[0]), int(payload_range[1])))
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                                (spacex_df['Payload Mass (kg)'] >= int(payload_range[0])) &
                                (spacex_df['Payload Mass (kg)'] <= int(payload_range[1]))
                               ]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category',
                        title="Success Count on Payload Mass between {:8,d}kg and {:8,d}kg for Site: {entered_site}".format(entered_site, int(payload_range[0],int(payload_range[1]))))
        return fig

if __name__ == '__main__':
    app.run_server()
