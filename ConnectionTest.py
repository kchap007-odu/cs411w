import pymysql


connection = pymysql.connect(host='sql5.freesqldatabase.com', user='sql5428936',
                             password='bARWMcterL', database='sql5428936')

cursor = connection.cursor()
sql_query = "SELECT VERSION()"

try:
    cursor.execute(sql_query)
    data = cursor.fetchone()
    print("Database version : %s" %data)

except Exception as e:
    print("Exception :", e)

connection.close()

# works and prints out Database version : 5.5.62-0ubuntu0.14.04.1
