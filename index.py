from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash_bootstrap_components import ThemeSwitchAIO
import dash

FONT_AWSOME = ['https://use.fontawesome.com/releases/v5.10.2/css/all.css']
app = dash.Dash(__name__, external_stylesheets=FONT_AWSOME)
app.scripts.config.serve_locally = True
server = app.server

# === Styles === #
tab_card = {'hight': '100%'}

main_config = {
    'hovermode': 'x unified',
    'legend': {'yanchor': 'top',
               'y': 0.9,
               'xanchor': 'left',
               'x': 0.1,
               'title': {'text': None},
               'font': {'color': 'white'},
               'bgcolor': 'rgba(0, 0, 0, 0.5)'},
    'margin': {'l': 10, 'r': 10, 't': 10, 'b': 10}
}

config_graph = {'displayModeBar': False, 'showTips': False}

template_theme1 = 'flatly'
template_theme2 = 'darkly'
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# === Lendo e limpando dados === #

df = pd.read_csv('dataset.csv')
df_cru = df.copy()

# Meses em números para poupar memória
df.loc[df['Mês'] == 'Jan', 'Mês'] == 1
df.loc[df['Mês'] == 'Fev', 'Mês'] = 2
df.loc[df['Mês'] == 'Mar', 'Mês'] = 3
df.loc[df['Mês'] == 'Abr', 'Mês'] = 4
df.loc[df['Mês'] == 'Mai', 'Mês'] = 5
df.loc[df['Mês'] == 'Jun', 'Mês'] = 6
df.loc[df['Mês'] == 'Jul', 'Mês'] = 7
df.loc[df['Mês'] == 'Ago', 'Mês'] = 8
df.loc[df['Mês'] == 'Set', 'Mês'] = 9
df.loc[df['Mês'] == 'Out', 'Mês'] = 10
df.loc[df['Mês'] == 'Nov', 'Mês'] = 11
df.loc[df['Mês'] == 'Dez', 'Mês'] = 12

# Removendo o prefixo 'R$' para o tipo inteiro
df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')
df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0

# Transformando dados para tipo inteiro
df['Valor Pago'] = df['Valor Pago'].astype(int)
df['Chamadas realizadas'] = df['Chamadas Realizadas'].astype(int)
df['Dia'] = df['Dia'].astype(int)
df['Mês'] = df['Mês'].astype(int)

# Criando opções pros filtros que virão
options_month = [{'label': 'Ano todo', 'value': 0}]
for i, j in zip(df_cru['Mês'].unique(), df['Mês'].unique()):
    options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value'])

options_team = [{'label': 'Todas Equipes', 'value': 0}]
for i in df['Equipe'].unique():
    options_team.append({'label': i, 'value': i})

# ==== Layout ==== #
app.layout = dbc.Container(children=[
    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Sales Analytics")
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-balance-scale',
                                   style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[
                                           url_theme1, url_theme2]),
                            html.Legend("André Júnior")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button(
                            "Visite o Site", href="https://github.com/andre-jnr", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Top Consultores por Equipe')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc',
                                      config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc',
                                      config=config_graph)
                        ], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(
                                id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '100vh'})

# === Callbacks === #


# Run server
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
