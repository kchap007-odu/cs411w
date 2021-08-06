import pymysql
import json


json_data = open("data_chart.json").read()
json_obj = json.loads(json_data)

connection = pymysql.connect(host='sql5.freesqldatabase.com', user='sql5428936',
                             password='bARWMcterL', database='sql5428936')

cursor = connection.cursor()

for item in json_obj:
    Current_Fridge_Temp = int(item.get("Current Fridge Temperature"))
    Target_Fridge_Temp = int(item.get("Target Fridge Temperature"))
    Current_Freezer_Temp = int(item.get("Current Freezer Temperature"))
    Target_Freezer_Temp = int(item.get("Target Freezer Temperature"))
    E_Use = int(item.get("Energy Use"))
    Fridge_Last_On = item.get("Fridge Last On Time")
    Fridge_Last_Off = item.get("Fridge Last Off Time")
    Freezer_Last_On = item.get("Freezer Last On Time")
    Freezer_Last_Off = item.get("Freezer Last Off Time")

    cursor.execute("INSERT INTO refrigerator_id (Current_Fridge_Temperature, Target_Fridge_Temperature, "
                   "Current_Freezer_Temperature, Target_Freezer_Temperature, Energy_Use, Fridge_Last_On_Time, "
                   "Fridge_Last_Off_Time, Freezer_Last_On_Time, Freezer_Last_Off_Time) "
                   "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Current_Fridge_Temp, Target_Fridge_Temp, Current_Freezer_Temp,
                                                          Target_Freezer_Temp, E_Use, Fridge_Last_On, Fridge_Last_Off,
                                                          Freezer_Last_On, Freezer_Last_Off))

connection.commit()
connection.close()
