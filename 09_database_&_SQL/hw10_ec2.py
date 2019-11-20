import sqlite3 as sqlite
import sys

DBNAME = 'Northwind_small.sqlite'

def query(statement):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(statement)
    res = cur.fetchall()
    conn.close()
    return res

res = query('''
    SELECT COUNT(*) FROM 'Order' AS o JOIN Employee AS e ON o.EmployeeId=e.Id 
        WHERE ShipCity LIKE '{}%' AND length(e.FirstName) = {}
'''.format(sys.argv[1],sys.argv[2])
)

print('''Searched for
1) ShipCity starts with: {}
2) The number of characters in employee's first name: {}
The number of orders: {}
'''.format(sys.argv[1],sys.argv[2],res[0][0])
)






