# pages/friday.py
from dash import dcc, html, dash_table
from pages import utils
import dash_bootstrap_components as dbc


def get_layout(df):
    df = df[0]
    df['Arrived'] = False
    df['Badge'] = False
    columns = utils.col_all
    columns.append({"id": 'Arrived', "presentation": "dropdown"})
    columns.append({"id": 'Badge', "presentation": "dropdown"})
    dropdown = {
        'Arrived': {
            'options': [
                {'label': 'Yes', 'value': True},
                {'label': 'No', 'value': False}
            ]
        },
        'Got the Badge': {
            'options': [
                {'label': 'Yes', 'value': True},
                {'label': 'No', 'value': False}
            ]
        }
    }
    layout = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Row(dbc.Col(html.H3(f"All participants, ({df.shape[0]})"), width={"size": 6, "offset": 1})),
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(
                            id='table',
                            columns=columns,
                            data=df.to_dict('records'),
                            # filter_action="native",  # Enable filtering
                            markdown_options={"html": True},  # Allow HTML content
                            style_data_conditional=[
                                {'if': {'state': 'selected'}, 'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                                 'border': '1px solid blue'}
                            ],
                            css=[{"selector": "P", "rule": "margin-top: 0; margin-bottom: 0"}],
                            fill_width=False,
                        ), width=2)
                    ])
                ])
            ]),
            dbc.Col(html.Div(id='row-info', style={'margin-top': '0px'}), width=4)
        ])  # end Main Row

    ])
    return layout