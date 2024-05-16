import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


# df = read_tables(88)
data_path = './data.xlsx'
german_path = './german_support.xlsx'
african_path = './african.xlsx'

df0 = pd.read_excel(data_path)
df0 = df0[['Group', 'First Name', 'Surname', 'Country', 'Flag_url', 'Food', 'Bus']]
df0['Hotel'] = 'Crowne Plaza'
df0['Address'] = 'Lyoner Strasse 44-48, 60528 Frankfurt'
df0['Color'] = 'darkblue'
df0['Color2'] = 'darkblue'
df0['Color3'] = 'darkblue'
df0['Opacity'] = 1
df0.loc[df0['Group'] == 'Sup', 'Hotel'] = 'Anor'
df0.loc[df0['Group'] == 'Sup', 'Address'] = 'An der Brücke 8-10, 64546 Mörfelden-Walldorf'
df0.loc[df0['Group'] == 'Sup', 'Color'] = 'darkred'
df0.loc[df0['Group'] == 'Sup', 'Color2'] = 'white'
df0.loc[df0['Group'] == 'Sup', 'Color3'] = 'darkred'
df0.loc[df0['Group'] == 'Sup', 'Bus'] = '___'
df0.loc[df0['Surname'] == 'Haddad Tschabold', ['Surname', 'Country']] = ['Haddad', 'Tschabold (Switzerland)']
df0.loc[df0['Surname'] == 'Fernández Quijano', ['Surname', 'Country']] = ['Fernández', 'Quijano (Spain)']
df0.loc[df0['Surname'] == 'Maniglier-Sotiropoulos', ['Surname','Country', 'Food']] = ['Maniglier-', 'Sotiropoulos (France)', 'Meat (Special)']
df0.loc[df0['Surname'] == 'Hernandez Kobayashi', ['Surname', 'Country']] = ['Hernandez', 'Kobayashi (Spain)']
df0.loc[df0['Surname'] == 'Yoneoka-Golemehova', ['Surname', 'Country']] = ['Yoneoka-', 'Golemehova (Bulgaria)']
df0.loc[df0['Surname'] == 'Maruyama', ['Surname', 'Country']] = [' ', 'Maruyama (United Kingdom)']
df0.loc[df0['Surname'] == 'Vontor', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Bendinger', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Ferrario', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Hasegawa', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Kilpeläinen', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Voutsina', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Saget', ['Food']] = ['Vegetarian (Special)']
df0.loc[df0['Surname'] == 'Janssens', ['Food']] = ['Vegetarian (Special)']
df0.loc[df0['Surname'] == 'Ranzoni', ['Food']] = ['Vegetarian (Special)']
df0.loc[df0['Surname'] == 'Geracitano', ['Food']] = ['Vegetarian (Special)']
df0.loc[df0['Surname'] == 'Balderrama Sudan', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Indraccolo', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Trama', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Clinton', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Fernandez', ['Food']] = ['Vegetarian (Special)']
df0.loc[df0['Surname'] == 'Siccardi', ['Food']] = ['Vegan (Special)']
df0.loc[df0['Surname'] == 'Craaveiro', ['Food']] = ['Vegan (Special)']
df0.loc[df0['Surname'] == 'Seaword', ['Food']] = ['Meat (Special)']
df0.loc[df0['Surname'] == 'Spühler', ['Hotel']] = ['Crowne Plaza']
df0.loc[df0['Surname'] == 'Spühler', ['Address']] = ['Lyoner Strasse 44-48, 60528 Frankfurt']
df0 = df0.sort_values(by=['Group', 'Surname', 'First Name'], ascending=[True, True, True])

# Isabault MANIGLIER-SOTIROPOULOS    ->    Meat (Special Diet)
# Carola Bendinger    ->    Meat (Special Diet)
# Alice Ferrario    ->    Meat (Special Diet)
# Tomonori Hasegawa    ->    Meat (Special Diet)
# Kari Kilpeläinen    ->    Meat (Special Diet)
# Alexandra Voutsina    ->    Meat (Special Diet)
# Jade Saget    ->    Vegetarian (Special Diet)
# Janssens Philippe    ->    Vegetarian (Special Diet)
# Paola Ranzoni    ->    Vegetarian (Special Diet)
# Francesco Geracitano    ->    Vegetarian (Special Diet)
# Yamila Balderrama Sudan    ->    Meat (Special Diet)


df1 = pd.read_excel(german_path)
df1 = df1[['First Name', 'Surname', 'Country', 'Food']]
df1['Flag_url'] = 'de.svg'
df1['Group'] = 'GS'
df1['Hotel'] = 'Anor'
df1['Address'] = 'An der Brücke 8-10, 64546 Mörfelden-Walldorf'
df1['Color'] = 'darkred'
df1['Color2'] = 'white'
df1['Color3'] = 'darkred'
df1['Bus'] = '___'
df1['Opacity'] = 1
df1.loc[df1['Surname'] == 'Cecchinato', ['Hotel']] = ['Crowne Plaza']
df1.loc[df1['Surname'] == 'Cecchinato', ['Address']] = ['Lyoner Strasse 44-48, 60528 Frankfurt']
df1.loc[df1['Surname'] == 'Kanemaki', ['Hotel']] = ['Crowne Plaza']
df1.loc[df1['Surname'] == 'Kanemaki', ['Address']] = ['Lyoner Strasse 44-48, 60528 Frankfurt']
df1 = df1.sort_values(by=['Group', 'Surname', 'First Name'], ascending=[True, True, True])

df2 = pd.read_excel(african_path)
df2['Bus'] = '___'
df2['Food'] = ' '
df2.loc[df2['Surname'] == 'Mousse', ['Food']] = ['Meat (Special)']
df2.loc[df2['Surname'] == 'Agonglo', ['Food']] = ['Meat (Special)']
df2.loc[df2['Surname'] == 'Ah Vee', ['Food']] = ['Meat (Special)']
df2 = df2.sort_values(by=['Group', 'Surname', 'First Name'], ascending=[True, True, True])
# print(df0)
df = pd.concat([df0, df1], ignore_index=True)
df = pd.concat([df, df2], ignore_index=True)

# df = df.loc[df['Surname'] == 'Danner']
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
                                        html.P(row['Country'], className="card-text", style={'color': row['Color']}),
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
