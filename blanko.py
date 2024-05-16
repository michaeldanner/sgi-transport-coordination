import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


# df = read_tables(88)
data_path = './blank.xlsx'

df = pd.read_excel(data_path)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Container([
                    dbc.Card([
                        # dbc.CardHeader(""),
                        dbc.CardImg(src=app.get_asset_url(f'badge_{row["Color"]}.png'), top=True, className='img-fluid'),
                        dbc.CardImgOverlay([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([

                                    ], width=6),
                                    dbc.Col([

                                    ], width=6),
                                ])
                            ]),

                        ])
                    ]),  # Approx 5,5 x 9,5 cm -- 2,3 x 3,75
                ], className='card-container')
            ], width=12) for index, row in df.iterrows()
        ], className='g-4')
    ], fluid=False)
])


if __name__ == '__main__':
    app.run_server(debug=False)
