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
import dash_cytoscape as cyto
import dash_table
from plotly.subplots import make_subplots
import plotly.graph_objects as go

cyto.load_extra_layouts()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True

readytgntahun=pd.DataFrame(columns=[])
df = pd.read_csv('australia net interest margin.csv')
df['DATE'] = pd.to_datetime(df['DATE'], format="%d/%m/%y")
fig = px.line(df, x=df.DATE, y=df['Net Interest Margin'])

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

default_stylesheet = [
    {
        "selector": "node",
        "style": {
            'width': '10px', 
            'height': '10px',
            "content": "data(label)",
            "font-size": "5px",
           
            
        }
    }
]

myList = ['Pilih Intitusi Pengawasan','Australian Securities and Investments Commission', 'Bank of India','BNR-National Bank of Rwanda','Bangko Sentral ng Pilipinas (BSP)','National Banking and Securities Commission (CNBV)','De Nederlandsche Bank (DNB)','Financial Conduct Authority (FCA)','Monetary Authority of Singapore (MAS)', 'Security Exchange Commision (SEC)','OeNB (Austria)']
default_category = 'Pilih Intitusi Pengawasan'

app.layout = html.Div([
    
    html.Div([html.H1('Financial Services Supervisory Technology', style={'textAlign': 'center','background': '#f9f9f9','box-shadow': '0 0 1px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.1)','border-radius': '5px','margin-bottom': '20px','text-shadow': '1px 1px 1px rgba(0,0,0,.1)'})]),
                       
    
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Banking Industry Current State', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Financial Technology Market State', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Indonesia State', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Risk and Potential', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            
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
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])
             
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    dash.dependencies.Output('x-time-series', 'figure'),
    dash.dependencies.Output('noninterestincome', 'figure'),
    dash.dependencies.Output('cost1', 'figure'),
    dash.dependencies.Output('cost2', 'figure'),
     dash.dependencies.Output('return', 'figure'),
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
   
   fig2 = px.scatter(df, x='Year', y='Bank noninterest income to total income (%)')
   fig2.update_traces(mode='lines+markers')
   fig2.update_xaxes(showgrid=False)
   fig2.update_layout(
       title_text="Bank Non Interest Income (%)"
       )
   
   #figure3-cost structure
   fig3 = px.scatter(df, x='Year', y='Bank overhead costs to total assets (%)')
   fig3.update_traces(mode='lines+markers')
   fig3.update_xaxes(showgrid=False)

    #figure4-cost structure2
   fig4 = px.scatter(df, x='Year', y='Bank cost to income ratio (%)')
   fig4.update_traces(mode='lines+markers')
   fig4.update_xaxes(showgrid=False)
   
   #figreturn
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

        fig2 = px.scatter(df, x='Year', y='Bank noninterest income to total income (%)')
        fig2.update_traces(mode='lines+markers')
        fig2.update_xaxes(showgrid=False)
        fig2.update_layout(
            title_text="Bank Non Interest Income (%)"
            )
        #figure3-cost structure
        fig3 = px.scatter(df, x='Year', y='Bank overhead costs to total assets (%)')
        fig3.update_traces(mode='lines+markers')
        fig3.update_xaxes(showgrid=False)
        fig3.update_layout(
            title_text="Bank Cost Structure"
            )

        #figure4-cost structure2
        fig4 = px.scatter(df, x='Year', y='Bank cost to income ratio (%)')
        fig4.update_traces(mode='lines+markers')
        fig4.update_xaxes(showgrid=False)
        #figreturn
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
   
        
        return (html.P([ '{}'.format(value)," menggunakan",html.Br(),"API",html.Br(),"Data Pullback"])),fig,fig2,fig3,fig4,fig6
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
        
        fig2 = px.scatter(df, x='Year', y='Bank noninterest income to total income (%)')
        fig2.update_traces(mode='lines+markers')
        fig2.update_xaxes(showgrid=False)
        fig2.update_layout(
            title_text="Bank Non Interest Income (%)"
            )
        
        #figure3-cost structure
        fig3 = px.scatter(df, x='Year', y='Bank overhead costs to total assets (%)')
        fig3.update_traces(mode='lines+markers')
        fig3.update_xaxes(showgrid=False)
        fig3.update_layout(
            title_text="Bank Cost Structure"
            )

        #figure4-cost structure2
        fig4 = px.scatter(df, x='Year', y='Bank cost to income ratio (%)')
        fig4.update_traces(mode='lines+markers')
        fig4.update_xaxes(showgrid=False)
        
         #figreturn
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
        
        return (html.P([ '{}'.format(value)," menggunakan",html.Br(),"API",html.Br(),"Data Pullback"])),fig,fig2,fig3,fig4,fig6
    
    
   return (html.P([ '{}'.format(value)])),fig,fig2,fig3,fig4,fig6


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    """
    https://fred.stlouisfed.org/series/DDEI01AUA156NWDB
    australia interest margin
    30 Desember 2020
    Bank net interest margins, the yield curve, and the 2007–2009
financial crisis
     First, the trends in net interest margins suggest that banks will
need to remain increasingly focused on their asset liability management practices and develop innovative strategies to retain
(and build) fee based revenue sources. Second, the reduced cash flows driven by downward pressure on net interest margins forces banks to retain profits and payout fewer dividends when Tier 1 capital buffers are below required levels. Third,
regulators must be cognizant of banks’ plausible shifts in profit seeking behavior over time that could be linked to swings
in the yield curve


Attempting to connect a callback Input item to component:
  "first-dropdown"
but no components with that id exist in the layout.

If you are assigning callbacks to components that are
generated by other callbacks (and therefore not in the
initial layout), you can suppress this exception by setting
`suppress_callback_exceptions=True`
    """