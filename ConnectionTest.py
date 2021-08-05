import pyodbc
import json


# connect to database
conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=sql5.freesqldatabase.com@3306; DATABASE=sql5428936; UID=sql5428936; PWD=bARWMcterL')
cursor = conn.cursor()

# create a record as python dictionary

record = {

"Current Fridge Temperature": 34,

"Target Fridge Temperature": 38,

"Current Freezer Temperature": 5,

"Target Freezer Temperature": 0,

"Energy Use": 397,

"Fridge Last On Time": "22:46:34",

"Fridge Last Off Time": "4:45:2",

"Freezer Last On Time": "11:39:27",

"Freezer Last Off Time": "14:39:37"

}

# insert this into database as json object

cursor.execute("Insert Into refridgerator values (?)", (json.dumps(record),))
cursor.commit()

# close all connections

cursor.close()
conn.close()
