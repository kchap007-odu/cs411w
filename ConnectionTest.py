import pyodbc


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=sql5.freesqldatabase.com;'
                      'Database=sql5428936;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM database_name.table')

for row in cursor:
    print(row)
