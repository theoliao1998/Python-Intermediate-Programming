import requests
import json
import html
from bs4 import BeautifulSoup
from requests_html import HTMLSession

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

url_loc = "https://openflights.org/html/apsearch"
header = {'User-agent': 'Mozilla/5.0'}

def get_loc(code):
    if code in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[code]
    
    session = HTMLSession()
    r = session.get(url_loc)
    #r.html.render()
    script = """
       () => {
                  document.querySelectorAll("input[name='iata']")[0].value = '""" + code + """';
                  document.querySelectorAll("input[value='Search']")[0].click();
                  let time = 1;
                  setTimeout(function(){document.querySelectorAll("input[value='Load']")[0].click();}, 200);
                  setTimeout(function(){var node1 = document.createElement("LI");var node2 = document.createElement("LI");
                  node1.setAttribute("id", "x_val"); node2.setAttribute("id", "y_val");
                  var textnode1 = document.createTextNode(document.querySelectorAll("input[name='x']")[0].value);
                  node1.appendChild(textnode1);
                  var textnode2 = document.createTextNode(document.querySelectorAll("input[name='y']")[0].value);
                  node2.appendChild(textnode2);
                  document.querySelector("body").appendChild(node1);document.querySelector("body").appendChild(node2);
                  }, 400);
        }
    """
    r.html.render(script=script, sleep=1, keep_page=True)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    CACHE_DICTION[code] = [soup.find('li',{'id':'x_val'}).string, soup.find('li',{'id':'y_val'}).string]
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close()
    return CACHE_DICTION[code]