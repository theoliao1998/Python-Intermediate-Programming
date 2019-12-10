import requests
import json
import html
from bs4 import BeautifulSoup
import plotly.graph_objs as go
import sqlite3 as sqlite
from pathlib import Path
from statistics import mean
from secret import key


DBNAME = 'airports.db'
AIRPORTSJSON = 'airports.json'
INSULAR_AREAS = {'#American_Samoa','#Guam', '#Northern_Mariana_Islands', '#Puerto_Rico', '#U.S._Virgin_Islands'}	
INSULAR_AIRPORTS = {'NSTU', 'PGUM', 'PGSN', 'PGRO', 'PGWT', 'TJBQ', 'TJRV', 'TJCP', 'TJPS', 'TJSJ', 'TJIG', 'TJVQ', 'TIST', 'TISX'}
url_prefix = "https://en.wikipedia.org/wiki/List_of_airports_in_"
api_url = "https://api.travelpayouts.com/v2/prices/latest"
busy_airports_url = "https://www.flightsfrom.com/top-100-airports-in-north-america"
consumer_key = key
header = {'User-agent': 'Mozilla/5.0'}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}={}".format(k, params[k]))
    return baseurl + "?" + "&".join(res)

def make_request_using_cache(url, header,params=None):
    unique_ident = params_unique_combination(url,params) if params else url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers=header,params=params)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

AIRPORTS_FNAME = 'airports.json'
try:
    airport_file = open(AIRPORTS_FNAME, 'r')
    airports_data = airport_file.read()
    AIRPORTS_DICTION = json.loads(airports_data)
    airport_file.close()

# if there was no file, no worries. There will be soon!
except:
    AIRPORTS_DICTION = {}

def get_busy_airports():
    text = make_request_using_cache(busy_airports_url,header)
    if not text:
        return set()
    soup = BeautifulSoup(text, 'html.parser')
    return {a['href'][1:] for a in soup.find(class_="hometoplist").find_all('a')}

busy_airports = get_busy_airports()


# Create tables
def init_db():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        CREATE TABLE IF NOT EXISTS 'States' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'raw' TEXT,
            'name' TEXT UNIQUE
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE IF NOT EXISTS 'Airports' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'ICAO' NCHAR(4) UNIQUE,
            'IATA' NCHAR(4),
            'name' TEXT,
            'lat' REAL,
            'lon' REAL,
            'state_id' INTEGER,    
            FOREIGN KEY (state_id) REFERENCES States(Id)
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE IF NOT EXISTS 'Flights' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'origin' INTEGER,
            'destination' INTEGER,
            'trip_class' INTEGER,
            'price' INTEGER,
            'date' TEXT,
            'duration' INTEGER,
            'transfers' INTEGER,
            FOREIGN KEY (origin) REFERENCES Airports(Id),
            FOREIGN KEY (destination) REFERENCES Airports(Id)
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def query(statement):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(statement)
    res = cur.fetchall()
    conn.close()
    return res

def get_url(state):
    state = state.replace("-","_")
    if state == "Georgia": state += "_(U.S._state)"
    return url_prefix+state

# Load data
def insert_airports_data():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()

    # if table is not empty, don't need to insert
    # if len(cur.execute('SELECT * FROM "Countries" LIMIT 1').fetchall()): return
    
    with open(AIRPORTSJSON, "r", encoding='utf-8') as content:
        data = json.load(content)
    
    for a in data:
        if data[a]["country"] == "US":
            if get_url(data[a]["state"]) not in CACHE_DICTION:
                raw = make_request_using_cache(get_url(data[a]["state"]),header)
                insertion_state = (None,raw,data[a]["state"])
                statement = 'INSERT INTO "States" '
                statement += 'VALUES (?, ?, ?)'
                cur.execute(statement, insertion_state)

            if data[a]["iata"] in busy_airports:
                insertion_airport = (None,data[a]["icao"], data[a]["iata"], data[a]["name"], data[a]["lat"], data[a]["lon"], data[a]["state"])
                statement = 'INSERT INTO "Airports" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, (SELECT Id FROM "States" WHERE name = ?))'
                cur.execute(statement, insertion_airport)
    
    raw = make_request_using_cache(url_prefix+"the_United_States",header)
    insertion_state = (None,raw,"All")
    statement = 'INSERT INTO "States" '
    statement += 'VALUES (?, ?, ?)'
    cur.execute(statement, insertion_state)
                
    conn.commit()
    conn.close()


# init db
db_file = Path(DBNAME)
if not db_file.is_file():
    init_db()
    insert_airports_data()


def get_states():
    text = query("SELECT raw FROM States WHERE name='All'")[0][0]
    if not text:
        return []
    state_soup = BeautifulSoup(text, 'html.parser')
    states = [html.unescape(a.string) for a in state_soup.find(class_="toccolours").find_all('a') if a['href'] not in INSULAR_AREAS]
    mid = len(states) // 2
    return states[:mid], states[mid:]


def get_airports(state):
    text =  query("SELECT raw FROM States WHERE name='{}'".format(state))[0][0] #make_request_using_cache(url_prefix+state,header)
    if not text:
        return []
    soup = BeautifulSoup(text, 'html.parser')
    airports = soup.find("table",class_="wikitable sortable").find_all('tr')
    start = 2
    try:
        end = airports.index(soup.find("table",class_="wikitable sortable").find_all('tr',{"style":"background:#CCCCCC;"})[1])
    except:
        end = airports.index(soup.find("table",class_="wikitable sortable").find_all('tr',{"style":"background:#ccc;"})[1])

    return [(tr.find_all('td')[0].a.string, tr.find_all('td')[2].string, tr.find_all('td')[4].a.string) for tr in airports[start:end]\
        if tr.find_all('td')[2].string and tr.find_all('td')[2].string.replace('\n','') in busy_airports]


def get_loc(code):
    res = query("SELECT lat, lon FROM Airports WHERE IATA='{}'".format(code))
    return res[0] if res else None

def plot_state_airports(state):
    # print(state)
    codes = [airport[1].replace('\n','') for airport in get_airports(state) if get_loc(airport[1].replace('\n',''))]
    if not codes:
        return "<h1>Oops! There's no busy airport in this state.</h1>"

    locs = [get_loc(code) for code in codes]
    lat_vals = [float(loc[0]) for loc in locs]
    lon_vals = [float(loc[1]) for loc in locs]
    text_vals = [query("SELECT name FROM Airports WHERE IAtA='{}'".format(code))[0][0]+" ({})".format(code) for code in codes]
    center = (mean(lat_vals),mean(lon_vals))
    lat_axis = [center[0]-20 , center[0]+20]
    lon_axis = [center[1]-20 , center[1]+20]

    layout = dict(
        title = "Airports in {}".format(state),
        geo = dict(
            # scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(235, 189, 52)",
            subunitcolor = "rgb(17, 23, 31)",
            countrycolor = "rgb(100, 137, 217)",
            showlakes  = True,
            lakecolor = "rgb(52, 128, 235)",
            showocean = True,
            oceancolor = "rgb(52, 128, 235)",
            lataxis = {'range': lat_axis},
            lonaxis = {'range': lon_axis},
            center= {'lat': center[0], 'lon': center[1] },
            countrywidth = 3,
            subunitwidth = 3
        ))

    fig = go.Figure(data=go.Scattergeo(
        lon = lon_vals,
        lat = lat_vals,
        text = text_vals,
        mode = 'markers',
        marker_color = 'red',
        marker = {"symbol":"star", "size":15},
        showlegend=False
        ))

    fig.update_layout(layout)
    return fig.to_html(fig, include_plotlyjs=True,full_html=True)


def plot_airport(code):
    loc = get_loc(code)
    if not loc:
        return "<h1>Oops! Data missing...</h1>"

    lat_vals = [float(loc[0])]
    lon_vals = [float(loc[1])]
    text_vals = [query("SELECT name FROM Airports WHERE IAtA='{}'".format(code))[0][0]+" ({})".format(code)]
    
    
    lat_axis = [lat_vals[0]-20 , lat_vals[0]+20]
    lon_axis = [lon_vals[0]-20 , lon_vals[0]+20]

    layout = dict(
        title = text_vals[0],
        geo = dict(
            # scope='usa',
            projection=dict( type='albers usa' ) if code not in INSULAR_AIRPORTS else dict( type='equirectangular' ),
            showland = True,
            landcolor = "rgb(235, 189, 52)",
            subunitcolor = "rgb(17, 23, 31)",
            countrycolor = "rgb(100, 137, 217)",
            showlakes  = True,
            lakecolor = "rgb(52, 128, 235)",
            showocean = True,
            oceancolor = "rgb(52, 128, 235)",
            lataxis = {'range': lat_axis},
            lonaxis = {'range': lon_axis},
            center= {'lat': lat_vals[0], 'lon': lon_vals[0] },
            countrywidth = 3,
            subunitwidth = 3
        ))

    fig = go.Figure(data=go.Scattergeo(
        lon = lon_vals,
        lat = lat_vals,
        text = text_vals,
        mode = 'markers',
        marker_color = 'red',
        marker = {"symbol":"star", "size":15},
        showlegend=False
        ))

    fig.update_layout(layout)
    # fig.show()
    return fig.to_html(fig, include_plotlyjs=True,full_html=True)


def insert_flight_data(data, origin, dest):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()

    # if table is not empty, don't need to insert
    # if len(cur.execute('SELECT * FROM "Countries" LIMIT 1').fetchall()): return
    
    for d in data:
        insertion = (None,origin,dest,d['trip_class'],d['value'],d['depart_date'],d['duration'],d['number_of_changes'])
        statement = 'INSERT INTO "Flights" '
        statement += "VALUES (?, (SELECT Id FROM Airports WHERE IATA=?), (SELECT Id FROM Airports WHERE IATA=?), ?, ?, ?, ?, ?)"
        cur.execute(statement, insertion)
                
    conn.commit()
    conn.close()

def get_data(origin,destination,month,order):
    params={'token':consumer_key,'currency':'usd','origin':origin,'destination':destination,'beginning_of_period':month+'-01','period_type':'month',"one-way":"true","limit":100}
    url = params_unique_combination(api_url,params)
    # if url in CACHE_DICTION: print(CACHE_DICTION[url])
    if url not in CACHE_DICTION or ('success' not in json.loads(CACHE_DICTION[url])) or (not json.loads(CACHE_DICTION[url])['success']) :
        resp = json.loads(make_request_using_cache(url,header))
        if 'success' in resp and resp['success']: insert_flight_data(resp['data'],origin,destination)

    return query("""SELECT trip_class, price, date, duration, transfers 
        FROM Flights AS f JOIN Airports AS a1 ON f.origin=a1.Id JOIN Airports AS a2 ON f.destination=a2.Id  
        WHERE a1.IATA='{}' AND a2.IATA='{}' AND date LIKE '{}%' ORDER BY {}""".format(origin,destination,month,order))

# print(get_data('LAX','LGA','2019-12','price'))

def plot_price_trending(origin,destination,month):
    get_data(origin,destination,month,'date')
    data = query("""SELECT date, min(price) 
        FROM Flights AS f JOIN Airports AS a1 ON f.origin=a1.Id JOIN Airports AS a2 ON f.destination=a2.Id  
        WHERE a1.IATA='{}' AND a2.IATA='{}' AND date LIKE '{}%' GROUP BY date""".format(origin,destination,month))

    dates = [d[0] for d in data]
    prices = [d[1] for d in data]

    layout = go.Layout(
        title='The trending of lowest prices from {} to {} in {}'.format(origin,destination,month),
    )

    fig = go.Figure(data = go.Bar(
            x=dates,
            y=prices
    ), layout=layout)
    
    return fig.to_html(fig, include_plotlyjs=True,full_html=True)


def plot_popularity_trending(origin,destination,month):
    get_data(origin,destination,month,'date')
    data = query("""SELECT date, COUNT(*) 
        FROM Flights AS f JOIN Airports AS a1 ON f.origin=a1.Id JOIN Airports AS a2 ON f.destination=a2.Id  
        WHERE a1.IATA='{}' AND a2.IATA='{}' AND date LIKE '{}%' GROUP BY date""".format(origin,destination,month))

    dates = [d[0] for d in data]
    popularity = [d[1] for d in data]

    layout = go.Layout(
        title='The trending of popularity from {} to {} in {}'.format(origin,destination,month),
    )

    fig = go.Figure(data = go.Bar(
            x=dates,
            y=popularity
    ), layout=layout)
    
    return fig.to_html(fig, include_plotlyjs=True,full_html=True)

# plot_price_trending("LAX","LGA",'2019-12')

