# index.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from pages import utils
from pages import home, friday, thursday, wednesday, saturday, sunday, monday, train, badge, departure_train, busses
import os
import dash_bootstrap_components as dbc


root_dir = os.path.dirname(os.path.abspath(__file__))


def read_tables(day):
    # regular_path = './regular.xlsx'
    # support_path = './supporters.xlsx'
    # eba_path = './eba.xlsx'
    # german_path = './german_support.xlsx'
    data_path = './data.xlsx'

    df = pd.read_excel(data_path)
    # df = df[df['Travel to Frankfurt by'] == "Airplane"]

    if False:
        # Read the Excel file
        df_regular = pd.read_excel(regular_path)
        df_regular['Group'] = 'Reg'
        df_support = pd.read_excel(support_path)
        df_support['Group'] = 'Sup'
        df_eba = pd.read_excel(eba_path)
        df_eba['Group'] = 'EBA'

        # print(df_regular.columns.values)

        # merge the three files
        df_support = pd.concat([df_regular, df_support], ignore_index=True)
        df = pd.concat([df_support, df_eba], ignore_index=True)

        # df = pd.read_excel(german_path)

        # add more information to the tables
        df.rename(columns={'Arrival Time (00:00)': 'Arrival_Time'}, inplace=True)
        df.rename(columns={'Departure Time (00:00)': 'Departure_Time'}, inplace=True)

        df.rename(columns={'Your native language': 'Native'}, inplace=True)
        df.rename(columns={'Other languages you speak': 'Languages'}, inplace=True)
        df.rename(columns={'Flight number/Train number/Bus number': 'Flight #'}, inplace=True)

        # correct input mistakes
        try:
            df.loc[df['Arrival_Time'] == 'I will arrive on Thursday already in Frankfurt at 14:04 Frankfurt Hbf', ['Arrival Date', 'Arrival_Time']] = ['09.05.2024', '14:04']
            df.loc[df['Arrival_Time'] == '13:00 but on the 09.05,', ['Arrival Date', 'Arrival_Time']] = ['09.05.2024', '13:00']
            df.loc[df['Arrival_Time'] == 'actually 9/5/24 at 19:55', ['Arrival Date', 'Arrival_Time']] = ['09.05.2024', '19:55']
            df.loc[df['Arrival_Time'] == 'not known yet (aiming for times suggested)', ['Arrival_Time']] = ['00:00']
            df.loc[df['Arrival_Time'] == 'Not yet confirmed', ['Arrival_Time']] = ['00:00']
            df.loc[df['Arrival_Time'] == '05 p.m.', ['Arrival_Time']] = ['17:00']
            df.loc[df['Arrival_Time'] == '8:00 am (at Frankfurt Airport)', ['Arrival_Time']] = ['08:00']
            df.loc[df['Ticket-Nr'] == "150523-0109-YD", ['Arrival Date']] = ['09.05.2024']
            df.loc[df['Ticket-Nr'] == "150523-0046-TR", ['Arrival Date']] = ['09.05.2024']
        except KeyError:
            print("key error")

        try:
            df['Arrival_Time'] = df['Arrival_Time'].apply(utils.validate_and_format_time)
            df['Arrival Date'] = df['Arrival Date'].apply(utils.convert_to_datetime)
            df['Departure_Time'] = df['Departure_Time'].apply(utils.validate_and_format_time)
            df['Departure Date'] = df['Departure Date'].apply(utils.convert_to_datetime)
        except KeyError:
            print("key error")

        df['First Name'] = df['First Name'].apply(utils.format_name)
        df['Surname'] = df['Surname'].apply(utils.format_name)

        df['Terminal'] = ''
        df['Estimated'] = df['Arrival_Time']

        # Flight numbers to estimated time
        df['Flight #'] = df['Flight #'].apply(utils.convert_flight_number_to_icao)

        df['Flag_url'], df['Country'] = zip(*[utils.country_code_to_flag(code) for code in df['Country']])
        df['Flag'] = df['Flag_url'].apply(lambda x: f'<img src="assets/{x}" width="40" height="23">')

        duplicates = df.duplicated(subset=['First Name', 'Surname'], keep=False)
        # keep=False marks all duplicates as True, change to 'first' or 'last' to keep either
        # Filter the DataFrame to show only duplicates
        df_duplicates = df[duplicates]
        print(df_duplicates[['First Name', 'Surname']])
        # Remove duplicates, keeping the first occurrence
        df = df.drop_duplicates(subset=['First Name', 'Surname'], keep='first')

    online = False
    if online:
        df['Flight #'] = df['Flight #'].apply(utils.convert_flight_number_to_icao)
        df.loc[df['Flight #'] == 'BAW902', ['Terminal', 'Estimated']] = ['FRA T2', '07:17 - 07:08']

        # Filter out entries where arrival is by car, train, or bus
        filtered_df = df[~df['Travel to Frankfurt by'].isin(['Car', 'Train', 'Bus'])]
        # filtered_df = filtered_df[filtered_df['Arrival Date'] == 10.0]
        # print(filtered_df)

        # Select distinct flight_number and arrival_date pairs
        distinct_flights = filtered_df[['Flight #', 'Arrival Date']].drop_duplicates()

        distinct_flights[['Terminal', 'Estimated']] = distinct_flights.apply(utils.get_flightinfo, axis=1)
        # print(distinct_flights)
        distinct_flights.to_excel('flights.xlsx', index=False, engine='openpyxl')

    df[['Terminal', 'Estimated']] = df.apply(utils.apply_flight_number, axis=1)

    dfs = df.sort_values(by=['Arrival Date', 'Arrival_Time'], ascending=[True, True])
    dfs2 = df.sort_values(by=['Departure Date', 'Departure_Time'], ascending=[True, True])
    dfs_names = df.sort_values(by=['Surname', 'First Name'], ascending=[True, True])

    df_a = dfs[dfs['Travel to Frankfurt by'] == "Airplane"]
    df_n = dfs[dfs['Travel to Frankfurt by'] != "Airplane"]
    df_d = dfs2[dfs2['Departure from Frankfurt by'] == 'Airplane']
    df_dn = dfs2[dfs2['Departure from Frankfurt by'] != "Airplane"]

    # separate the dataframes into time slots
    dataframe = []
    if day == 8:
        df_8 = df_a[df_a['Arrival Date'] == 8]
        dataframe.append(df_8)
    elif day == 9:
        df_9 = df_a[df_a['Arrival Date'] == 9]
        df_9r = df_9[df_9['Group'] == 'Reg']
        df_9s = df_9[df_9['Group'] == 'Sup']
        dataframe.append(df_9r)
        dataframe.append(df_9s)
    elif day == 10:
        df_10 = df_a[df_a['Arrival Date'] == 10]
        df_10_0 = df_10[df_10['Arrival_Time'] <= '10:15']
        df_10_14 = df_10[(df_10['Arrival_Time'] > '10:15') & (df_10['Arrival_Time'] <= '14:10')]
        df_10_16 = df_10[(df_10['Arrival_Time'] > '14:10') & (df_10['Arrival_Time'] <= '15:30')]
        df_10_17 = df_10[(df_10['Arrival_Time'] > '15:30') & (df_10['Arrival_Time'] <= '16:30')]
        df_10_18 = df_10[(df_10['Arrival_Time'] > '16:30') & (df_10['Arrival_Time'] <= '17:30')]
        df_10_20 = df_10[(df_10['Arrival_Time'] > '17:30') & (df_10['Arrival_Time'] <= '19:20')]
        df_10_22 = df_10[df_10['Arrival_Time'] > '19:20']
        dataframe.append(dict(title=f"{day}.05.2024 - 12:00", frame=df_10_0))
        dataframe.append(dict(title=f"{day}.05.2024 - 14:00", frame=df_10_14))
        dataframe.append(dict(title=f"{day}.05.2024 - 16:00", frame=df_10_16))
        dataframe.append(dict(title=f"{day}.05.2024 - 17:00", frame=df_10_17))
        dataframe.append(dict(title=f"{day}.05.2024 - 17:40", frame=df_10_18))
        dataframe.append(dict(title=f"{day}.05.2024 - 19:30", frame=df_10_20))
        dataframe.append(dict(title=f"{day}.05.2024 - 21:10", frame=df_10_22))
    elif day == 11:
        df_11 = df_d[df_d['Departure Date'] == 11]
        dataframe.append(df_11)
    elif day == 12:
        df_12 = df_d[df_d['Departure Date'] == 12]
        df_12_0 = df_12[df_12['Departure_Time'] <= '13:30']
        df_12_15 = df_12[(df_12['Departure_Time'] > '13:30') & (df_12['Departure_Time'] <= '15:30')]
        df_12_16 = df_12[(df_12['Departure_Time'] > '15:30') & (df_12['Departure_Time'] <= '16:10')]
        df_12_17 = df_12[(df_12['Departure_Time'] > '16:10') & (df_12['Departure_Time'] <= '17:40')]
        df_12_22 = df_12[df_12['Departure_Time'] > '17:40']
        dataframe.append(dict(title=f"{day}.05.2024 - 12:00", frame=df_12_0))
        dataframe.append(dict(title=f"{day}.05.2024 - 14:00", frame=df_12_15))
        dataframe.append(dict(title=f"{day}.05.2024 - 16:00", frame=df_12_16))
        dataframe.append(dict(title=f"{day}.05.2024 - 17:00", frame=df_12_17))
        # dataframe.append(dict(title=f"{day}.05.2024 - 18:00", frame=df_12_18))
        dataframe.append(dict(title=f"{day}.05.2024 - 21:00", frame=df_12_22))
    elif day == 13:
        df_13 = df_d[df_d['Departure Date'] == 13]
        dataframe.append(df_13)
    elif day == 0:
        dfs.to_excel('data2.xlsx', index=False, engine='openpyxl')
        dataframe.append(dfs)
    elif day == 1:
        dfn_bus = df_n[df_n['Travel to Frankfurt by'] == "Bus"]
        dfn_train = df_n[df_n['Travel to Frankfurt by'] == "Train"]
        dfn_car = df_n[df_n['Travel to Frankfurt by'] == "Car"]
        dataframe.append(dict(title="Bus", frame=dfn_bus))
        dataframe.append(dict(title="Train", frame=dfn_train))
        dataframe.append(dict(title="Car", frame=dfn_car))
    elif day == 2:
        dfdn_bus = df_dn[df_dn['Departure from Frankfurt by'] == "Bus"]
        dfdn_train = df_dn[df_dn['Departure from Frankfurt by'] == "Train"]
        dfdn_car = df_dn[df_dn['Departure from Frankfurt by'] == "Car"]
        dataframe.append(dict(title="Bus", frame=dfdn_bus))
        dataframe.append(dict(title="Train", frame=dfdn_train))
        dataframe.append(dict(title="Car", frame=dfdn_car))
    elif day == 50:
        dfs_names = dfs_names[dfs_names['Group'] != "Sup"]
        country_counts = dfs_names['Country'].value_counts()
        #  print(country_counts)
        dfs_names = dfs_names.sort_values(by=['Country', 'Surname', 'First Name'], ascending=[True, True, True])
        df_bus1 = dfs_names[dfs_names['Country'].isin(["United Kingdom", "Italy", "Ireland", "San Marino", "Switzerland"])]
        df_bus2 = dfs_names[dfs_names['Country'].isin(["France", "Spain", "Belgium", "Portugal", "Luxembourg", "Iceland", "Norway"])]
        df_bus3 = dfs_names[dfs_names['Country'].isin(["Germany", "Austria", "Denmark", "Sweden",
                                                       "Netherlands", "Finland"])]
        df_bus4 = dfs_names[dfs_names['Country'].isin(["Czech Republic", "Poland", "Hungary", "Croatia",
                                                       "Greece", "Israel", "Slovenia",
                                                       "Serbia", "Slovakia", "Russia", "Romania",
                                                       "Bulgaria", "Estonia", "Turkey", "Malta", "Lithuania"])]
        dataframe.append(dict(title="Bus 1", frame=df_bus1))
        dataframe.append(dict(title="Bus 2", frame=df_bus2))
        dataframe.append(dict(title="Bus 3", frame=df_bus3))
        dataframe.append(dict(title="Bus 4", frame=df_bus4))
    elif day == 88:
        dataframe.append(dfs_names)
    return dataframe


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Table([
            html.Tr([
                html.Td("Arrival: "),
                html.Td(dcc.Link('Arrive', href='/home'),),
                html.Td(dcc.Link('Wednesday', href='/wednesday')),
                html.Td(dcc.Link('Thursday', href='/thursday'),),
                html.Td(dcc.Link('Friday', href='/friday')),
                html.Td(dcc.Link('Train/Car', href='/train')),
            ]),
            html.Tr([
                html.Td("Departure: "),
                html.Td(dcc.Link('Depart', href='/home'),),
                html.Td(dcc.Link('Saturday', href='/saturday')),
                html.Td(dcc.Link('Sunday', href='/sunday'),),
                html.Td(dcc.Link('Monday', href='/monday')),
                html.Td(dcc.Link('Train/Car', href='/departure_train')),
            ]),
            html.Tr([
                html.Td("Tools: "),
                html.Td(dcc.Link('Badges', href='/badge'),),
                html.Td(dcc.Link('Bus Groups', href='/busses'),),
            ]),
        ]),
    ]),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/friday':
        df = read_tables(10)
        return friday.get_layout(df)
    elif pathname == '/thursday':
        df = read_tables(9)
        return thursday.get_layout(df)
    elif pathname == '/wednesday':
        df = read_tables(8)
        return wednesday.get_layout(df)
    elif pathname == '/saturday':
        df = read_tables(11)
        return saturday.get_layout(df)
    elif pathname == '/sunday':
        df = read_tables(12)
        return sunday.get_layout(df)
    elif pathname == '/monday':
        df = read_tables(13)
        return monday.get_layout(df)
    elif pathname == '/train':
        df = read_tables(1)
        return train.get_layout(df)
    elif pathname == '/departure_train':
        df = read_tables(2)
        return departure_train.get_layout(df)
    elif pathname == '/badge':
        df = read_tables(88)
        return badge.get_layout(df)
    elif pathname == '/busses':
        df = read_tables(50)
        return busses.get_layout(df)
    else:
        df = read_tables(0)
        return home.get_layout(df)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
