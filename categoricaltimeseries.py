#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 11:37:54 2021

@author: hendrasetiawan
"""


import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_daq as daq
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df1 = pd.read_csv('australia.csv')
df1['Country']='australia'

df2 = pd.read_csv('india.csv')
df2['Country']='india'

df3 = pd.read_csv('Malaysia.csv')
df3['Country']='Malaysia'



frames = [df1, df2, df3]
result = pd.concat(frames)

# Plotly figure 1
fig = px.line(result, x='Year', y='Bank return on equity (%, after tax)',
              color="Country",
              line_group="Country", hover_name="Country")
fig.update_layout(title='Productivity, Europe' , showlegend=True)



"""

# Data
gapminder = px.data.gapminder()

# Most productive european countries (as of 2007)
df_eur = gapminder[gapminder['continent']=='Europe']
df_eur_2007 = df_eur[df_eur['year']==2007]
eur_gdp_top5=df_eur_2007.nlargest(5, 'gdpPercap')['country'].tolist()
df_eur_gdp_top5 = df_eur[df_eur['country'].isin(eur_gdp_top5)]

# Most productive countries on the american continent (as of 2007)
df_ame = gapminder[gapminder['continent']=='Americas']
df_ame_2007 = df_ame[df_ame['year']==2007]
df_ame_top5=df_ame_2007.nlargest(5, 'gdpPercap')['country'].tolist()
df_ame_gdp_top5 = df_ame[df_ame['country'].isin(df_ame_top5)]

# Plotly figure 1
fig = px.line(df_eur_gdp_top5, x='year', y='gdpPercap',
              color="country",
              line_group="country", hover_name="country")
fig.update_layout(title='Productivity, Europe' , showlegend=False)


# Plotly figure 2
fig2 = go.Figure(fig.add_traces(
                 data=px.line(df_ame_gdp_top5, x='year', y='gdpPercap',
                              color="country",
                              line_group="country", line_dash='country', hover_name="country")._data))
fig2.update_layout(title='Productivity, Europe and America', showlegend=False)

#fig.show()
"""


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(figure=fig)])

if __name__ == '__main__':
    app.run_server(debug=True)