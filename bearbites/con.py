import pyodbc

server = 'bearbites.database.windows.net'
database = 'BearBites'
username = 'ajakad@bearbites'
password = 'cs4800BearBites'
driver= '{ODBC Driver 17 for SQL Server}'
def getConnection():
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("EXEC AccountLookup @UserName=admin , @PassCode=testbear")
    row = cursor.fetchone()
    while row:
        print (str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()
    return cnxn