'''
SI 507 F18 homework 9: Basic SQL statements
'''

import sqlite3 as sqlite

DBNAME = 'Northwind_small.sqlite'

def query(statement):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(statement)
    res = cur.fetchall()
    conn.close()
    return res

def printResult(question):
    if __name__=="__main__":
        for row in question():
            print(''.join([('{:'+str(7 if isinstance(x,int) or isinstance(x,float) else 30)+'s}').format(str(x)) for x in row]))

#----- Q1. Show all rows from the Region table 
print('-'*20 + "Question 1" + '-'*20)
def question1():
    return query("SELECT * FROM Region")

printResult(question1)

#----- Q2. How many customers are there? 
print('-'*20 + "Question 2" + '-'*20)
def question2():
    return query("SELECT COUNT(Id) FROM 'Customer'")

printResult(question2)

#----- Q3. How many orders have been made? 
print('-'*20 + "Question 3" + '-'*20)
def question3():
    return query("SELECT COUNT(Id) FROM 'Order'")

printResult(question3)

#----- Q4. Show the first five rows from the Product table 
print('-'*20 + "Question 4" + '-'*20)
def question4():
    return query("SELECT * FROM 'Product' LIMIT 5")

printResult(question4)

#----- Q5. Show the names of the five cheapest products 
print('-'*20 + "Question 5" + '-'*20)
def question5():
    return query("SELECT ProductName FROM 'Product' ORDER BY UnitPrice LIMIT 5")

printResult(question5)

#----- Q7. Show the names and number of units in stock of all products that have more than 100 units in stock  
print('-'*20 + "Question 6" + '-'*20)
def question6():
    return query("SELECT ProductName, UnitsInStock FROM 'Product' WHERE UnitsInStock>100")

printResult(question6)

#----- Q7. Show all column names in the Order table 
print('-'*20 + "Question 7" + '-'*20)
def question7():
    return query("SELECT name FROM PRAGMA_TABLE_INFO('Order')")

printResult(question7)

#----- Q8. Show the names of all customers who lives in USA and have a fax number on record.
print('-'*20 + "Question 8" + '-'*20)
def question8():
    return query("SELECT ContactName FROM 'Customer' WHERE Country='USA' AND FAX IS NOT NULL")

printResult(question8)

#----- Q9. Show the names of all the products, if any, that requires a reorder. 
# (If the units in stock of a product is lower than its reorder level but there's no units of the product currently on order, the product requires a reorder) 
print('-'*20 + "Question 9" + '-'*20)
def question9():
    return query("SELECT ProductName FROM 'Product' WHERE UnitsInStock<ReorderLevel AND UnitsOnOrder=0")

printResult(question9)

#----- Q10. Show ids of all the orders that ship to France where postal code starts with "44"
print('-'*20 + "Question 10" + '-'*20)
def question10():
    return query("SELECT Id FROM 'Order' WHERE ShipCountry='France' AND ShipPostalCode LIKE '44%'")

printResult(question10)


