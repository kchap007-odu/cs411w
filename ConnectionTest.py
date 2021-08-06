import pymysql
import json


json_data = open("data_chart.json").read()
json_obj = json.loads(json_data)

connection = pymysql.connect(host='sql5.freesqldatabase.com', user='sql5428936',
                             password='bARWMcterL', database='sql5428936')

cursor = connection.cursor()

for item in json_obj:
    Current_Fridge_Temp = item.get("Current Fridge Temperature")
    Target_Fridge_Temp = item.get("Target Fridge Temperature")
    Current_Freezer_Temp = item.get("Current Freezer Temperature")
    Target_Freezer_Temp = item.get("Target Freezer Temperature")
    E_Use = item.get("Energy Use")
    Fridge_Last_On = item.get("Fridge Last On Time")
    Fridge_Last_Off = item.get("Fridge Last Off Time")
    Freezer_Last_On = item.get("Freezer Last On Time")
    Freezer_Last_Off = item.get("Freezer Last Off Time")

    cursor.execute("insert into refrigerator_id(Current Fridge Temperature, Target Fridge Temperature, "
                   "Current Freezer Temperature, Target Freezer Temperature, Energy Use, Fridge Last On Time, "
                   "Fridge Last Off Time, Freezer Last On Time, Freezer Last Off Time) "
                   "value(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Current_Fridge_Temp, Target_Fridge_Temp, Current_Freezer_Temp,
                                                         Target_Freezer_Temp, E_Use, Fridge_Last_On, Fridge_Last_Off,
                                                         Freezer_Last_On, Freezer_Last_Off))
connection.commit()
connection.close()
