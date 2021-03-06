import dash
import json
import logging

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as bootstrap
from dash.dependencies import Input, Output, State, ALL

from ..user.broker import Broker

logger = logging.getLogger(__name__)
app = dash.Dash(
    external_stylesheets=[bootstrap.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
broker = Broker()


header = [
    bootstrap.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                bootstrap.Row(
                    [
                        bootstrap.Col(html.Img(
                            src=app.get_asset_url('fans.png'),
                            height="65px"),
                            style={
                                "margin-right": "10px",
                            }),
                        bootstrap.Col(bootstrap.NavbarBrand(
                            "Check In",
                            className="mb h1",
                            style={
                                "font-size": "35px",
                            }
                        )),
                    ],
                    align="center",
                    no_gutters=True
                ),
            ),
        ],
        color="dark",
        dark=True,
        style={
            "margin-bottom": "10px",
            "margin-left": "-15px",
            "margin-right": "-15px",
        }
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
        xs=12
    ),
]

_qr_size = 300
_qr_url = "kwarqs.local"

user_form = [
    bootstrap.Col(
        [
            bootstrap.Card(
                id="new-member-card",
                children=
                [
                    bootstrap.CardHeader(
                        id="new-member-header",
                        children=[
                            html.H4([
                                "Add a member",
                                bootstrap.Button(
                                    children="+",
                                    id="new-member-expand-button",
                                    color="primary",
                                    size="sm",
                                    outline=True,
                                    style={
                                        "float": "right",
                                        "width": "3em",
                                        "border": "0px"
                                    }

                                )
                            ]),
                        ]
                    ),
                    bootstrap.Collapse(
                        id="new-member-collapse",
                        is_open=False,
                        children=bootstrap.Form(
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
                        )
                    ),
                ],
            ),
        ],
        lg=4,
        xs=12,
    ),
    bootstrap.Col(
        [
            html.Img(
                src=f"https://chart.googleapis.com/chart?cht=qr&chl=http%3A%2F%2F{_qr_url}"
                    f"&chs={_qr_size}x{_qr_size}&choe=UTF-8&chld=L|2%27%20alt=",
                style={
                    "max-width": f"{_qr_size}px",
                    "height": f"{_qr_size}px",
                    "float": "right",
                    "margin-top": "20em"
                }
            )
        ],
        lg=8,
        xs=12,
    )
]

manual_sign_in = [
    bootstrap.Col(
        [
            bootstrap.Card(
                id="manual-card",
                children=
                [
                    bootstrap.CardHeader(
                       [html.H4(["Sign in without ID"])]
                    ),
                    bootstrap.DropdownMenu(
                        id="manual-user-list",
                        label="Select your name",
                        bs_size="lg",
                        style={
                            "margin": "auto",
                            "padding": "1.75em",
                        }
                    ),
                ],
                style={
                    "margin": "1em",
                    "padding": "1em"
                }
            )
        ],
        xs=12,
        lg=4,
    )
]

email_button = [
    bootstrap.Col(
        [
            bootstrap.Card(
                id="email-card",
                children=
                [
                    bootstrap.CardHeader(
                        [html.H4(["Export Attendance"])]
                    ),
                    bootstrap.CardBody([
                        bootstrap.Button(
                            id="email-send-button",
                            children=["Send"],
                            color="secondary",
                        )
                        ],
                        style={
                            "margin": "auto"
                        }
                    )
                ]
            )
        ],
        lg=4,
        xs=12,
    )
]

# Main app layout
app.layout = bootstrap.Container(
    [
        *header,
        bootstrap.Row(
            [*body, *manual_sign_in],
            align="top"
        ),
        bootstrap.Row(
            user_form,
            align="top"
        ),
        bootstrap.Row(
            email_button,
            align="top",
            style={
                "margin-top": "5em",
                "margin-bottom": "5em"
            }
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


@app.callback(
    Output('name-field', 'value'),
    [Input('new-member-submit', 'n_clicks')],
    [State('name-field', 'value'),
     State('uid-field', 'value')])
def submit_new_member(n_clicks, name, uid):
    logger.info(f"New member submitted - Name: {name}, User:{uid}")
    if name is not None and uid is not None:
        broker.add_user(name, int(uid))
    return ""


@app.callback(
    Output('uid-field', 'value'),
    [Input('uid-load-button', 'n_clicks')])
def load_uid_from_last_scanned(n_clicks):
    last_tag = broker.get_last_tag()
    if last_tag == 0:
        return ""
    return str(last_tag)


@app.callback(
    Output("manual-user-list", "children"),
    [Input("manual-user-list", "n_clicks")]
)
def load_users(n):
    users = broker.get_all_users()
    logger.info(f"Loading all users. {len(users)} total")
    items = [
        bootstrap.DropdownMenuItem(u.name, key=u.uid, id={
            "type": "manual-user",
            "uid": u.uid
        })
        for u in users
    ]
    return items


@app.callback(
    Output('manual-card', 'style'),
    Input({'type': 'manual-user', 'uid': ALL}, 'n_clicks'),
)
def manual_sign_in_clicked(n_clicks):
    ctx = dash.callback_context

    if len(ctx.triggered) == 1:
        item_string = ctx.triggered[0]['prop_id'].split('.')[0]
        if not item_string:
            return {}
        item = json.loads(item_string)
        uid = item["uid"]
        broker.on_new_tag(uid)

    return {}


@app.callback(
    [Output(f"new-member-expand-button", "children"),
     Output(f"new-member-collapse", "is_open")],
    [Input(f"new-member-expand-button", "n_clicks")],
    [State(f"new-member-collapse", "is_open")],
)
def toggle_accordion(n_clicks, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "+", False

    if is_open:
        return "+", False
    else:
        return "-", True


@app.callback(
    [Output("email-card", 'color')],
    [Input("email-send-button", "n_clicks")],
)
def send_email(n_clicks):
    if n_clicks == 0:
        return 'secondary'

    broker.send_email()
    return 'primary'
