import requests
import json
import secret
import plotly
import plotly.graph_objs as go

MAPBOX_TOKEN = secret.MAPBOX_TOKEN

base_url_venure = "https://api.foursquare.com/v2/venues/explore"
base_url = "https://api.foursquare.com/v2/venues/"

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}={}".format(k, params[k]))
    return baseurl + "?" + "&".join(res)

def make_request_using_cache(baseurl, params):
    
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION,indent=2)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]





# -----------------------------------------------------------------------------

# ----------------------------------------------
# Part 1: Get photo information 
# ----------------------------------------------
print("----------------Part1--------------------")
# city = str(input("In what city do you want to search: "))
# type = str(input("What kind of place are you looking for: "))
city = "Ann Arbor"
type = "coffee shop"
lat_vals = []
lon_vals = []
text_vals = []
params_venue = {"client_id":secret.client_id, "client_secret":secret.client_secret, "near":city, "query":type, "v":'20191029', "limit":25}
params_photo = {"client_id":secret.client_id, "client_secret":secret.client_secret, "v":'20180322'}
for item in make_request_using_cache(base_url_venure,params_venue)["response"]["groups"][0]["items"]:
    lat_vals.append(item["venue"]["location"]["lat"])
    lon_vals.append(item["venue"]["location"]["lng"])
    text_vals.append(item["venue"]["name"])
    print("Venue: "+item["venue"]["name"])
    print("Address: "+item["venue"]["location"]["address"]+", "+item["venue"]["location"]["city"]+", "+ \
        item["venue"]["location"]["state"]+" "+item["venue"]["location"]["postalCode"])
    base_url_photo = base_url+item["venue"]["id"]+"/photos"
    for photo in make_request_using_cache(base_url_photo,params_photo)["response"]["photos"]["items"]:
        print("Photo id: "+photo["id"]+"\n")
        photo_url = photo["prefix"]+"original"+photo["suffix"]
        text_vals[-1] +="<br><a href='"+photo_url+"' style='color:white'>"+photo_url +"</a>"

# ----------------------------------------------
# Part 2: Map data onto Plotly
# ----------------------------------------------



layout = dict(
    autosize=True,
    showlegend = False,

    mapbox=dict(
        accesstoken=secret.MAPBOX_TOKEN,
        bearing=0,
        center=dict(
            lat=(float(min(lat_vals))+float(max(lat_vals)))/2,
            lon=(float(min(lon_vals))+float(max(lon_vals)))/2,
        ),
        pitch=0,
        zoom=12,
      ),
)

fig = go.Figure(data=go.Scattermapbox(
    lon = lon_vals,
    lat = lat_vals,
    text = text_vals,
    mode = 'markers',
    marker_color = 'blue',
    ))

fig.update_layout(layout)
fig.show()
