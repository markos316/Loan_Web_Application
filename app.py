import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input

import numpy as np
import plotly.graph_objects as go

from LoanObject import Loan

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(
        children='Loan Calculator and Visualizaton',
        style={'text-align': 'center'}
    ),
    html.Div([
        html.P([
            html.Label('Enter loan amount: '),
            dcc.Input(value='5000', type='number', id='loan_amt')
        ],
        style={'width': '250px', 'margin-right': 'auto',
                   'margin-left': 'auto', 'text-align': 'center'}),

        html.P([
            html.Label('Loan term in months: '),
            dcc.Input(value='36', type='number', id='term')
        ],
        style={'width': '250px', 'margin-right': 'auto',
                   'margin-left': 'auto', 'text-align': 'center'}),

        html.P([
            html.Label('Interest rate per year: '),
            dcc.Input(value='4.5', type='number', id='interest')

        ],
        style={'width': '250px', 'margin-right': 'auto',
                   'margin-left': 'auto', 'text-align': 'center'}),

        html.P([
            html.Label('Extra payment: '),
            dcc.Input(value='0', type='number', id='extra_paym')
        ],
        style={'width': '250px', 'margin-right': 'auto',
                   'margin-left': 'auto', 'text-align': 'center'}),

        ],
        ),
    html.Div([
        html.H6('Amortization Scheudle'),
        dcc.Graph(id='table'),
        html.H6('Loan Bar Graph'),
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(id='year-slider'),
        html.H6(id='output')]
    ),
    html.Div(id='my-output'),
    ]
)


@app.callback(
   Output('output','children'), Output('table', 'figure'), Output('graph-with-slider', 'figure'), Output('year-slider', 'min'), Output('year-slider', 'max'), Output('year-slider', 'value'),
    Output('year-slider', 'marks'),  Output('year-slider', 'step'), Input('loan_amt', 'value'), Input('term', 'value'), Input('interest', 'value'),
    Input('extra_paym', 'value')
)
def update_loan_amt(loan_amt, term, interest, extrapaym):
    #main_loan = Loan(loan_amt, intest, term, 0)
    loan_amt = float(loan_amt)
    interest = float(interest)
    columns = {'Loan'}
    lower = interest - 0.5 * 4
    upper = interest + 0.5 * 4
    index = np.arange(lower, upper, 0.5)
    portfolio = pd.DataFrame(index=index, columns=columns)

    for index, row in portfolio.iterrows():
        portfolio.loc[index, ['Loan']] = Loan(loan_amt, float(index), term, extrapaym)

    df = portfolio.loc[interest, 'Loan'].calculation()

    cols = {'Marks'}

    dfm = pd.DataFrame(columns=cols, index=range(1, 10))

    for index, row in dfm.iterrows():
        dfm.loc[index, ['Marks']] = lower
        lower = lower + 0.5


    min = dfm['Marks'].min()
    max = dfm['Marks'].max()
    value = float(interest)
    marks = {str(Marks): str(Marks) for Marks in dfm['Marks']}
    step = None

    fig = go.Figure(data=[
        go.Bar(name='Extra Payment', x=df['Month'], y=df['Extra Payment'], text=extrapaym, textposition='auto'),
        go.Bar(name='Principal', x=df['Month'], y=df['Principal'], text=df['Principal'], textposition='auto'),
        go.Bar(name='Interest', x=df['Month'], y=df['Interest'], text=df['Monthly Payment'], textposition='outside')
                    ])
    fig.update_layout(barmode='stack')

    fig1 = go.Figure(data=[go.Table(
        header=dict(values=['Month', 'Principal Paid', 'Interest Paid', 'Monthly Payment', 'Total Interest Paid', 'Balance Left'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df['Month'], df['Principal'], df['Interest'], df['Monthly Payment'], df['Total Interest'], df['Balance']],
                   fill_color='lavender', align='left')
    )])
    interest_total = round(df['Interest'].sum(), 2)
    total = interest_total + loan_amt
    text = 'Principal Paid: $' + str(loan_amt) + '\n' + ' Interest Paid: $' + str(interest_total) + '\n' + 'Total Paid: $' + str(total)

    return text, fig1, fig, min, max, value, marks, step



#@app.callback(Output('graph-with-slider', 'figure'), Input())


if __name__ == "__main__":
    app.run_server(debug=True)
