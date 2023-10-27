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
fig = px.pie(data_frame= data.groupby('Launch Site').mean().reset_index(), title = "Overall pie chart", values='class', names='Launch Site')
      
# Create a dash application
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1('Airline Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
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
                ),
                html.Div(dcc.Graph(id='success-pie-chart')),
                html.Br()
])
@app.callback([Output(component_id='success-pie-chart', component_property='figure')],
              Input(component_id='site_dropdown', component_property='value'))

def get_pie_chart(site_dropdown):
    entered_site = site_dropdown
    filtered_df = data
    if entered_site == 'ALL':
        fig = px.pie(data_frame= data.groupby('Launch Site').mean().reset_index(), title = "Overall pie chart", values='class', names='Launch Site')
        return [dcc.Graph(figure=fig)]
    else:
        if(entered_site =='CCAFS LC-40'):
            data2= data[data['Launch Site'] == 'CCAFS LC-40' ]
            d2 = pd.DataFrame(data2['class'].value_counts()/data2.shape[0],columns=['class'])
            d2 = d2.reset_index()
            d2.columns = ['Success','percentage']
            fig = px.pie(data_frame= d2, values='percentage', names='Success',labels=['Success','Failure'])
            return [dcc.Graph(figure=fig)]

        elif(entered_site =='VAFB SLC-4E'):
            data2= data[data['Launch Site'] == 'VAFB SLC-4E' ]
            d2 = pd.DataFrame(data2['class'].value_counts()/data2.shape[0],columns=['class'])
            d2 = d2.reset_index()
            d2.columns = ['Success','percentage']
            fig = px.pie(data_frame= d2, values='percentage', names='Success',labels=['Success','Failure'])
            return [dcc.Graph(figure=fig)]

        elif(entered_site == 'KSC LC-39A'):
            data2= data[data['Launch Site'] == 'KSC LC-39A' ]
            d2 = pd.DataFrame(data2['class'].value_counts()/data2.shape[0],columns=['class'])
            d2 = d2.reset_index()
            d2.columns = ['Success','percentage']
            fig = px.pie(data_frame= d2, values='percentage', names='Success',labels=['Success','Failure'])
            return [dcc.Graph(figure=fig)]
        elif(entered_site == 'CCAFS SLC-40'):
            data2= data[data['Launch Site'] == 'CCAFS SLC-40' ]
            d2 = pd.DataFrame(data2['class'].value_counts()/data2.shape[0],columns=['class'])
            d2 = d2.reset_index()
            d2.columns = ['Success','percentage']
            fig = px.pie(data_frame= d2, values='percentage', names='Success',labels=['Success','Failure'])
            return [dcc.Graph(figure=fig)]

            


# Run the app
if __name__ == '__main__':
    app.run_server()