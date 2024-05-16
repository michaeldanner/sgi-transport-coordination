import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

# df = read_tables(88)
data_path = './data2.xlsx'
df = pd.read_excel(data_path)
df = df.head(6)

print(df.shape)


def run_app_server(name, country, url):
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

    app.layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Container([
                        dbc.Card([
                            # dbc.CardHeader(""),
                            dbc.CardImg(src=app.get_asset_url(f'table_card.png'), top=True, className='img-table'),
                            dbc.CardImgOverlay([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H5(" ", className="table-spacer"),
                                            html.P(f"{country}", className="table-text", style={'color': 'darkblue'}),
                                            html.H5(f"{name}", className="table-title",
                                                    style={'color': 'darkblue'}),
                                            # html.H5(f"{row['Surname']}", className="card-title"),

                                        ], width=12),
                                    ])
                                ]),
                                dbc.CardImg(src=app.get_asset_url(url), bottom=True, className='table-card-img',
                                            style={'opacity': 1})
                                # dbc.CardFooter("SGI European Conference in May 2024", className="card-text"),
                            ])
                        ], className='table-card'),  # Approx 5,5 x 9,5 cm -- 2,3 x 3,75
                    ], className='table-container')
                ], width=12)
            ], className='g-4')
        ], fluid=False)
    ])

    app.run_server(debug=True)


if __name__ == '__main__':
    run_app_server("Hans-Martin Besenfelder", "Australia", "au.svg")
