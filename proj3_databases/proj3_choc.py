import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'

# Create tables
def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        CREATE TABLE IF NOT EXISTS 'Countries' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' NCHAR(2),
            'Alpha3' NCHAR(3),
            'EnglishName' TEXT,
            'Region' TEXT,
            'Subregion' TEXT,
            'Population' INTEGER,
            'Area' REAL
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE IF NOT EXISTS 'Bars' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Company' TEXT,
            'SpecificBeanBarName' TEXT,
            'Ref' TEXT,
            'ReviewDate' TEXT,
            'CocoaPercent' REAL,
            'CompanyLocationId' INTEGER,
            'Rating' REAL,
            'BeanType' TEXT,
            'BroadBeanOriginId' INTEGER,
            CONSTRAINT fk_company_location
            FOREIGN KEY (CompanyLocationId)
            REFERENCES Countries(Id)
            CONSTRAINT fk_broad_bean_origin
            FOREIGN KEY (BroadBeanOriginId)
            REFERENCES Countries(Id)
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

init_db()

# Load data
def insert_countries_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # if table is not empty, don't need to insert
    if len(cur.execute('SELECT * FROM "Countries" LIMIT 1').fetchall()): return
    
    with open(COUNTRIESJSON, "r", encoding='utf-8') as content:
        countries_data = json.load(content)
    
    for c in countries_data:
        insertion = (None, c['alpha2Code'], c['alpha3Code'], c['name'], c['region'], c['subregion'], c['population'], c['area'])
        statement = 'INSERT INTO "Countries" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def insert_bars_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # if table is not empty, we don't need to insert
    if len(cur.execute('SELECT * FROM "Bars" LIMIT 1').fetchall()): return
    
    with open(BARSCSV, "r") as content:
        bars_data = csv.reader(content)
        next(bars_data) # skip header
        for row in bars_data:
            insertion = (None, row[0], row[1], row[2], row[3], row[4].replace("%",""),row[5], row[6], row[7], row[8])
            statement = 'INSERT INTO "Bars" '
            statement += '''VALUES (?, ?, ?, ?, ?, ?, 
(SELECT Id FROM "Countries" WHERE EnglishName = ?), ?, ?, (SELECT Id FROM "Countries" WHERE EnglishName = ?))'''
            cur.execute(statement, insertion)

    conn.commit()
    conn.close()

insert_countries_data()
insert_bars_data()


# Part 2: Implement logic to process user commands
def bad_command(command):
    print("Command not recognized: " + command)
    print()

def format(row, percent = False):
    res = list(row)
    if len(row) == 6:
        for i in [0,1,2,5]:
            if not row[i]:
                res[i] = "Unknown"+" "*8 
            elif len(row[i]) <= 12:
                res[i] = row[i] + " "*(15-len(row[i]))
            else:
                res[i] = row[i][:12]+"..."
        
        res[3] = round(row[3],1).__str__()+" "*(5-len(round(row[3],1).__str__()))
        res[4] = row[4].__str__()+"%"+" "*(5-len(row[4].__str__()))
    elif len(row) == 3:
        for i in [0,1]:
            if not row[i]:
                res[i] = "Unknown"+" "*8 
            elif len(row[i]) <= 12:
                res[i] = row[i] + " "*(15-len(row[i]))
            else:
                res[i] = row[i][:12]+"..."
        if percent:
            res[2] = round(row[2]).__str__() + "%"
        else:
            res[2] = row[2].__str__() if isinstance(row[2],int) else round(row[2],1).__str__()
    elif len(row) == 2:
        if not row[0]:
            res[0] = "Unknown"+" "*8 
        elif len(row[0]) <= 12:
            res[0] = row[0] + " "*(15-len(row[0]))
        else:
            res[0] = row[0][:12]+"..."
        if percent:
            res[1] = round(row[1]).__str__() + "%"
        else:
            res[1] = row[1].__str__() if isinstance(row[1],int) else round(row[1],1).__str__()

    return res

order_mapping = {"ratings":"Rating","cocoa":"CocoaPercent"}
name_mapping_bars = {"sellcountry":"C1.Alpha2","sourcecountry":"C2.Alpha2","sellregion":"C1.Region","sourceregion":"C2.Region"}
name_mapping_countries = {"country":"Alpha2","region":"Region"}


def process_command(command):
    if not command:
        if __name__=="__main__":
            print()
        return

    command_eles = command.split()
    columns = """Bars.SpecificBeanBarName, Bars.Company, C1.EnglishName AS CompanyLocation, Bars.Rating, 
Bars.CocoaPercent, C2.EnglishName AS BroadBeanOrigin"""
    conditions = []
    order = "ratings"
    desc = " DESC"
    limit = "10"
    groupby = ""
    having =" HAVING COUNT(*)>4 "
    choose = ""
    percent = False
    if command_eles[0] == 'bars':
        order = "Rating"
        having = ""
        for ele in command_eles[1:]:
            eles = ele.split("=")
            if len(eles) == 1:
                if ele in order_mapping:
                    order = order_mapping[ele]
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            elif len(eles) == 2:
                if eles[0] in {"top","bottom"}:
                    desc = " DESC" if eles[0] == "top" else ""
                    limit = str(int(eles[1]))
                elif eles[0] in name_mapping_bars:
                    conditions.append(name_mapping_bars[eles[0]]+"='"+eles[1]+"'")
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            else:
                if __name__=="__main__": bad_command(command)
                return
    elif command_eles[0] == 'companies':
        groupby = " GROUP BY Company"
        agg = "AVG(Rating) AS ratings" 
        choose = "C1"
        for ele in command_eles[1:]:
            eles = ele.split("=")
            if len(eles) == 1:
                if ele in order_mapping:
                    order = ele
                    agg = "AVG("+order_mapping[ele]+") AS "+order
                elif ele == "bars_sold":
                    order = ele
                    agg = "COUNT(*) AS "+ele
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            elif len(eles) == 2:
                if eles[0] in {"top","bottom"}:
                    desc = " DESC" if eles[0] == "top" else ""
                    limit = str(int(eles[1]))
                elif eles[0] in name_mapping_countries:
                    conditions.append(name_mapping_countries[eles[0]]+"='"+eles[1]+"'")
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            else:
                if __name__=="__main__": bad_command(command)
                return
        
        columns = "Bars.Company, C1.EnglishName AS CompanyLocation, "+agg
    
    elif command_eles[0] == 'countries':
        groupby = " GROUP BY EnglishName"
        agg = "AVG(Rating) AS ratings" 
        choose = "C1"
        for ele in command_eles[1:]:
            eles = ele.split("=")
            if len(eles) == 1:
                if ele in order_mapping:
                    order = ele
                    agg = "AVG("+order_mapping[ele]+") AS "+order
                elif ele == "bars_sold":
                    order = ele
                    agg = "COUNT(*) AS "+ele
                elif ele == "sellers" or ele == "sources":
                    if ele == "sources": 
                        choose = "C2"
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            elif len(eles) == 2:
                if eles[0] in {"top","bottom"}:
                    desc = " DESC" if eles[0] == "top" else ""
                    limit = str(int(eles[1]))
                elif eles[0] == "region":
                    conditions.append("region='"+eles[1]+"'")
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            else:
                if __name__=="__main__": bad_command(command)
                return
        
        columns = choose +".EnglishName AS Country, "+ choose+".Region, "+agg
    elif command_eles[0] == 'regions':
        conditions.append("Region IS NOT NULL")
        groupby = " GROUP BY C1.Region"
        agg = "AVG(Rating) AS ratings" 
        choose = "C1"
        for ele in command_eles[1:]:
            eles = ele.split("=")
            if len(eles) == 1:
                if ele in order_mapping:
                    order = ele
                    agg = "AVG("+order_mapping[ele]+") AS "+order
                elif ele == "bars_sold":
                    order = ele
                    agg = "COUNT(*) AS "+ele
                elif ele == "sellers" or ele == "sources":
                    if ele == "sources": 
                        groupby = " GROUP BY C2.Region"
                        choose = "C2"
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            elif len(eles) == 2:
                if eles[0] in {"top","bottom"}:
                    desc = " DESC" if eles[0] == "top" else ""
                    limit = str(int(eles[1]))
                else:
                    if __name__=="__main__": bad_command(command)
                    return
            else:
                if __name__=="__main__": bad_command(command)
                return
        
        columns = choose+".Region, "+agg

    else:
        if __name__=="__main__": bad_command(command)
        return

    condition = " WHERE "+ " AND ".join(conditions) if conditions else ""
    join = {"C1":" LEFT JOIN Countries AS C1 ON Bars.CompanyLocationId = C1.Id ","C2":" LEFT JOIN Countries AS C2 ON Bars.BroadBeanOriginId = C2.Id "}
    join[""] = join["C1"]+join["C2"]
    statement = "SELECT "+columns+" FROM Bars "+join[choose] + condition + groupby+ having +" ORDER BY "+order + desc + " LIMIT "+limit
    
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(statement)
    res = cur.fetchall()
    #print(res)
    for row in res:
        row = format(row,order=="cocoa")
        if __name__=="__main__":
            print(" ".join(row))

    if __name__=="__main__": print()
    conn.close()
    return res


def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = input('Enter a command: ')
    while response != 'exit':

        if response == 'help':
            if __name__=="__main__": print(help_text)
        else:
            process_command(response)
        
        response = input('Enter a command: ')
    
    if __name__=="__main__": print("bye")

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
