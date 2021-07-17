import dash
import dash_html_components as html
import dash_core_components as dcc
import sd_material_ui

from dash.dependencies import Input, Output, State
from datetime import datetime

from ..reader import get_reader

app = dash.Dash()
reader = get_reader()

# A Button on Paper
app.layout = sd_material_ui.Paper([
    html.Div(children=[
        html.P(id='output', children=['n_clicks value: . n_clicks_previous value: ']),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=0.5 * 1000,  # in milliseconds
            n_intervals=0
        )
    ]),

    sd_material_ui.Button(id='input', children='Click me'),
])


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(interval):
    tag = reader.LAST_TAG
    return [
        html.Span(f'Last Tag: {tag}'),
    ]


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
