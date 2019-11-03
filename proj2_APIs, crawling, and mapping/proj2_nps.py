## proj_nps.py
## Skeleton for Project 2 for SI 507
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key
import requests
import json
from bs4 import BeautifulSoup
import plotly.graph_objs as go

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

state_name = {}

baseurl = "https://www.nps.gov"
textSearch_baseurl = "https://maps.googleapis.com/maps/api/place/textsearch/json"
nearbySearch_baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
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
        if resp.status_code != 200:
            return None
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite():
    def __init__(self, type, name, desc=None, url=None):
        self.type = type if type else ""
        self.name = name
        self.description = desc
        self.url = url
        if url:
            soup = BeautifulSoup(make_request_using_cache(url,header), 'html.parser')
            street_address = soup.find(class_="street-address")
            if street_address:
                self.address_street = street_address.contents[0].strip().replace("<br>","")
            elif soup.find("span",{"itemprop":"postOfficeBoxNumber"}):
                self.address_street ="P.O. Box"+soup.find("span",{"itemprop":"postOfficeBoxNumber"}).string.strip()
            else:
                self.url = None
                return
            
            self.address_city = soup.find("span",{"itemprop":"addressLocality"}).string.strip()
            self.address_state = soup.find("span",{"itemprop":"addressRegion"}).string.strip()
            self.address_zip = soup.find("span",{"itemprop":"postalCode"}).string.strip()
    
    def __str__(self):
        full_name = self.name+" ("+self.type+")" if self.type else self.name
        return full_name+": "+self.address_street+", "+self.address_city+", "+self.address_state+" "+self.address_zip \
            if self.url else full_name

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name,location=None):
        self.name = name
        self.location = location
    
    def __str__(self):
        return self.name

## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: list of all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def get_sites_for_state(state_abbr):
    state_abbr = state_abbr.lower()
    state_url = baseurl + "/state/" + state_abbr
    state_text = make_request_using_cache(state_url,header)
    if not state_text:
        return []
    state_soup = BeautifulSoup(state_text, 'html.parser')
    state_name[state_abbr] = state_soup.find(class_="page-title").string.strip()
    sites = state_soup.find(id="list_parks").find_all(class_="clearfix")
    return [NationalSite(li.div.h2.string,
                        li.div.h3.a.string,
                        li.div.p.string,
                        baseurl + li.div.h3.a['href'])  for li in sites]


def get_site_location(national_site):
    query = national_site.name+" "+national_site.type if national_site.type else national_site.name
    params_ts = {"query":query, "key":google_places_key}
    resp_ts = json.loads(make_request_using_cache(textSearch_baseurl,header=header,params=params_ts))
    return resp_ts["results"][0]["geometry"]["location"] if resp_ts["results"] else None


## Must return the list of NearbyPlaces for the specific NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(national_site):
    location = get_site_location(national_site)
    if not location:
        return []
    params_ns = {"key":google_places_key,"location":str(location["lat"])+","+str(location["lng"]),"radius":10000}
    resp_ns = json.loads(make_request_using_cache(nearbySearch_baseurl,header=header,params=params_ns))
    return [NearbyPlace(res["name"],res["geometry"]["location"]) for res in resp_ns["results"]]


def plot_sites(sites,nearby=None):
    lat_vals = []
    lon_vals = []
    text_vals = []
    for s in sites:
        location = s.location if nearby else get_site_location(s)
        if location:
            lat_vals.append(float(location["lat"]))
            lon_vals.append(float(location["lng"]))
            text_vals.append(str(s.name))
    
    min_lat = float(min(lat_vals))
    max_lat = float(max(lat_vals))
    min_lon = float(min(lon_vals))
    max_lon = float(max(lon_vals))
    pad_lat = (max_lat-min_lat)/10
    pad_lon = (max_lon-min_lon)/10

    lat_axis = [min_lat-pad_lat , max_lat+pad_lat]
    lon_axis = [min_lon-pad_lon , max_lon+pad_lon]

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    if nearby:
        title = "Places near "+nearby['name']
        if nearby["type"]:
            title += " "+nearby['type']
    else:
        title = "National Sites in "+ state_name[sites[0].address_state.lower()]

    layout = dict(
        title = title,
        geo = dict(
            scope='usa',
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
            center= {'lat': center_lat, 'lon': center_lon },
            countrywidth = 3,
            subunitwidth = 3
        ))

    fig = go.Figure(data=go.Scattergeo(
        lon = lon_vals,
        lat = lat_vals,
        text = text_vals,
        mode = 'markers',
        marker_color = 'red' if nearby else 'purple',
        marker = {"size":5} if nearby else {"symbol":"star", "size":15},
        showlegend=False
        ))
    
    if nearby:
        fig.add_scattergeo(
            lon = [nearby['location']['lng']],
            lat = [nearby['location']['lat']],
            text = [str(nearby['name'])],
            mode = 'markers',
            marker_color = 'purple',
            marker = {"symbol":"star", "size":15},
            showlegend=False
            )

    fig.update_layout(layout)
    fig.show()


## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_sites_for_state(state_abbr):
    sites = get_sites_for_state(state_abbr)
    plot_sites(sites)


## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_nearby_for_site(site_object):
    sites = get_nearby_places_for_site(site_object)
    location = get_site_location(site_object)
    plot_sites(sites,{'location':location,'name':site_object.name,'type':site_object.type})

current_results = {}

def commands():
    command = str(input('Enter command (or "help" for options): '))
    if command == "help":
        print("""
    list <stateabbr>
        available anytime
        lists all National Sites in a state
        valid inputs: a two-letter state abbreviation
    nearby <result_number>
        available only if there is an active result set
        lists all Places near a given result
        valid input for <result number>: an integer 1-len(result_set_size)
    map
        available only if there is an active result set
        displays the current results on a map
    exit
        exits the program
    help
        lists available commands (these instructions)
""")
    elif command == "exit":
        print("Bye")
        return
    elif command == "map":
        if not current_results:
            print("Not available since there is no active result set")
        elif current_results["nearby"]:
            plot_nearby_for_site(current_results["nearby"])
        else:
            plot_sites_for_state(current_results["state"])
    else:
        command = command.split()
        if len(command) != 2:
            print("Invalid command")
        elif command[0] == "nearby":
            if current_results and current_results["state"]:
                if command[1].isdigit() and int(command[1])>0 and int(command[1])<=len(current_results["results"]):
                    current_results["nearby"] = current_results["results"][int(command[1])-1]
                    current_results["state"] = None
                    current_results["results"] = get_nearby_places_for_site(current_results["nearby"])
                    print("Places near "+current_results["nearby"].name+" "+current_results["nearby"].type+"\n")
                    for i in range(len(current_results["results"])):
                        print(str(i+1)+" "+current_results["results"][i].__str__())
                    print("""
Type "map" to map the list of national sites, or "list <state>" to do a search for another state:
""")
                else:
                    print("Invalid result-number")
            else:
                print("Not available since there is no active result set of national sites")
        elif command[0] == "list":
            resp = get_sites_for_state(command[1])
            if not resp:
                print("Invalid state-abbreviation")
            else:
                current_results["nearby"] = None
                current_results["state"] = command[1].lower()
                current_results["results"] = resp
                print("National Sites in "+state_name[current_results["state"]]+"\n")
                for i in range(len(current_results["results"])):
                     print(str(i+1)+" "+current_results["results"][i].__str__())
                print("""
Type "nearby <result number>" to search for places near one of the national sites above, 
"map" to map the list of national sites, or "list <state>" to do a search for another state:
""")
        else:
            print("Invalid command")

    commands()


if __name__ == "__main__":
    commands()
