# SI507-Final
SI507 Final Project - Flight Insight

## Data Source
* US airport information crawled from https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States and its linked-to pages
* A list of top 100 airports in north America scrawled from https://www.flightsfrom.com/top-100-airports-in-north-america  
* Detailed airports location information a from https://github.com/mwgg/Airports
* Travelpayouts Data API https://support.travelpayouts.com/hc/en-us/articles/203956163-Travel-insights-with-Travelpayouts-Data-API

## Other files needed
Besides all the files provided here, another file called secret.py is also needed which should contain the client key of the api.
![home](https://user-images.githubusercontent.com/53862461/70453458-ca41e280-1a76-11ea-879d-05883ba93dee.png)

## Usages
* clone the repo  
* add secret.py containing client key
* set up a vertual environment and use `pip install -r requirements.txt` to install all the packages needed  
* run `python3 flightapp.py`  
* open http://localhost:5000/ or http://127.0.0.1:5000/, and it should be the home page
![home](https://user-images.githubusercontent.com/53862461/70448561-88ad3980-1a6e-11ea-95c5-ccd2a73e4a6d.png)  
* click start button, then you could choose the state of origin airport.
![home](https://user-images.githubusercontent.com/53862461/70448721-c90cb780-1a6e-11ea-9a69-c6e8cd8cda78.png)
* click the link on the state name, a map of all the busy commercial airports (from https://www.flightsfrom.com/top-100-airports-in-north-america) in that state will be shown in a new tab
![home](https://user-images.githubusercontent.com/53862461/70449069-57813900-1a6f-11ea-86ac-4beabc25b8bd.png)
* further choose an airport within the state (with the airport map poped in a new tab if one clicks the link on the airport name)
![home](https://user-images.githubusercontent.com/53862461/70449427-f9088a80-1a6f-11ea-8170-0dda02d3b3cc.png)
![home](https://user-images.githubusercontent.com/53862461/70449351-d37b8100-1a6f-11ea-8377-651a88e33bcd.png)
* similarly choose the distination state and then airport
* choose the month of the flight and how the data are ordered
![home](https://user-images.githubusercontent.com/53862461/70449641-50a6f600-1a70-11ea-8c9e-9d4dbddb07f6.png)
* click search button and then all the relevant found data about people's searching flights in recent 48 hrs will be shown in a table in the chosen order
![home](https://user-images.githubusercontent.com/53862461/70449924-d4f97900-1a70-11ea-9266-1b0ffa726f74.png)
* click the "Price Trending" link, and the trending of lowest prices based on the found data will be visualized in a new tab
![home](https://user-images.githubusercontent.com/53862461/70450229-5c46ec80-1a71-11ea-920e-88e6a58422f4.png)
* click the "Popularity Trending" link, and the trending of popularity based on the found data will be visualized in a new tab
![home](https://user-images.githubusercontent.com/53862461/70450519-df684280-1a71-11ea-96ad-826b3eefdee2.png)
* click the "Another search" link to have another search  

## Code structure
* Basically, this is a mini webapp with no models used. 
* The views are coded as html templates in the folder templates.
* The controllers are coded in flightapp.py, which use functions from data.py to obtain data.
* Data retrievation and processing are completed in data.py     
    * init_db() initialize the database with three tables used to store data for states, airports, and flights  
    * insert_airports_data() is used to insert all data about US airports from airports.json to the States and Airports table of the database. Meanwhile, data about the airports scrawled from websites will also be stored 
    * get_states() parses data crawled from https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States and gives all states  
    * get_airports(state) parses data crawled from linked pages to https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States and gives detailed information of the airports in the chosen state  
    * get_data(origin,destination,month,order) obtain data from the api if the request is not cached, insert them to the database, and then query data in the desired order.
    * ...
* There's also a test file test.py which provides some basic tests.
