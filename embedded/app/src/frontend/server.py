import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as bootstrap
from dash.dependencies import Input, Output, State
from datetime import datetime

from ..user.broker import Broker
from ..user.message import Status

app = dash.Dash(
    external_stylesheets=[bootstrap.themes.BOOTSTRAP]
)
broker = Broker()


header = [
    bootstrap.Col([
            html.H1("Kwarqs Check In"),
            html.Hr(),
        ],
    )
]

body = [
    bootstrap.Col(
        [
            bootstrap.Alert(id='live-update-text'),
            dcc.Interval(
                id='interval-component',
                interval=0.5 * 1000,  # in milliseconds
                n_intervals=0
            )
        ],
        md=8,
    ),
    bootstrap.Col(
        [
            html.Div(children=[
                html.P(id='output', children=['n_clicks value: . n_clicks_previous value: ']),
                bootstrap.Button(id='input', children='Click me'),
                ]
            )
        ]
    ),
]


# A Button on Paper
app.layout = bootstrap.Container(
    [
        bootstrap.Row(
            header,
            align="center",
        ),
        bootstrap.Row(
            body,
            align="center"
        )
    ],
    fluid=True,
)


@app.callback(
    Output('live-update-text', 'children'),
    Output('live-update-text', 'color'),
    [Input('interval-component', 'n_intervals')])
def update_text(interval):
    message = broker.get_current_message()
    children = [
        html.H1(message.title, className='display-3'),
        html.P(message.subtitle, className="lead"),
    ]
    return children, message.status


# Callback for Button
@app.callback(
    Output('output', 'children'),
    [Input('input', 'n_clicks')],
    [State('input', 'n_clicks_previous')])
def display_clicks_flat(n_clicks_flat: int, n_clicks_flat_prev: int):
    if n_clicks_flat:
        return [f'n_clicks value: {n_clicks_flat}. n_clicks_prev value: {n_clicks_flat_prev}']
    else:
        return ['n_clicks value: ']
