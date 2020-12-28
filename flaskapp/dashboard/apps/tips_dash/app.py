"""Dash uygulaması"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from flaskapp.dashboard.apps.tips_dash.data import get_data

CONFIG = { # bu sabit içerisinde bu Dash uygulamasına ait ayarları tutacağız.
    'BASE_URL': '/h9M5hdnUFRE8qffkqDUrWdK/tips/', # bu key sayesinde iframe olarak bu linke istek attığımızda bu Dash'e ulaşabileceğiz
    'APP_URL': 'tips', # bu key sayesinde rol bazlı yönetim yapabileceğiz
    'APP_NAME': 'Tips Veri Setine Ait Dashboard', # bu key ile navbar da linki nasıl göstereceğimizi gösterecek
    'MIN_HEIGHT': 1500, # iframe'in boyutunu set edecek
}


def add_dash(server):
        
    def get_fig(df):
        return px.scatter(df, x="total_bill",
                        y="tip",
                        color='time',
                        log_x=True,
                        size_max=60,
                        title='Toplam Hesaba Göre Verilen Bahşiş Miktarı',
                        labels={'time': 'Hangi Öğün',
                                'total_bill': 'Toplam Hesap', 'tip': 'Bahşiş'}
                        )


    DF = get_data()

    app = dash.Dash(server=server,
                    routes_pathname_prefix=CONFIG['BASE_URL'],
                    suppress_callback_exceptions=True,
                    external_stylesheets=[dbc.themes.BOOTSTRAP])

    day_dropdown = dcc.Dropdown(
        id='day-dropdown',
        options=[
            
            {'label': f'Gün: {day}', 'value': day} for day in DF['day'].unique()
        ],
        searchable=False,  
        placeholder='Gün Seçebilirsiniz...',  
    )

    smoker_dropdown = dcc.Dropdown(
        id='smoker-dropdown',
        options=[
            {'label': f'Sigara: {smoker}', 'value': smoker} for smoker in DF['smoker'].unique()
        ],
        searchable=False,
        placeholder='Sigara Durumunu Seçebilirsiniz...'
    )

    LAYOUT = html.Div(children=[
        html.H1('Basit Bir Dash Örneği', style={
            'textAlign': 'center',
            'color': 'red',
        }),
        html.Div(children=[
            dbc.Row(children=[
                dbc.Col(children=[
                    day_dropdown,
                smoker_dropdown
                ]),
                dbc.Col(children=[
                    dcc.Graph( 
                id='scatter-chart',
                figure=get_fig(DF)
            )
                ])
            ]),
        ]),
    ])

    app.layout = LAYOUT


    @app.callback(
        dash.dependencies.Output('scatter-chart', 'figure'),
        [dash.dependencies.Input('day-dropdown', 'value'),
        dash.dependencies.Input('smoker-dropdown', 'value')]
    )

    def day_filtrele(day_value, smoker_value):
    
        if not day_value and not smoker_value:
            return get_fig(DF)
        elif day_value and not smoker_value:
            return get_fig(DF.query(f'day == "{day_value}"'))
        elif smoker_value and not day_value:
            return get_fig(DF.query(f'smoker == "{smoker_value}"'))
        else:
            return get_fig(DF.query(f'day == "{day_value}"').query(f'smoker == "{smoker_value}"'))
    
    return server