import requests
import json
import webbrowser

class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", json=None):
        if not json:
            self.title = title
            self.author = author
            self.release_year = release_year
        else:
            self.title = json["trackName"] if "trackName" in json else json["collectionName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"][:4]

    def __str__(self):
        return self.title + " by " + self.author + " ("+self.release_year+")"

    def __len__(self):
        return 0

## Other classes, functions, etc. should go here

class Song(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year",album="No Album",
                genre="No Genre", track_length=0,json=None):
        super().__init__(title,author,release_year,json)
        if not json:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.album = json["collectionCensoredName"]
            self.genre = json["primaryGenreName"]
            self.track_length = json["trackTimeMillis"]

    def __str__(self):
        return super().__str__() + " [" + self.genre + "]"

    def __len__(self):
        return self.track_length / 1000

class Movie(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year",rating="No Rating",
                movie_length=0,json=None):
        super().__init__(title,author,release_year,json)
        if not json:
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]

    def __str__(self):
        return super().__str__() + " [" + self.rating + "]"

    def __len__(self):
        return int(round(self.movie_length / 1000 /60))


#params = {"term":"Spider","limit":30}
baseurl = "https://itunes.apple.com/search?parameterkeyvalue"

def fetchData(params):
    """
    This program fetches data from itunes and create media, song, and movie objects accordingly
    Other types of fecthed results will be ignored
    The count of all fetched results and the created objects will be returned
    """
    resp = json.loads(requests.get(baseurl,params).text)
    print(requests.get(baseurl,params).url)
    res = resp["results"]
    other_medias = []
    songs = []
    movies = []
    urls = [[],[],[]]
    for data in res:
        if "kind" in data and data["kind"] == "song":
            songs.append(Song(json=data))
            urls[0].append(data["trackViewUrl"])
        elif "kind" in data and data["kind"] == "feature-movie":
            movies.append(Movie(json = data))
            urls[1].append(data["trackViewUrl"])
        else:
            other_medias.append(Media(json = data))
            urls[2].append(data["collectionViewUrl"])
    
    return resp,songs,movies,other_medias,urls

def interactiveSearch(init=True, query=None):
    if init:
        query = str(input('Enter a search term, or "exit" to quit: '))
    
    if query == "exit":
        print("\nBye!")
        return

    params = {"term":query}
    res = fetchData(params)
    i = 0
    
    print("\nSONGS")
    if not res[1]:
        print("No songs found!")
    for elem in res[1]:
        i += 1
        print(repr(i)+" "+elem.__str__())
    
    print("\nMOVIES")
    if not res[2]:
        print("No movies found!")
        
    for elem in res[2]:
        i += 1
        print(repr(i)+" "+elem.__str__())
        
    s = i
        
    print("\nOTHER MEDIA")
    if not res[3]:
        print("No other media found!")
    for elem in res[3]:
        i += 1
        print(repr(i)+" "+elem.__str__())
    
    urls = res[-1][0] + res[-1][1] + res[-1][2]
    while True:
        query = str(input('\nEnter a number for more info, or another search term, or exit: '))
        if query.isdigit() and int(query)>=0 and int(query)<=i:
            url = urls[int(query)-1]
            print("\nLaunching "+url + " in web browser...")
            webbrowser.open(url)
        else:
            interactiveSearch(False,query)


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    interactiveSearch()
