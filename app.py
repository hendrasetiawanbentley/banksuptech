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
import os
import tweepy as tw
import pandas as pd
from searchtweets import ResultStream, gen_rule_payload, load_credentials
from searchtweets import collect_results
import numpy as np
import re
import textblob
from textblob import TextBlob
from googletrans import Translator
import nltk
import dash_auth
from users import USERNAME_PASSWORD_PAIRS

nltk.download('wordnet')
nltk.download('punkt')



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    USERNAME_PASSWORD_PAIRS
)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True
myList = ['Pilih Intitusi Pengawasan','Australian Securities and Investments Commission', 'Bank of India','BNR-National Bank of Rwanda','Bangko Sentral ng Pilipinas (BSP)','National Banking and Securities Commission (CNBV)','De Nederlandsche Bank (DNB)','Financial Conduct Authority (FCA)','Monetary Authority of Singapore (MAS)','Security Exchange Commision (SEC)','OeNB (Austria)']
default_category = 'Pilih Intitusi Pengawasan'

data_url = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'
df = pd.read_csv(data_url)

tempo=pd.read_csv('new_tempodotco_tweets.csv')
tempo['signal']=tempo.text.str.contains('OJK')
tempoclean=tempo.loc[tempo.signal==True,:]
df = tempoclean

def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())#The long string of what seems like nonsense essentially takes away any characters that aren’t normal english words/letters.
tempoclean["cleantweet"] = tempoclean['text'].apply(lambda x: clean_tweet(x))


#for NLP
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity ==0:
        return 'Neutral'
    else:
        return 'Negative'
    
tempoclean["Sentiment"] = tempoclean['cleantweet'].apply(lambda x: analyze_sentiment(x))


app.layout = html.Div([
     html.Div([html.H1('Financial Services Supervisory Technology', style={'textAlign': 'center','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'})]),
    dcc.Tabs([
       
        dcc.Tab(label='Banking Industry Current State', children=[
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
            html.H5('Summary, Analysis and Math Modelling Per Country After All Graph'),
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
        dcc.Tab(label='OJK Sentiment Analysis', children=[
           #disini untuk mengisikan
            html.Div([
            html.H3('Pemantauan Twitter Major Media'),
            #contoh major media
            html.H5('Tempo Indonesia'),
            html.H6('Tweet Tempo dan Link Berita Tentang OJK'),
            html.H6('Tabel dan Sentimen Analysis'),
            dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} 
                 for i in df.columns],
               data=df.to_dict('records'),
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender")
            ),
              
                 
            html.H3('Key Person Indonesia'),
            #contoh major media
            html.H5('Menteri Keuangan'),
            html.H6('Tweet Menteri Keuangan dan Terkait OJK'),
            html.H6('Tabel dan Sentimen Analysis'),
                 
            html.H3('Google Search Result'),
            #contoh major media
            html.H5('Google Sentiment Analysis'),
            html.H6('Tabel dan Sentimen Analysis'),
                 
            html.H3('Pemantauan Fokus OJK'),
            #contoh major media
            html.H5('UMKM, Digitalisasi, dan, Ekonomi Hijau'),
            html.H6('Tabel dan Sentimen Analysis'),
                 
            html.Img(src=app.get_asset_url('suptechnetwork.png'), style={'height':'100%', 'width':'100%'})
            ],style={'width': '50%', 'display': 'inline-block','float': 'left'}),
             
        
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

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('first-dropdown', 'value')])

def update_output(value):
   df = pd.read_csv('empty.csv')
   fig = make_subplots(specs=[[{"secondary_y": True}]]) 
        # Add traces
   fig.add_trace(
       go.Scatter(x=df.Year,y=df['Bank net interest margin (%)'], name="Bank Net Interest Margin"),
       )
   fig.add_trace(
       go.Scatter(x=df.Year, y=df['Bank return on assets (%, after tax)'],name="Bank return on assets (%) after tax")
       )
        # Add figure title
   fig.update_layout(
       title_text="Bank Net Interest Margin (%) and Bank Return on Asset (after tax) (%) Relationship "
       )
    # Set x-axis title
   fig.update_xaxes(title_text="Year")
    # Set y-axes titles
   fig.update_yaxes(
       title_text="<b>Percentage (%)</b>", 
       secondary_y=False)
   fig.update_yaxes(
       title_text="<b>secondary</b> yaxis title", 
       secondary_y=True)
   if value=='Australian Securities and Investments Commission': 
        df = pd.read_csv('australia.csv')
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add traces
        fig.add_trace(
            go.Scatter(x=df.Year,y=df['Bank net interest margin (%)'], name="Bank Net Interest Margin"),
            )
        fig.add_trace(
            go.Scatter(x=df.Year, y=df['Bank return on assets (%, after tax)'],name="Bank return on assets (%) after tax")
            
            )
        
        # Add figure title
        fig.update_layout(
            title_text="Bank Net Interest Margin (%) and Bank Return on Asset (after tax) (%) Relationship "
            )

    # Set x-axis title
        fig.update_xaxes(title_text="Year")

    # Set y-axes titles
        fig.update_yaxes(
                title_text="<b>Percentage (%)</b>", 
                secondary_y=False)
        fig.update_yaxes(
                title_text="<b>secondary</b> yaxis title", 
                secondary_y=True)
        return fig
   if value=='Bank of India': 
        df = pd.read_csv('India.csv')
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces
        fig.add_trace(
            go.Scatter(x=df.Year,y=df['Bank net interest margin (%)'], name="Bank Net Interest Margin"),
            )
        fig.add_trace(
            go.Scatter(x=df.Year, y=df['Bank return on assets (%, after tax)'],name="Bank return on assets (%) after tax")
            
            )
        
        # Add figure title
        fig.update_layout(
            title_text="Bank Net Interest Margin (%) and Bank Return on Asset (after tax) (%) Relationship "
            )

    # Set x-axis title
        fig.update_xaxes(title_text="Year")

    # Set y-axes titles
        fig.update_yaxes(
                title_text="<b>Percentage (%)</b>", 
                secondary_y=False)
        fig.update_yaxes(
                title_text="<b>secondary</b> yaxis title", 
                secondary_y=True) 
          
        return fig
    
   
  
   return fig

@app.callback(
    dash.dependencies.Output('noninterestincome', 'figure'),
    [dash.dependencies.Input('first-dropdown', 'value')])

def update_output(value):
   df = pd.read_csv('empty.csv')
   
   fig2 = px.scatter(df, x='Year', y='Bank noninterest income to total income (%)')
   fig2.update_traces(mode='lines+markers')
   fig2.update_xaxes(showgrid=False)
   fig2.update_layout(
       title_text="Bank Non Interest Income (%)"
       )
   if value=='Australian Securities and Investments Commission': 
        df = pd.read_csv('australia.csv')
        fig2 = px.scatter(df, x='Year', y='Bank noninterest income to total income (%)')
        fig2.update_traces(mode='lines+markers')
        fig2.update_xaxes(showgrid=False)
        fig2.update_layout(
          title_text="Bank Non Interest Income (%)"
          )
        return fig2
   if value=='Bank of India':
        df = pd.read_csv('India.csv')
        fig2 = px.scatter(df, x='Year', y='Bank noninterest income to total income (%)')
        fig2.update_traces(mode='lines+markers')
        fig2.update_xaxes(showgrid=False)
        fig2.update_layout(
          title_text="Bank Non Interest Income (%)"
          )
        return fig2
   return fig2

@app.callback(
    dash.dependencies.Output('cost1', 'figure'),
    [dash.dependencies.Input('first-dropdown', 'value')])

def update_output(value):
   df = pd.read_csv('empty.csv')
   
   #figure3-cost structure
   fig3 = px.scatter(df, x='Year', y='Bank overhead costs to total assets (%)')
   fig3.update_traces(mode='lines+markers')
   fig3.update_xaxes(showgrid=False)
     
   if value=='Australian Securities and Investments Commission':
        df = pd.read_csv('australia.csv')
        fig3 = px.scatter(df, x='Year', y='Bank overhead costs to total assets (%)')
        fig3.update_traces(mode='lines+markers')
        fig3.update_xaxes(showgrid=False)
        return fig3
   if value=='Bank of India':
        df = pd.read_csv('India.csv')
        fig3 = px.scatter(df, x='Year', y='Bank overhead costs to total assets (%)')
        fig3.update_traces(mode='lines+markers')
        fig3.update_xaxes(showgrid=False)
        return fig3
   return fig3

@app.callback(
    dash.dependencies.Output('cost2', 'figure'),
    [dash.dependencies.Input('first-dropdown', 'value')])

def update_output(value):
   df = pd.read_csv('empty.csv')
   
    #figure4-cost structure2
   fig4 = px.scatter(df, x='Year', y='Bank cost to income ratio (%)')
   fig4.update_traces(mode='lines+markers')
   fig4.update_xaxes(showgrid=False)
     
   if value=='Australian Securities and Investments Commission':
        df = pd.read_csv('australia.csv')
        fig4 = px.scatter(df, x='Year', y='Bank cost to income ratio (%)')
        fig4.update_traces(mode='lines+markers')
        fig4.update_xaxes(showgrid=False)
        return fig4
   if value=='Bank of India':
        df = pd.read_csv('India.csv')
        fig4 = px.scatter(df, x='Year', y='Bank cost to income ratio (%)')
        fig4.update_traces(mode='lines+markers')
        fig4.update_xaxes(showgrid=False)
        return fig4
   return fig4

@app.callback(
    dash.dependencies.Output('return', 'figure'),
    [dash.dependencies.Input('first-dropdown', 'value')])

def update_output(value):
   df = pd.read_csv('empty.csv')
   
   fig6 = make_subplots(specs=[[{"secondary_y": True}]])
   fig6.add_trace(
    go.Scatter(x=df.Year,y=df['Bank return on assets (%, after tax)'], name="Bank Return On Asset"),
    )
   fig6.add_trace(
    go.Scatter(x=df.Year, y=df['Bank return on equity (%, after tax)'],name="Bank Return On Equity")    
    )
   fig6.update_layout(
    title_text="Bank Return On Asset and Bank Return On Equity"
    )
     
   if value=='Australian Securities and Investments Commission':
        df = pd.read_csv('australia.csv')
        fig6 = make_subplots(specs=[[{"secondary_y": True}]])
        fig6.add_trace(
          go.Scatter(x=df.Year,y=df['Bank return on assets (%, after tax)'], name="Bank Return On Asset"),
        )
        fig6.add_trace(
          go.Scatter(x=df.Year, y=df['Bank return on equity (%, after tax)'],name="Bank Return On Equity")    
        )
        fig6.update_layout(
          title_text="Bank Return On Asset and Bank Return On Equity"
        )
        return fig6
   if value=='Bank of India':
        df = pd.read_csv('India.csv')
        fig6 = make_subplots(specs=[[{"secondary_y": True}]])
        fig6.add_trace(
          go.Scatter(x=df.Year,y=df['Bank return on assets (%, after tax)'], name="Bank Return On Asset"),
        )
        fig6.add_trace(
          go.Scatter(x=df.Year, y=df['Bank return on equity (%, after tax)'],name="Bank Return On Equity")    
        )
        fig6.update_layout(
          title_text="Bank Return On Asset and Bank Return On Equity"
        )
        return fig6
   return fig6


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('first-dropdown', 'value')])

def update_output(value):
   if value=='Australian Securities and Investments Commission': 
        return (html.P([ '{}'.format(value)," menggunakan",html.Br(),"API",html.Br(),"Data Pullback"]))
   if value=='Bank of India': 
        return (html.P([ '{}'.format(value)," menggunakan",html.Br(),"API",html.Br(),"Data Pullback"]))
   return (html.P([ '{}'.format(value)]))


if __name__ == '__main__':
    app.run_server(debug=True)
