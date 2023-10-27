# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
data =  pd.read_csv('spacex_launch_dash.csv')
spacex_df = data
min_value = data['Payload Mass (kg)'].min()
max_value = data['Payload Mass (kg)'].max()

# Create a dash application
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1('SPACEX Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                dcc.Dropdown(id='site_dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                ],
                value='ALL',
                placeholder="ALL",
                searchable=True
                ), html.Div(dcc.Graph(id='success-pie-chart')),
               
                html.Br(),
                 dcc.RangeSlider(
                                    id='slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks = {
                                            0: '0 kg',
                                            1000: '1000 kg',
                                            2000: '2000 kg',
                                            3000: '3000 kg',
                                            4000: '4000 kg',
                                            5000: '5000 kg',
                                            6000: '6000 kg',
                                            7000: '7000 kg',
                                            8000: '8000 kg',
                                            9000: '9000 kg',
                                            10000: '10000 kg'
                                    },

                                    value=[min_value,max_value]
                                ),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),


])

@app.callback(
     Output(component_id='success-pie-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value')])
def get_pie_chart(entered_site):
    print(entered_site)
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data_frame= data.groupby('Launch Site').mean().reset_index(), values='class', names='Launch Site'
        , title= "Overall Success"
        )

        return fig
    else:  
        data2= data[data['Launch Site'] == entered_site ]
        d2 = pd.DataFrame(data2['class'].value_counts()/data2.shape[0],columns=['class'])
        d2 = d2.reset_index()
        d2.columns = ['Success','percentage']
        fig = px.pie(data_frame= d2, values='percentage', names='Success',labels=['Success','Failure'],title= "Success for " + entered_site )
        return fig

@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value'),Input(component_id='slider',component_property='value')])

def update_scattergraph(site_dropdown,slider):
    
    if site_dropdown == 'All Sites':
        print("ALL:")
        print(site_dropdown,slider)
        low, high = slider
        df  = spacex_df
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
           
            hover_data=['Payload Mass (kg)'])
        return fig
    else:
        low, high = slider
        print("Not ALL:")
        print(site_dropdown,slider)
        df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
            
            hover_data=['Payload Mass (kg)'])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()