#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:20:48 2020

@author: hendrasetiawan
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_daq as daq
from dash.dependencies import Input, Output
import dash_table
from plotly.subplots import make_subplots
import plotly.graph_objects as go




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Banking Industry Current State', children=[
            myList = ['Pilih Intitusi Pengawasan','Australian Securities and Investments Commission', 'Bank of India','BNR-National Bank of Rwanda','Bangko Sentral ng Pilipinas (BSP)','National Banking and Securities Commission (CNBV)','De Nederlandsche Bank (DNB)','Financial Conduct Authority (FCA)','Monetary Authority of Singapore (MAS)','Security Exchange Commision (SEC)','OeNB (Austria)']
            default_category = 'Pilih Intitusi Pengawasan'
            html.Div([
            
            html.Div([
            html.H3('Supervisory Technology Network'),
            html.Img(src=app.get_asset_url('suptechnetwork.png'), style={'height':'100%', 'width':'100%'})
            ],style={'width': '50%', 'display': 'inline-block','float': 'left'}),
            
            html.Div([
            html.H3('Regulatory Agency Utilization'),
            dcc.Dropdown(id='first-dropdown',
            options=[{'label':l, 'value':l} for l in myList],
            value = default_category
            ),
            html.Div(id='dd-output-container'),
            ],style={'width': '50%', 'display': 'inline-block','float': 'right'}),
            
            html.Div([
            html.H3('Related Country Banking Condition'),
            html.H5('Summary and Analysis After All Graph'),
            html.H6(''),
            ],style={'width': '100%', 'display': 'inline-block'}),
            
            html.Div([
            dcc.Graph(id='return')
            ],style={'width': '100%', 'display': 'inline-block'}),
            
            html.Div([
            dcc.Graph(id='x-time-series')
            ],style={'width': '65%', 'display': 'inline-block'}),
            
            html.Div([
            dcc.Graph(id='noninterestincome')
            ],style={'width': '35%', 'display': 'inline-block'}),
            
             html.Div([
            dcc.Graph(id='cost1')
            ],style={'width': '65%', 'display': 'inline-block'}),
            
            html.Div([
            dcc.Graph(id='cost2')
            ],style={'width': '35%', 'display': 'inline-block'}),
            
            
            
            
        ],style={'width': '100%', 'display': 'inline-block', 'float': 'right'})
            
        ]),
        dcc.Tab(label='Tab two', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Tab three', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
