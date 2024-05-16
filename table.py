import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

# df = read_tables(88)
data_path = './data2.xlsx'
df = pd.read_excel(data_path)

print(df.shape)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([

            dbc.Container([
                dbc.Card([
                    # dbc.CardHeader(""),
                    dbc.CardImg(src=app.get_asset_url(f'table_card.png'), top=True, className='img-table'),
                    dbc.CardImgOverlay([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H5(" ", className="table-spacer"),
                                    html.P(f"{row['Country']}", className="table-text", style={'color': 'darkblue'}),
                                    html.H5(f"{row['First Name']} {row['Surname']}", className="table-title",
                                            style={'color': 'darkblue'}),
                                    # html.H5(f"{row['Surname']}", className="card-title"),

                                ], width=12),
                            ])
                        ]),
                        dbc.CardImg(src=app.get_asset_url(row["Flag_url"]), bottom=True, className='table-card-img',
                                    style={'opacity': 1})
                        # dbc.CardFooter("SGI European Conference in May 2024", className="card-text"),
                    ])
                ], className='table-card', id=f'id+{index}'),  # Approx 5,5 x 9,5 cm -- 2,3 x 3,75
            ], className='table-container')

        ], className='g-4') for index, row in df.iterrows()
    ], fluid=False)
])

app.run_server(debug=False)
