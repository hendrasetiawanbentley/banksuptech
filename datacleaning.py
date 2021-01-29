#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 21:52:12 2020

@author: hendrasetiawan
"""

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




"""

#data clean 1

df = pd.read_csv('sumberdata.csv')
df.columns = df.columns.str[:5]
df=df.rename(columns={"Count": "Country"})
df = df.loc[df["Country"]== "Australia"]
df1_transposed = df.T
df1_transposed = df1_transposed.iloc[1:]
new_header = df1_transposed.iloc[0] #grab the first row for the header
df1_transposed  = df1_transposed [1:] #take the data less the header row
df1_transposed .columns = new_header #set the header row as the df header
df1_transposed=df1_transposed.fillna(0)
df1_transposed.index.names = ['Year']
for column in df1_transposed:
    df1_transposed[column ] = pd.to_numeric(df1_transposed[column], errors='coerce').fillna(0, downcast='infer')
df1_transposed.to_csv("australia.csv")

#data clean 2 make per country
   
def countryselection():
   with open("listofcountry.txt") as f:
           inventories = f.readlines()
           countryname=[item.strip() for item in inventories]
           for country in countryname:
               df = pd.read_csv('sumberdata.csv')
               df.columns = df.columns.str[:5]
               df=df.rename(columns={"Count": "Country"})
               df = df.loc[df["Country"]== country ]
               df1_transposed = df.T
               df1_transposed = df1_transposed.iloc[1:]
               new_header = df1_transposed.iloc[0] #grab the first row for the header
               df1_transposed  = df1_transposed [1:] #take the data less the header row
               df1_transposed .columns = new_header #set the header row as the df header
               df1_transposed=df1_transposed.fillna(0)
               df1_transposed.index.names = ['Year']
               for column in df1_transposed:
                   df1_transposed[column ] = pd.to_numeric(df1_transposed[column], errors='coerce').fillna(0, downcast='infer')
               df1_transposed.to_csv(country+".csv")
 

#df=df.fillna(0)

#df['Bank net interest margin (%)'] = pd.to_numeric(df['Bank net interest margin (%)'], errors='coerce').fillna(0, downcast='infer')
#for column in df:
#    df[column ] = pd.to_numeric(df[column], errors='coerce').fillna(0, downcast='infer')
#df.to_csv("australia.csv")

"""



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#df = pd.read_csv('sumberdata.csv')
#df.columns = df.columns.str[:5]
#df=df.rename(columns={"Count": "Country"})
#df = df.loc[df["Country"]== "Australia"]
#df1_transposed = df.T
#df1_transposed.to_csv("australia.csv")
#df=df.fillna(0)

#df['Bank net interest margin (%)'] = pd.to_numeric(df['Bank net interest margin (%)'], errors='coerce').fillna(0, downcast='infer')
#for column in df:
#    df[column ] = pd.to_numeric(df[column], errors='coerce').fillna(0, downcast='infer')
#df.to_csv("australia.csv")



#df=df.fillna(0)

#df['Bank net interest margin (%)'] = pd.to_numeric(df['Bank net interest margin (%)'], errors='coerce').fillna(0, downcast='infer')
#for column in df:
#    df[column ] = pd.to_numeric(df[column], errors='coerce').fillna(0, downcast='infer')
#df.to_csv("australia.csv")
#fig = px.line(df, x=df.Year, y=df['Bank net interest margin (%)'])

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


#figure2
fig2 = px.scatter(df, x='Year', y='Bank noninterest income to total income (%)')
fig2.update_traces(mode='lines+markers')
fig2.update_xaxes(showgrid=False)
fig2.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                    xref='paper', yref='paper', showarrow=False, align='left',
                    bgcolor='rgba(255, 255, 255, 0.5)', text="Bank noninterest income to total income (%)")
fig2.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})




#figure3-cost structure
fig3 = px.scatter(df, x='Year', y='Bank overhead costs to total assets (%)')
fig3.update_traces(mode='lines+markers')
fig3.update_xaxes(showgrid=False)

#figure4-cost structure2
fig4 = px.scatter(df, x='Year', y='Bank cost to income ratio (%)')
fig4.update_traces(mode='lines+markers')
fig4.update_xaxes(showgrid=False)

#figure5-boone indicator
fig5 = px.scatter(df, x='Year', y='Boone indicator')
fig5.update_traces(mode='lines+markers')
fig5.update_xaxes(showgrid=False)

#figure6-Profitability indicator
fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
fig6.add_trace(
    go.Scatter(x=df.Year,y=df['Bank return on assets (%, after tax)'], name="Bank Raturn On Asset"),
    )
fig6.add_trace(
    go.Scatter(x=df.Year, y=df['Bank return on equity (%, after tax)'],name="Bank Return On Equity")    
)

# Add figure title
fig6.update_layout(
    title_text="Bank Raturn On Asset and Bank Return On Equity"
)
# Set x-axis title
fig6.update_xaxes(title_text="Year")
# Set y-axes titles
fig6.update_yaxes(
        title_text="<b>Percentage (%)</b>", 
        secondary_y=False)
fig6.update_yaxes(
        title_text="<b>secondary</b> yaxis title", 
        secondary_y=True)





app.layout = html.Div([
    dcc.Graph(figure=fig),
    html.H6('- Net Interest Margin adalah cost of intermediation. Indikator ini memiliki trend menurun sepanjang periode. Di sisi lain, return on asset cenderung bertahan pada level yang sama. Jarak yang melebar antara garis NIM dan RoE mengindikasikan industri perbankan berhasil melakukan utilisasi teknologi pada operasional untuk efesiensi atau perubahan model bisnis/revenue stream'),
    html.H6('- Intermediation Cost mengandung variable seperti interest expense, risk premium, operational cost , dan target profit. Variabel variable tersebut menjadi faktor yang membentuk spread antara interest income minus interest expense'),
    html.H6('- Penelitian tentang NIM mengarisbawahi faktor yang mempengaruhi NIM sebagai berikut'),
    html.P('- (Md. Shahidul Islama , Shin-Ichi Nishiyama (2015)) relative size of the bank (negative), Liquid asset–total asset ratio (positive), Equity–total asset ratio (positive), Operating expenses–total asset ratio (positive), Growth rate of GDP (negative), Required reserve to total asset ratio (positive)'),
    html.P('- (Afanisieff et al. (2002) - (bank central of brazil),  opportunity cost and operating cost (positively), basic interest rate (positively) , the risk premium (positively), '),
    html.P('- (Saunders and Schumacher (2000), implicit interest payments (positive),opportunity cost (positive),inflation rate (negative)'),
    html.H6('- NIM Mathematical Modelling - Dealership Model'),
    html.P('- Penelitian tentang NIM mengarisbawahi faktor yang mempengaruhi NIM sebagai berikut'),
    html.P('- the bank is viewed as "a dealer" (essentially a demander of one type of deposit and supplier of one type of loan)'),
    html.Img(src=app.get_asset_url('ho.png'), style={'height':'100%', 'width':'100%'}),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6)
    
    
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
    
   
    
    
    """
    Variabel di dalam data
    Bank net interest margin (%)	
    Bank noninterest income to total income (%)	
    Bank overhead costs to total assets (%)
	Bank return on assets (%, after tax)	
    Bank return on equity (%, after tax)	
    Bank Z-score	
    Boone indicator	
    Debit card (% age 15+)	
    Credit card (% age 15+)	
    Domestic credit to private sector (% of GDP)	
    Nonbank financial institutions’ assets to GDP (%)	B
    Bank non-performing loans to gross loans (%)
	Bank cost to income ratio (%)	
    Bank concentration (%)	
    Bank branches per 100,000 adults
    """
    
    
    
    
    
    
    """
    Excess liquidity and net interest margins: Evidence from
Vietnamese banks

    Excess liquidity has recently become a prominent phenomenon in emerging economies
    reflects intermediation efficiency or the cost of intermediation (Almarzoqi & Naceur, 2015)
    This endowment effect, which suggests the rigidity of deposit rates, is in line with Claessens, Coleman, and Donnelly’s (2018) finding that
low rates negatively affect NIMs as banks are reluctant to lower deposit rates quickly. Ampudia and Van den Heuvel (2019)
Second, the quantity effect argues that higher policy rates decrease bank loans, and banks then tend to expand NIMs to maintain
their profitability with a smaller credit volume (Alessandri & Nelson, 2015)

Second, the quantity effect argues that higher policy rates decrease bank loans, and banks then tend to expand NIMs to maintain
their profitability with a smaller credit volume (Alessandri & Nelson, 2015). Borio et al. (2017) find a positive impact of the interest
rate structure on the net interest income for 14 major advanced economies. Alessandri and Nelson (2015) provide evidence that
policy rates contribute positively to banks’ NIMs and suggest that banks in the United Kingdom raise their lending interest rates and
lower lending quantities in response to higher funding costs.

 In this line, Berry, Ionescu, Kurtzman, and Zarutskie (2019)
note that tightening monetary policy episodes in the United States do not always lead to higher NIMs, as interest rate pass-through
sensitivities depend on the competitive environment of deposits and loans.

We find that higher
monetary policy interest rates expand NIMs, while excess liquidity compresses NIMs.

We suggest that central banks reduce excess liquidity in the economies to maintain healthy profitability in the banking systems
and financial stability

========================================

The determinants of bank net interest margins: A panel
evidence from South Asian countries - 
(Md. Shahidul Islama , Shin-Ichi Nishiyama (2015))

The paper
relative size of the bank (negative)
Liquid asset–total asset ratio (positive)
Equity–total asset ratio (positive)
Operating expenses–total asset ratio (positive)
Growth rate of GDP (negative)
Required reserve to total asset ratio (positive)

High NIM - the higher wealth maximizer for the bank, the lower will be the social welfare
Low NIM - the lower wealth maximizer for the bank, the higher will be the social welfare 



The determinants of bank interest rate margins:
an international study
Saunders and Schumacher (2000) 

narrow margins may be indicative of a relatively
competitive banking system with a low level of intermediation costs and regulatory
“taxes” (e.g. reserve requirements and capital requirements)

the cost of intermediation services

this paper assumes that the representative bank is
a risk-averse agent that acts as a dealer in a market for the immediate provision of
deposits and loans.

The effect of market structure on bank spreads appears to vary across countries.
The more segmented or restricted the banking system, in terms of geographic restrictions on branching and universality of banking services, the larger appears to be the
monopoly power of existing banks and the higher their spreads.

bank capital assets ratios are generally significant and have the
expected positive signs

Banks seek to lower the cost of holding relatively high capital ratios by demanding
higher NIMs

implicit interest payments are measured by non-interest expense minus
other operating income divided by total average assets

implicit interest payments (positive), 
opportunity cost (positive), 



whether bank margins are providing effective price signals to market players (Hawtrey and Liang, 2008).



Afanisieff et al. (2002) 
opportunity cost and operating cost (positively)
basic interest rate (positively) 
the risk premium (positively)
inflation rate (negative)
 
but a set of macroeconomic variables such as 
the market interest rate, 
the volatility of market interest rate, 
inflation rate and output
growth heavily affect margins as well.


Hawtrey and Liang (2008) 
market power, 
operational cost, 
risk aversion, 
interest rate volatility,
credit risk,
volume of loans, 
implicit interest payments 
quality of management.

Tarus et al. (2012) 
operating expenses, 
credit risk and 
inflation are positively 

market concentration and 
economic growth are negatively related to the net interest margins


The dealership model

In undertaking this function it faces a major type of uncertainty and, hence, cost. This cost occurs because the demand for bank loans and the supply of deposits are viewed as stochastic so that deposit supplies (inflows) tend to arrive at different times from loan demands (outflows)

The model indicates that the optimal mark-up (sum of fees) for deposit and loan services will depend on four factors: (i)thedegreeofbankmanagementriskaversion;(ii)themarketstruc- ture in which the bank operates; (iii) the average size of bank transactions;
and (iv) the variance of interest rates.

likely to impact on actual margins derived from balance sheet and income statement data. The factors directly considered are the proba- bility of loan defaults, the opportunity cost of required reserves, and the cost of implicit interest payments on deposits in the form of service change remissions or subsidies

The probability of a new deposit supply (A ) and a new loan demand (X ) arriving at the bank depends on the respective sizes of the two fees a and b.
For example, by raising b,the price of loans, P falls (rates on loans rise) L
and new loan demand is discouraged. By raising a, the price of deposits, P rises (deposit rates fall) so that new deposits are discouraged. Clearly, by mani- pulating the size of the fees a and b, and, therefore, the price or interest spread a + b, the bank can influence the probability of loan and deposit arriva


A large a and a small B will result in a large a/B ratio and, hence, spread (s). That is, if a bank faces relatively inelastic demand and supply functions in the markets in which it operates, it may be able to exercise monopoly power (and earn a producer's rent) by demanding a greater spread than it could get if banking markets were competitive (low a/B ratio)

####                                                                                                                                                                                                                                           
Bank Return on Equity

Why Do Banks Target ROE?
George Pennacchi and João A. C. Santos
Federal Reserve Bank of New York Staff Reports, no. 855 June 2018

EPS growth is better at explaining nonfinancials’ stock market value while ROE is better at explaining banks’ market values.
Greater competition also resulted from a liberalization of intra-state and inter-state bank branching restrictions during the 1980s and 1990s
banks benefited from deposit insurance that we argue was not fairly priced.
The market-to-book values of banks’ stocks react more to ROE announcements than EPS announcements while the reverse occurs for non-financial firms
Begenau and Stafford (2016). They show empirically that banks with low Return on Assets (ROA) attempt to maintain a high ROE by using higher leverage.
The model has several key ingredients. First, the bank’s deposits are insured by the government. Second, the bank has “charter” or “franchise” value that derives from its ability to pay interest on insured deposits that is below a competitive risk-free rate. Third, the bank must pay corporate income taxes.
With respect to the FDIC deposit insurance premiums, historically they have been assessed without regard to individual banks’ risk. It was only in 1991 that the FDIC changed the flat-rate assessment system to one based on the bank’s risk.
1970s, ut since then their preferences have shifted towards ROE.
(iv) that banks’ capital-to-assets ratio declined over time.  
Federal Deposit Insurance Corporation Improvement Act of 1991, began to be implemented in January of 1993. Banks were assigned to a nine-cell matrix depending on their capitalization (well capitalized, adequately capitalized, or undercapitalized) and on their primary federal regulator's composite rating (rating 1 or 2, rating 3, or rating 4 or 5) and depending on their cell charged one out of five possible risk premiums which ranged from 23 to 31 bps.
Note that our model predicts that banks would be especially resistant to post-financial crisis regulation, such as Basel III, that is gradually forcing them to increase their capital.
A by-product of higher capital is downward pressure on the bank’s ROE.                                                                                                                                                                                                                       

    """
  
