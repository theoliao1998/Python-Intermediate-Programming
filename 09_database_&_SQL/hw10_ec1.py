import sqlite3 as sqlite

DBNAME = 'Northwind_small.sqlite'

def query(statement):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(statement)
    res = cur.fetchall()
    conn.close()
    return res

res = query('''
    WITH o AS (
	SELECT CustomerID, OrderDate FROM 'Order' ORDER BY OrderDate DESC
    )
    SELECT o1.CustomerID, o1.OrderDate AS 'Order date', o2.OrderDate AS 'Previous order date', 
        (julianday(o1.OrderDate) - julianday(o2.OrderDate)) AS ' days passed'
        FROM o AS o2 JOIN o AS o1 ON o2.OrderDate < o1.OrderDate AND o1.CustomerID = o2.CustomerID
	    GROUP BY o1.CustomerID,o1.OrderDate ORDER BY o1.CustomerID, 'Order date'
'''
)

print("CustomerID,Order date,Previous order date, days passed")
for row in res:
    print(",".join([str(x) for x in row]))



