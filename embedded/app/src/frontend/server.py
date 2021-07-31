import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as bootstrap
from dash.dependencies import Input, Output, State

from ..user.broker import Broker

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
        lg=8,
    ),
]

user_form = [
    bootstrap.Col(
        [
            bootstrap.Card(
                id="new-member-card",
                children=
                [
                    bootstrap.CardHeader(
                       [html.H4(["Add a member"])]
                    ),
                    bootstrap.Form(
                        id="new-member-form",
                        children=[
                            bootstrap.FormGroup(
                                [
                                    html.Label(["Name"]),
                                    bootstrap.Input(id="name-field")
                                ]
                            ),
                            bootstrap.FormGroup(
                                [
                                    html.Label(["ID"]),
                                    bootstrap.InputGroup(
                                        [
                                            bootstrap.InputGroupAddon(
                                                bootstrap.Button("Load", id="uid-load-button", n_clicks=0),
                                                addon_type="prepend",
                                            ),
                                            bootstrap.Input(id="uid-field"),
                                        ])

                                ]
                            ),
                            bootstrap.Button(
                                id="new-member-submit",
                                children=["Add"],
                                type="Submit",
                                style={
                                    "float": "right"
                                }

                            )
                        ],
                        style={
                            "margin": "1em",
                            "padding": "1em"
                        }
                    ),
                ],
            ),
        ],
        lg=4
    )
]


# Main app layout
app.layout = bootstrap.Container(
    [
        bootstrap.Row(
            header,
            align="top",
        ),
        bootstrap.Row(
            [*body, *user_form],
            align="top"
        ),
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
    Output('new-member-card', 'style'),
    [Input('new-member-submit', 'n_clicks')],
    [State('name-field', 'value'),
     State('uid-field', 'value')])
def submit_new_member(n_clicks, name, uid):
    print(f"Name: {name}, User:{uid}")
    if name is not None and uid is not None:
        broker.add_user(name, int(uid))
    return {}


# Callback for Button
@app.callback(
    Output('uid-field', 'value'),
    [Input('uid-load-button', 'n_clicks')])
def load_uid_from_last_scanned(n_clicks):
    last_tag = broker.get_last_tag()
    print(last_tag)
    if last_tag == 0:
        return ""
    return str(last_tag)

