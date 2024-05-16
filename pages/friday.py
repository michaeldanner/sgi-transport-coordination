# pages/friday.py
from dash import dcc, html, dash_table
from pages import utils
import dash_bootstrap_components as dbc


def get_layout(dfs):
    for df in dfs:
        continue
        # print("Data:")
        # print(df['frame']['Arrival Date'] + " - " + df['frame']['Arrival_Time'])

    layout = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Row(dbc.Col(html.H3(f"Friday, {df['title']} ({df['frame'].shape[0]})"), width={"size": 6, "offset": 1})),
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i, "presentation": 'markdown'} for i in
                                     df['frame'][utils.columns].columns],
                            data=df['frame'].to_dict('records'),
                            # filter_action="native",  # Enable filtering
                            markdown_options={"html": True},  # Allow HTML content
                            style_data_conditional=[
                                {'if': {'state': 'selected'}, 'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                                 'border': '1px solid blue'}
                            ],
                            # row_selectable='single'
                            # css=[{"selector": ".dash-table-container td", "rule": 'max-height: "15px"; height: "15px"; '}],
                            css=[{"selector": "P", "rule": "margin-top: 0; margin-bottom: 0"}],
                            # fixed_rows={'headers': True, 'data': 0},
                            fill_width=False,
                            # page_size=df['frame'].shape[0]
                        ), width=2)
                    ])
                ]) for df in dfs
            ]),
            dbc.Col(html.Div(id='row-info', style={'margin-top': '0px'}), width=4)
        ])  # end Main Row

    ])
    return layout