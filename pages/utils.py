import re
from datetime import datetime, timedelta
import pandas as pd
import pytz
import requests
from bs4 import BeautifulSoup
import json

col_all = [{"id": 'Group', "name": 'Group'},
           {"id": 'First Name', "name": 'First Name'},
           {"id": 'Surname', "name": 'Surname'},
           {"id": 'Arrival Date', "name": 'Arrival Date'},
           {"id": 'Arrival_Time', "name": 'Arrival_Time'},
           {"id": 'Travel to Frankfurt by', "name": 'Arrive by'},
           {"id": 'Flight #', "name": 'Flight #'},
           {"id": 'Terminal', "name": 'Terminal'},
           {"id": 'Estimated', "name": 'Estimated'},
           {"id": 'Flag', "name": 'Flag', "presentation": 'markdown'},
           {"id": 'Native', "name": 'Native'},
           {"id": 'Country', "name": 'Country'},
           {"id": 'Languages', "name": 'Languages'},
           {"id": 'Departure Date', "name": 'Depart'},
           {"id": 'Departure_Time', "name": 'Depart Time'},
           {"id": 'Departure from Frankfurt by', "name": 'Depart by'}
           ]
columns = [
    'Group', 'First Name', 'Surname', 'Arrival Date', 'Arrival_Time', 'Flight #', 'Terminal', 'Estimated', 'Flag',
    'Native', 'Languages'
]
col_train = [
    'Group', 'First Name', 'Surname', 'Arrival Date', 'Arrival_Time', 'Flight #', 'Flag',
    'Native', 'Languages'
]
col_bus = [{"id": 'Group', "name": 'Group'},
           {"id": 'First Name', "name": 'First Name'},
           {"id": 'Surname', "name": 'Surname'},
           {"id": 'Flag', "name": 'Flag', "presentation": 'markdown'},
           {"id": 'Country', "name": 'Country'},
           {"id": 'Native', "name": 'Native'},
           {"id": 'Languages', "name": 'Languages'},
           ]
col_depart = [{"id": 'Group', "name": 'Group'},
              {"id": 'First Name', "name": 'First Name'},
              {"id": 'Surname', "name": 'Surname'},
              {"id": 'Flag', "name": 'Flag', "presentation": 'markdown'},
              {"id": 'Departure Date', "name": 'Depart'},
              {"id": 'Departure_Time', "name": 'Depart Time'},
              {"id": 'Departure from Frankfurt by', "name": 'Depart by'},
              {"id": 'Flight number/Train number/ Bus number', "name": 'Flight/Train/Bus'},
              {"id": 'Native', "name": 'Native'},
              {"id": 'Languages', "name": 'Languages'},
              ]
col_depart_train = [{"id": 'Group', "name": 'Group'},
              {"id": 'First Name', "name": 'First Name'},
              {"id": 'Surname', "name": 'Surname'},
              {"id": 'Flag', "name": 'Flag', "presentation": 'markdown'},
              {"id": 'Departure Date', "name": 'Depart'},
              {"id": 'Departure_Time', "name": 'Depart Time'},
              {"id": 'Departure from Frankfurt by', "name": 'Depart by'},
              {"id": 'Native', "name": 'Native'},
              {"id": 'Languages', "name": 'Languages'},
              ]


def convert_to_datetime(date_str):
    # Convert string to datetime object using the specified format
    try:
        ret_date = datetime.strptime(str(date_str), "%d.%m.%Y")
    except ValueError:
        ret_date = datetime.strptime('01.01.1980', "%d.%m.%Y")
        print("Date: " + str(date_str))
    return ret_date.strftime("%d")


def format_name(name):
    return str(name).title()


def validate_and_format_time(time_str):
    time_str = str(time_str)

    # Remove 'around' and any adjacent spaces
    time_str = re.sub(r'\s*\baround\b\s*', ' ', time_str).strip()

    # Extended regular expression to match optional 'hs', 'am', or 'pm' at the end
    match = re.match(r"^(2[0-3]|[01]?[0-9])([:.,-h]|)([0-5]?[0-9])\s*(:00|hs|am|pm)?$", time_str, re.IGNORECASE)
    if match:
        hours, _, minutes, period = match.groups()
        hours = int(hours)
        minutes = int(minutes)

        # Normalize the period to lowercase for easier handling
        if period:
            period = period.lower()

        # Convert PM hours to 24-hour format, except for 12 PM
        if period == 'pm' and hours < 12:
            hours += 12
        elif period == 'am' and hours == 12:
            hours = 0  # Midnight edge case

        # Format the hour and minute to ensure two digits
        formatted_time = f"{hours:02}:{minutes:02}"
        return formatted_time
    else:
        print(time_str)
        return time_str


# Convert country codes to emoji flags
def country_code_to_flag(country):
    code = country.lower()
    if code == 'austria' or code == 'österreich':
        code = 'at.svg'
        country = 'Austria'
    elif 'belg' in code:
        code = 'be.svg'
        country = 'Belgium'
    elif 'bulg' in code:
        code = 'bg.svg'
        country = 'Bulgaria'
    elif 'cro' in code or 'hrv' in code:
        code = 'hr.svg'
        country = 'Croatia'
    elif 'czech' in code or 'esko' in code or '\u30C1' in code:
        code = 'cz.svg'
        country = 'Czech Republic'
    elif code == 'iceland':
        code = 'is.svg'
        country = 'Iceland'
    elif 'nmark' in code:
        code = 'dk.svg'
        country = 'Denmark'
    elif code == 'deutschland' or 'ger' in code:
        code = 'de.svg'
        country = 'Germany'
    elif 'esto' in code:
        code = 'ee.svg'
        country = 'Estonia'
    elif code == 'finland' or code == 'suomi':
        code = 'fi.svg'
        country = 'Finland'
    elif 'fra' in code:
        code = 'fr.svg'
        country = 'France'
    elif code == 'greece':
        code = 'gr.svg'
        country = 'Greece'
    elif code == 'hungary' or code == 'ungheria' or code == 'hongrie':
        code = 'hu.svg'
        country = 'Hungary'
    elif code == 'ireland':
        code = 'ie.svg'
        country = 'Ireland'
    elif 'ital' in code:
        code = 'it.svg'
        country = 'Italy'
    elif code == 'israel' or '\u05E9' in code:
        code = 'il.svg'
        country = 'Israel'
    elif code == 'united kingdom' or code == 'uk' or 'u.k' in code:
        code = 'gb.svg'
        country = 'United Kingdom'
    elif code == 'spain' or code == 'españa' or code == 'span':
        code = 'es.svg'
        country = 'Spain'
    elif 'lith' in code:
        code = 'lt.svg'
        country = 'Lithuania'
    elif 'luxem' in code:
        code = 'lu.svg'
        country = 'Luxembourg'
    elif code == 'malta':
        code = 'mt.svg'
        country = 'Malta'
    elif 'nether' in code or 'neder' in code:
        code = 'nl.svg'
        country = 'Netherlands'
    elif code == 'norway' or code == 'norge':
        code = 'no.svg'
        country = 'Norway'
    elif 'pol' in code:
        code = 'pl.svg'
        country = 'Poland'
    elif code == 'portugal':
        code = 'pt.svg'
        country = 'Portugal'
    elif code == 'romania':
        code = 'ro.svg'
        country = 'Romania'
    elif 'russi' in code:
        code = 'ru.svg'
        country = 'Russia'
    elif code == 'san marino':
        code = 'sm.svg'
        country = 'San Marino'
    elif 'serb' in code:
        code = 'rs.svg'
        country = 'Serbia'
    elif 'sloven' in code:
        code = 'si.svg'
        country = 'Slovenia'
    elif 'slovak' in code:
        code = 'sk.svg'
        country = 'Slovakia'
    elif 'swit' in code or 'suis' in code or 'sviz' in code:
        code = 'ch.svg'
        country = 'Switzerland'
    elif 'swe' in code:
        code = 'se.svg'
        country = 'Sweden'
    elif 'turk' in code:
        code = 'tr.svg'
        country = 'Turkey'
    else:
        print(code)
    return code, country


def get_flightinfo(row):
    flightnumber = row['Flight #']
    day = row['Arrival Date']
    url = f"https://www.flightaware.com/live/flight/{flightnumber}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    flight_data = pd.Series([f"unknown", f"unknown"], index=['Terminal', 'Estimated'])
    print(url)
    response = requests.get(url, headers=headers)
    # print(response.content.decode())
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve the webpage")
        html_content = ""

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    script_text = None
    for script in soup.find_all("script"):
        if 'trackpollBootstrap' in script.text:
            script_text = script.text
            break

    # Assuming script_text contains the JavaScript variable assignment for trackpollBootstrap
    start = script_text.find('{')  # Find the start of the JSON object
    end = script_text.rfind('}')  # Find the end of the JSON object
    json_text = script_text[start:end + 1]  # Slice the JSON string

    # Convert the JSON string to a Python dictionary
    data = json.loads(json_text)
    # print(data)
    flights = data['flights']
    # Create a timedelta of 2 hours and 10 minutes
    time_increment = timedelta(hours=2, minutes=10)
    # Extracting terminal information
    for flight_id, flight_info in flights.items():
        try:
            flights = flight_info['activityLog']['flights']
            for flight in flights:
                flightId = flight['flightId'].split('-')
                destination_terminal = flight['destination'].get('terminal', 'No terminal info')
                iata = flight['destination'].get('iata', 'No iata info')
                est = flight['landingTimes'].get('estimated', 'No landing time')
                sch = flight['landingTimes'].get('scheduled', 'No schedule info')
                est = (datetime.utcfromtimestamp(est)+time_increment).astimezone(pytz.timezone('Europe/Berlin')).strftime('%H:%M')
                sched = (datetime.utcfromtimestamp(sch)+time_increment).astimezone(pytz.timezone('Europe/Berlin')).strftime('%H:%M')
                date = (datetime.utcfromtimestamp(sch)).astimezone(pytz.timezone('Europe/Berlin')).strftime('%d')
                if date == '{:02d}'.format(int(day)): #  todo: day
                    print(sch)
                    flight_data = [flightId[0], iata, destination_terminal, sched, est]
                    flight_data = pd.Series([f"{iata}-T{destination_terminal}", f"{sched}-{est}"],
                                            index=['Terminal', 'Estimated'])
                    print(flight_data)
        except Exception as e:
            print(f'Error in {e}')

    print(len(flight_data))
    return flight_data


def get_fra_flightinfo(flightnumber):
    url = f"https://airportinfo.live/arrivals/fra/airport-frankfurt"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    print(url)
    # The data you want to send with the form
    data = {
        'h': '18'
    }
    response = requests.get(url, headers=headers, data=data)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve the webpage")
        html_content = ""

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    script_text = []
    for script in soup.find_all("tr", class_="Frankfurt-arrivals"):
        script_text.append(script)

    for row in script_text:
        print(f"- {row}\t")
        values = [td.get_text() for td in row.find_all('td')]
        if 'LH' in values[0]:
            print(f"Flight# {values[0]} - {values[1]} - {values[4]} - {values[4][5:10]} - {values[4][10:12]} - {values[5]} ")

    return flightnumber


def split_flight_number(flight_number):
    # Regular expression to find groups of letters and numbers
    match = re.match(r"([a-zA-Z]+)(\s*)(\d+)", flight_number.replace(" ", ""))
    if match:
        # Extract the airline code and the numeric part
        airline_code = match.group(1)
        flight_number = match.group(3)
        return airline_code, flight_number
    return None, None


def convert_flight_number_to_icao(flight_number):
    try:
        # Mapping from IATA code to ICAO code
        iata_to_icao = {
            'BA': 'BAW',  # British Airways
            'AF': 'AFR',  # Air France
            'LH': 'DLH',  # Lufthansa
            'UX': 'AEA',  # Air Europe
            'FI': 'ICE',  # Icelandair
            'EI': 'EIN',  # Aer Lingus
            'EY': 'EIN',
            'EN': 'DLY',  # Air Dolomiti
            'OU': 'CTN',  # Croatia Airlines
            'LY': 'ELY',  # El Al
            'RO': 'ROT',  # Tarom
            'IB': 'IBE',  # Iberia
            'TK': 'THY',  # Iberia
            # Add more mappings as needed
        }

        # Split the input to get the IATA code and flight number
        parts = split_flight_number(flight_number)
        if len(parts) != 2:
            return flight_number

        iata_code, number = parts

        # Convert the flight number part by removing leading zeros
        number = number.lstrip('0')

        # Get the ICAO code from the mapping
        icao_code = iata_to_icao.get(iata_code.upper())
        if not icao_code:
            return flight_number

        # Create the ICAO flight number
        icao_flight_number = f"{icao_code}{number}"
    except Exception as e:
        print(e)
        return flight_number

    return icao_flight_number


def apply_flight_number(row):
    df_flight = pd.read_excel('flights.xlsx')
    df_trains = pd.read_excel('trains.xlsx')
    df_flight = pd.concat([df_flight, df_trains], ignore_index=True)
    flightnumber = row['Flight #']
    day = row['Arrival Date']

    filtered_df = df_flight[(df_flight['Flight #'] == flightnumber) & (df_flight['Arrival Date'] == day)]
    if not filtered_df.empty:
        # print(filtered_df[['Terminal', 'Estimated']].iloc[0])
        return filtered_df[['Terminal', 'Estimated']].iloc[0]
    else:
        print("Skip: " + str(flightnumber))
        return [None, None]

    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    return [None, None]


if __name__ == '__main__':
    data = {
        'Flight #': ['DLH1341'],
        'Arrival Date': [10],
        'Terminal': [2],
        'Estimated': [3],
    }
    df = pd.DataFrame(data)
    df[['Terminal', 'Estimated']] = df.apply(get_flightinfo, axis=1)
    # df[['Terminal', 'Estimated']] = df.apply(apply_flight_number, axis=1)
    print(df)
