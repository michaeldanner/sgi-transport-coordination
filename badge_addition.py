import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


# df = read_tables(88)
data_path = './data2.xlsx'
df = pd.read_excel(data_path)

print(df.shape)

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
                                        html.H5(" ", className="spacer"),
                                        html.H5(f"{row['First Name']} {row['Surname']}", className="card-title",
                                                style={'color': row['Color']}),
                                        # html.H5(f"{row['Surname']}", className="card-title"),
                                        html.P(f"{row['eyc']} {row['Country']}", className="card-text", style={'color': row['Color']}),
                                    ], width=6),
                                    dbc.Col([
                                        html.H5("Frankfurt Ikeda Peace Culture Centre", className="card-small", style={'color': row['Color']}),
                                        html.H5("Walldorf (Germany), May 2024", className="card-small", style={'color': row['Color']}),
                                        html.H5(f"Hotel: {row['Hotel']}", className="card-title", style={'color': row['Color']}),
                                        html.P(f"{row['Address']}", className="card-small", style={'color': row['Color']}),
                                        html.H5(f"Diet: {row['Food']}", className="card-title", style={'color': row['Color3']}),
                                        html.H5(f"{row['Bus']}", className="card-title", style={'color': row['Color2']}),
                                    ], width=6),
                                ])
                            ]),
                            dbc.CardImg(src=app.get_asset_url(row['Flag_url']), bottom=True, className='card-img',
                                        style={'opacity': row['Opacity']})
                            # dbc.CardFooter("SGI European Conference in May 2024", className="card-text"),
                        ])
                    ]),  # Approx 5,5 x 9,5 cm -- 2,3 x 3,75
                ], className='card-container')
            ], width=12) for index, row in df.iterrows()
        ], className='g-4')
    ], fluid=False)
])


if __name__ == '__main__':
    app.run_server(debug=False)
