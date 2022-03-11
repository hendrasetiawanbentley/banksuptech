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
        dcc.Tab(label='OJK Coincidence Index 4.0 Design', children=[
           
               
           html.H3('**Bold**OJK Coincidence Index 1.0**Bold**'),
           html.P('OJK Coincidence Index memiliki nilai yang meningkat apabila terjadi “tekanan” pada sistem yang cenderung mengarah ke kondisi “krisis” keuangan. Terdapat 5 (lima) dimensi tekanan didalam OJK Coincidence Index yaitu Pasar Nilai Tukar, Pasar Utang, Pasar Uang Antar Bank, Pasar Saham,  IJK yang akan di agregasikan menjadi 1 (satu) indeks komposit. (sebagaimana terlihat pada gambar dibawah)', className='v', id='v'),
           html.Img(src=app.get_asset_url('cth1.png'), style={'height':'20%', 'width':'20%'}),
           html.P('Semua indikator menggunakan data market dengan frekuensi yang tinggi (harian) dan lag publikasi yang singkat agar dapat mengukur episode stres ke depan dalam waktu yang cepat dan akurat, dan dapat mengestimasi tingkat keparahan episode tersebut. Selanjutnya, Pembobotan masing-masing indeks segmen untuk dikelompokkan ke indeks komposit menggunakan bivariate vector autoregression (VAR) model dan Ambang batas kritikal dihitung dari indeks rata-rata 10 hari sebelum dua tekanan tertinggi pada OJK Index selama masa pengamatan (Januari 2005 s/d Juli 2014).', className='c', id='c'),
           html.Br(),
           html.H3('**Bold**OJK Coincidence Index 2.0**Bold**'),
           html.P('OJK Coin dikembangkan pertama kali pada tahun 2014 berdasarkan naskah Hollo, Kremer, dan Duca (2012). OJK Coin v2.0, merupakan hasil dari penyempurnaan di tahun 2015 yang didokumentasikan melalui Catatan Riset No. CR/15/02. Pengembangaan dilaksanakan untuk meningkatkan keandalan alat ukur tekanan di sektor keuangan domestik'),
           html.P('Pengembangan pada tahun 2015 sebagai berikut:'),
           html.Br(),
           html.P('1.Perubahan perhitungan rentang waktu pergerakan nilai tukar IDR/USD dan imbal hasil (yield) Surat Berharga Negara (SBN) dari periode harian menjadi 10 hari'), 
           html.P('2.Perubahan metode perhitungan tingkat suku bunga antar bank (JIBOR) dari CMAX menjadi CMIN'),
           html.P('3.Perubahan indikator risiko gagal (default) institusi jasa keuangan dengan menggunakan metode component expected shortfall (CES).'),
           html.P('4.Perubahan perhitungan bobot masing-masing segmen dengan menggunakan metode principal component analysis (PCA) dari estimasi bivariate autoregression sebelumnya'),
           html.P('5.Perubahan metode perhitungan batas ambang tekanan berdasarkan kuantil'),
           html.P('6.Perubahan metode penyesuaian skala nilai indikator dari metode standardisasi normal menjadi order statistics'),
           html.Br(),
           html.H3('**Bold**OJK Coincidence Index 3.0**Bold**'),
           html.P('Dari analisa OJK Coin harian, ditemukan inkonsistensi indeks dalam merefleksikan kondisi tekanan granular, terutama pada segmen pasar nilai tukar dan pasar surat utang. Salah satu contohnya adalah inkonsistensi pada hasil analisa tanggal 19 Juli 2018. Kondisi pasar nilai tukar dan surat utang tanggal 19 Juli memburuk apabila dibandingkan dengan tanggal 18 Juli SBN 10Y. Namun demikian, OJK Coin memberikan sinyal kontradiktif dengan nilai indeks segmen pasar nilai tukar dan pasar utang malah menunjukkan penurunan.'),
           html.P('Untuk meningkatkan akurasi OJK Coin dalam mengukur tingkat tekanan pasar keuangan, dilakukan penyempurnaan sebagai berikut:'),
           html.Br(), 
           html.P('1. Menghilangkan indikator B/A spread nilai tukar dan yield SBN; dan'),
           html.P('2. Mengganti indikator B/A spread volatilitas nilai tukar dan CDS menjadi CMIN(60) data last price CDS dan volatilitas nilai tukar. '),
           html.Br(), 
           html.P('<b>Penyeragaman Metode Transformasi Sebagai Berikut</b>'),
           html.P('Terdapat dua jenis metode tranformasi yang digunakan di OJK Coin v2.0 yaitu CMAX/CMIN(60)1 dan Δ20d2. Kedua metode tersebut kemudian dibandingkan untuk mencari metode tranformasi terbaik yang mampu meningkatkan akurasi OJK Coin. Metode tranformasi terpilih akan diaplikasikan kepada seluruh indikator yang ada di OJK Coin secara seragam kecuali segmen IJK. Metode CMAX/CMIN(60) dipilih sebagai metode transformasi tunggal di dalam OJK Coin v3.0.'),
           html.P('Indikator volatilitas IHSG ditambahkan menjadi salah satu indikator segmen pasar saham sebagai alat pengukuran tekanan volatilitas pergerakan harga indeks. Volatilitas IHSG dihitung secara historis dalam rolling rentang sampel 1 bulan. Indikator volatilitas IHSG ini kemudian ditranformasi menggunakan metode CMIN(60), seragam dengan indikator-indikator lainnya.'),
           html.Br(), 
           html.P('OJK Coin telah disempurnakan lebih lanjut dengan cara:'),
           html.P('1. Mengganti indikator segmen pasar utang dan nilai tukar menjadi  CMIN(60) data last price;'),
           html.P('2. Menambahkan indikator CMIN(60) volatilitas 1M daily return IHSG di segmen pasar saham.'),
           html.Br(),
           html.H4('Design OJK Coincidence Index 3.0'),
           html.Img(src=app.get_asset_url('cth2.png'), style={'height':'10%', 'width':'10%'}),
            
           html.P('Paper Penyusunan OJK Index'),
           html.Br(),
           html.P('Brownlees C dan R. Engle 2011 Volatility, Correlation, and Tails for Systemic Risk Measurement Working Paper'),
           html.P('EngleRobert 2002, Dynamic Conditional Correlation: A Simple Class of Multivariate GARCH Models Journal of Business and Economic Statistics'),
           html.P('Hollo D  Kremer M dan M. Lo Duca 2012 CISS A Composite Indicator of Systemic Stress in the Financial System, Working Paper Series No 1426 Macroprudential Research Network (MARS)’),
           html.P('Lo Duca, Marco dan Tuomas A Petone 2011 Macro-financial Vulnerabilities and Future Financial Stress: Assessing Systemic Risks and Predicting Systemic Events, Working Paper Series No. 1311, Macroprudential Research Network MARS, Maret'), 

           

           
            
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
