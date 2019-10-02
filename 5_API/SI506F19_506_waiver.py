# import statements -- do not change
import json
import requests



############

## IMPORTANT NOTES: This assignment, depending upon your setup, is VERY UNLIKELY to work if you do not run it via the command prompt (Git Bash or Terminal, etc). YOU MUST RUN THIS IN PYTHON 3, NOT PYTHON 2.

# If you cannot see full lines of some of the instructions, you'll want to turn the
# "soft wrap" feature on in your text editor. In Atom, that's View -> Toggle Soft
# Wrap. There are similar instructions for any other text editor you can look up.

## Remember: run your program early and often to determine what it is doing and whether it is working as you expect it to! DO NOT turn your program in without first running it to make sure that all of the test output is shown and it runs properly.

## You should NOT be writing any calls to input.
## If your program does not run fully when we go to run it you will NOT pass the waiver. We are running these automatically with test files and inspecting them. Your program should not require any user input or user actions besides running the program.

## When you run this program, you will see the print statements provided for you.

## To run the tests for this file and see which are passing (they will show you Python unit test output), run the included test file in the same directory as all the rest of these files: f19_506waiver_tests.py
## If your program passes all of the tests, you will pass the waiver.

#########


## [PROBLEM 1] - Open a Flickr photo file as a Python dictionary.
print("\n***** PROBLEM 1 *****\n") # (Printed statements like this one throughout the problem set are provided to help you figure out where things are when you see output. You should leave them alone.)

## There are tests for this problem.

## We have provided a sample dictionary representing 1 Flickr photo in the format that Flickr returns it, saved in a JSON file, called sample_diction.json.

## Write code to open the file and load its contents as a Python dictionary into the variable sample_photo_rep. Then close the file (that'll keep you from running into easily-avoidable errors later on!).

## (You may also find it useful, for later in the problem set, to open the file "sample_diction.json" in a text editor, or copy and paste its contents into http://www.jsoneditoronline.org/ to see what the nested data in this dictionary will be structured like.)

with open('sample_diction.json', 'r') as f1:
    sample_photo_rep = json.load(f1)



## [PROBLEM 2] - Get and paste in a Flickr API key
print("\n***** PROBLEM 2 *****\n")

## There are no tests for this problem, but the rest of the assignment will not work if you don't complete it!

## You'll need an API key to access Flickr. 
## And you will need a Yahoo! account to log in to Flickr, so that you can get this API key.
## This Yahoo! account does not need to be a "real" account that you will use for anything else besides this, and you do not need to use your real name for it if you do not want to.

## Follow the instructions at:
## https://www.flickr.com/services/api/misc.api_keys.html
## to get a key for the Flickr API, so that you can get data from Flickr and paste it below, inside the quotes.

FLICKR_KEY = "96f96eb6aa17efff6e78768e2d4e3913" # paste your flickr API key here, between those quotation marks, such that the variable flickr_key will contain a string.


## DO NOT CHANGE ANYTHING ELSE ABOUT THE CODE HERE IN THIS PROBLEM 2.
## Normally you should not share API keys with others. But it is necessary to do this 
## exercise. We will not use it for anything nefarious.
## You can also regenerate the key (but do NOT regenerate it until after you get your waiver results!!!)
if FLICKR_KEY == "" or not FLICKR_KEY:
    print("Your flickr key is missing from the file. Enter your flickr key where directed and save the program!")
    exit()
##### END PROVIDED CODE


## [PROBLEM 3] - Get a list of tags from a dictionary which represents a photo
print("\n***** PROBLEM 3 *****\n")

## There are tests for this problem.

## The sample_photo_rep variable you defined back in Problem 1 should contain a complex Python object. It represents data about one single photo on Flickr.
## Write code to access the nested data inside sample_photo_rep to create a list of all of the tags of that photo.
## Save the list of tags in a variable called sample_tags_list.

## You will need to do a bunch of nested data investigation and nested iteration in order to complete this.
## Copying the contents of the sample_diction.json file into jsoneditoronline.org may help. Go slowly and step-by-step; understand, then extract, then understand the next bit...

## When you have completed this problem, the tags list in sample_tags_list should look like this: ['nature','mist','mountain']

## HINT: Check out the '_content' keys' values deep inside the nested dictionary... (Don't use the "raw" key. Look at the data and consider why not!)

sample_tags_list = [i['_content'] for i in sample_photo_rep['photo']['tags']['tag']]



## [PROBLEM 4] - Load a Flickr search response into a python dictionary, and then save a list of the corresponding photo IDs.
print("\n***** PROBLEM 4 *****\n")

## There are tests for this problem. It has 2 parts.

## We have also provided a file called sample_flickr_response.json.
## This file contains data that has been gotten from the Flickr API in response to a request for 25 photos tagged with the word "trees", but the data from the API has been altered slightly so that it is properly formatted in a JSON way (as you will do later).

## PART 1:
## Write code that will open the sample_flickr_response.json file and load the data inside that file into a variable called search_result_diction.

with open('sample_flickr_response.json', 'r') as f2:
    search_result_diction = json.load(f2)


## PART 2:
## The variable search_result_diction should now contain a very complex dictionary representing information about a bunch of photos that are tagged "trees". Each photo has an id.
## Write code to create a list of all of the photo ids from each photo included in search_result_diction, then save that list in a variable called sample_photo_ids.

sample_photo_ids = [i['id'] for i in search_result_diction['photos']['photo']]


## [PROBLEM 5] - Understand the caching approach used here, and then open a cache file.
print("\n***** PROBLEM 5 *****\n")

## There are tests for this problem.  But this code will work in conjunction with code you write later, so it can't all be tested until you've completed the whole assignment. In other words, it is possible (if unlikely) to pass the tests for this problem, but still have the code you write in this problem cause a difficulty for you. So take your time and be sure you understand what's happening here!

## We will be a using a process called caching, where we save a Flickr search under a unique identifier in a cache file. The general idea is to reduce calls to the Flickr API. 
## This process will work by associating a unique identifier string to each Flickr search. The program then checks whether the id is already in the cache file/dictionary. Only if the id is not in the cache file does the program make a request from the API.

## For this problem, you'll just write the code to open the cache file.
## In the next problem, you'll implement the caching process.

#### Don't change this line for now.
CACHE_FNAME = "waiver_cached_data.json" 
#### End non-changing code.
## If you save data in this file that is wrong/not working, not a problem: just delete the file from the folder, or rename it, and run this file again to try and fix the problem.

## Write code that uses a try/except statement to do the following:
## Open a json file with the CACHE_FNAME name.
## Read the file into a Python dictionary, saved in a variable called CACHE_DICTION
## Make sure you close the open file.
## If the above three steps don't work, create an empty dictionary called CACHE_DICTION.
## Translate the following English into code in order to set up a pattern so you can cache the data you get in this problem set.

try:
    f3 = open(CACHE_FNAME,'r')
    CACHE_DICTION = json.load(f3)
    f3.close()
except:
	CACHE_DICTION = {}



# In total, this should be about five or six lines of code. 
# We have also provided a file SAMPLE_waiver_cached_data.json, which is SIMILAR to what your code should generate in format, etc. (You may end up with much more data in your cache file, and you will definitely end up with different data in your cache file, which is just fine!)



## [PROBLEM 6] - Implement the caching process
print("\n***** PROBLEM 6 *****\n")

## There are tests for this problem.

## In this problem, you'll define a function to get data from Flickr which uses the caching framework described above. So it will only request data from the Flickr API if you have not already made the same request. See below for more detailed descriptions of the function's input, output, and what its behavior should be.

#### Utility function provided for your use here (do not change):
## This function creates the unique id to use in the caching process. It is similar in form to a REST API call, but has a slightly different syntax so we don't confuse it with a URL. Note that the function hides the API key that is required to query the Flickr API, but that you may not want to share with others who read your cache file.
## Use the example to understand what the format of this unique identifier is. Do not change the function code. 

def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

## Code provided to provide an example of the params_unique_combination function
pd = {}
pd["method"] = "flickr.photos.search"
pd["format"] = "json"
pd["api_key"] = FLICKR_KEY
pd["tags"] = "bells"
pd["tag_mode"] = "all"
pd["per_page"] = 112
print("params diction example", params_unique_combination("https://api.flickr.com/services/rest/", pd))
#### End non-changing code

## Now, define a function called get_flickr_data which accepts 2 inputs:
## - a REQUIRED parameter: any string representing a tag to search for on Flickr (e.g. if you wanted to search for data on photos tagged with "mountains", you would pass in "mountains" for this parameter)
## - an OPTIONAL parameter: whose default value is 50 (representing how many photos you want in your response data)
## The function should interact with the cache file to pull the Flickr data, if necessary, and then save it.

## The following is an EXTENDED description of what the function should do.

## (1) This function should use the provided utility function called params_unique_combination to get a unique identifier for the data request to the Flickr API.
## (2) The function should check whether or not the unique identifier for each request exists in your cache data, and if it does, should access that data.
## (3) If there is no such data in your cache, 
## (3a) The function should make a request to the Flickr Photos Search API for photos tagged with your input string. Your request should use the tag_mode "all" so that if your query string represents multiple tags, it will search for photos with ALL of those tags.
## (3b) It should modify the string that is returned from the Flickr API so that it is properly JSON formatted. (You want a version of the string without the first 14 characters or the very last character.)
## (3c) It should then load that modified string into a Python dictionary.
## (3d) The function should add the new dictionary of data to your cache dictionary, associated with the unique identifier key, and save all the data in the cache dictionary to your cache file!
## (4) The get_flickr_data function's RETURN VALUE, regardless of whether it got data from the cache, or made a new request and saved data to the cache, should be a big dictionary representing a bunch of search data from the Flickr Photos Search API.

## Hints: 
## API docs on this method are here: flickr.com/services/api/flickr.photos.search.html
## The base URL for the Flickr API is: "https://api.flickr.com/services/rest/"
## All Flickr API endpoints have the same base url, but different values of the "method" parameter. For the Photos Search API, that value should be "flickr.photos.search"
## Recall also that you have a variable FLICKR_KEY in this file which you should reuse in this function, since it is intended as a global variable for your whole program.
## The examples in the online textbook will be very helpful here.

def get_flickr_data(tags_string, number = 50):
    baseurl = "https://api.flickr.com/services/rest/"
    params_diction = {}  
    params_diction["format"] = "json"
    params_diction["method"] = "flickr.photos.search"
    params_diction["nojsoncallback"] = 1
    params_diction["per_page"] = number
    params_diction["api_key"] = FLICKR_KEY
    params_diction["tag_mode"] = "all"
    params_diction["tags"] = tags_string
    dr_id = params_unique_combination(baseurl, params_diction)   
    if dr_id in CACHE_DICTION:
        res = CACHE_DICTION[dr_id]
    else:
        flickr_resp = requests.get(baseurl, params = params_diction)
        res = json.loads(flickr_resp.text[14:-1])
        CACHE_DICTION[dr_id] = res
        fobj = open(CACHE_FNAME, "w")
        json.dump(CACHE_DICTION,fobj)
        fobj.close()

    return res
        





## [PROBLEM 7] - Use your caching process to do one search in Flickr
print("\n***** PROBLEM 7 *****\n")

## There are tests for this problem. Whether or not this works is also an additional test for your Problem 6, since you'll need to have correctly completed the function definition above to do this.

## Make an invocation to your get_flickr_data function with the input "mountains" (use the default second parameter). Save the result in the variable flickr_mountains_result. 

flickr_mountains_result = get_flickr_data('mountains')




## [PROBLEM 8] - Get photo IDs from a Flickr search.
print("\n***** PROBLEM 8 *****\n")

## There are tests for this problem.

## Remember the code you wrote in Problem 4? Modify that code slightly to get a list of all of the photo IDs from the flickr_mountains_result variable and save it in a variable photo_ids. 

## Your photo_ids variable should have 50 different photo ids, since your Flickr API response in Problem 7 should have made a request for data from 50 photos.


photo_ids = [i['id'] for i in flickr_mountains_result['photos']['photo']]




## [PROBLEM 9] - Use a caching process to search for and store information about specific photos
print("\n***** PROBLEM 9 *****\n")

## There are tests for this problem.

## Previously, you did a Flickr search using tags and cached the results. Here, instead of using tags, you'll query Flickr using photo IDs similar to the ones you found in Problem 8. You'll store the information in the same cache file used before, using a similar format for the unique identifier.
## You could use the list of IDs stored in the variable photo_ids. However, (in the next problem) we'll use the list saved in sample_photo_ids from Problem 4. This will allow us to make sure that the tests work, because you'll be working from data we've provided.

## First, take a look at another endpoint of the Flickr API, which you'll need for this problem:
## https://www.flickr.com/services/api/flickr.photos.getInfo.html

## Write a function called get_photo_data that takes 1 parameter: a photo id.
## This function should have the same structure as get_flickr_data from problem 6, except it should get information about the specified photo ID, rather than a tag search. 
## You should again use params_unique_combination to generate the unique identifier. Also, you can cache the results in the same cache file you already used.
## The get_photo_data function should return a complex dictionary that represents information about 1 photo on Flickr.


def get_photo_data(photo_id):
    baseurl = "https://api.flickr.com/services/rest/"
    params_diction = {}  
    params_diction["method"] = "flickr.photos.getInfo"
    params_diction["format"] = "json"
    params_diction["api_key"] = FLICKR_KEY
    params_diction["photo_id"] = photo_id
    dr_id = params_unique_combination(baseurl, params_diction)
    
    if dr_id in CACHE_DICTION:
        res = CACHE_DICTION[dr_id]
    else:
        flickr_resp = requests.get(baseurl, params = params_diction)
        res = json.loads(flickr_resp.text[14:-1])
        CACHE_DICTION[dr_id] = res
        fobj = open(CACHE_FNAME, "w")
        json.dump(CACHE_DICTION,fobj)
        fobj.close()

    return res





## The following two lines of code will invoke the get_photo_data function,
## assuming your photo_ids list from above is correct!
## If you'd like to try it out, uncomment these two lines. You should then see
## a huge dictonary. You could try writing more investigation code here as well if you find that helpful.

# one_photo_id = sample_photo_ids[10]
# respval = get_photo_data(one_photo_id)



## [PROBLEM 10] - Create a list of photo dictionaries, create a class for Flickr photos, and create a sorted list of instances of this class.
print("\n***** PROBLEM 10 *****\n")

## There are tests for this question. This question has 3 parts.

## Now that you have functions to get data from flickr and you've practiced
## writing data to files and getting data out of files, let's put it all together.

## PART 1:
## Iterate over your sample_photo_ids list from Problem 4, and invoke your get_photo_data function on each of the IDs. Append the result of each invocation to a list, so you are accumulating a list of dictionaries, each of which represents data about one photo. Save that list of dictionaries in a variable called photo_dictions_list.


photo_dictions_list = [get_photo_data(sample_id) for sample_id in sample_photo_ids]




## PART 2:
## Define a class called Photo.
## As input, the class should require 1 dictionary representing a flickr photo.
## The constructor should create the following instance variables:

##### artist, which holds a string representing the flickr *username* of the person who posted the photo, and should always be a string
##### title, which holds a string representing the title of the photo, and should always be a string
##### tags, which holds a list of strings, where each string is one tag of the photo (HINT: look back at the work you did in problem 3!), and should always be a list

## In the constructor of the class, if the dictionary input into the constructor was not valid for some reason (error getting data for the title, artist, or tags instance variable), the program should NOT break.
## Instead, the title should be the string "NONE", the artist should be the string "NONE", and/or the tags value should be an empty list: [].
## You can use a try/except clause inside the __init__ method (constructor) definition to allow this to happen. Though any approach that returns the correct values is fine.

## The class should also have a string method (__str__ method) that returns a string like, for example:

"""
This is my Photo Title, by Ansel Adams
Tags: ['mountains', 'river', 'yosemite']
"""

# or
# (This may depend on your OS and encodings, though most Python 3 users will see the former! MAKE SURE you are using Python 3, NOT Python 2.)

"""
This is my Photo Title, by Ansel Adams
Tags: [u'mountains', u'river', u'yosemite']
"""

## Your assignment has not been completed correctly if all of the results consist of NONE/NONE/[] data, but it is possible that during the process of working on the assignment, a photo will be deleted from Flickr and a few photos *may* result in invalid data.

class Photo(object):
    def __init__(self,photo_dict):
        try:
            self.artist = photo_dict['photo']['owner']['username']
            self.title = photo_dict['photo']['title']['_content']
            self.tags = [i['_content'] for i in sample_photo_rep['photo']['tags']['tag']]
        except:
            self.artist = "NONE"
            self.title = "NONE"
            self.tags = []
    
    def __str__(self):
        return """
This is my Photo {}, by {}
Tags: {}
""".format(self.title,self.artist,self.tags)





## PART 3:
## Iterate over the photo_dictions_list you created in Part 1,
## and for each dictionary in that list, create one instance of class Photo.
## Save the list of Photo instances in a variable called photo_insts.

photo_insts = [Photo(i) for i in photo_dictions_list]


## Sort the photo_insts list by the number of tags, in ascending order. So, for example, a photo that has only 3 tags would come earlier in the list than a photo that has 7 tags. Save the sorted list in a variable called sorted_photo_insts.

sorted_photo_insts = sorted(photo_insts, key=lambda photo:len(photo.tags))



## Write code using the string method (which you write in __str__) of the Photo class to print out the string representation of the first 3 photos in the list sorted_photos_insts.

print(str(sorted_photo_insts[0]).replace("This is my Photo","A Photo"))
print(str(sorted_photo_insts[1]).replace("This is my Photo","Yet Anothet Photo"))
print(str(sorted_photo_insts[2]).replace("This is my Photo","Another Photograph"))


## Sample output to show the formatting that should print out:

"""
A Photo, by Ansel Adams
Tags: ['mountains','yosemite']

Yet Another Photo, by Dorothea Lange
Tags: ['families','journalism']

Another Photograph, by Hilena Abebe
Tags: ['people', 'light', 'trees']
"""

## We cannot test automatically for things that print out. You should run your program and ensure that the correct output is printing.
