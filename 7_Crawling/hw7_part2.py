# 507 Homework 7 Part 2

count = 0
#### Your Part 2 solution goes here ####
import json
try:
    data_file = open('directory_dict.json', 'r')
    data_contents = data_file.read()
    data = json.loads(data_contents)
    data_file.close()

# if there was no file, no worries. There will be soon!
except:
    print('Missing data file "directory_dict.json".')
    data = {}


count = len(list(filter(lambda x: data[x]['title']=="PhD student", data)))


#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)