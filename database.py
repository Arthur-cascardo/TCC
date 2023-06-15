import mysql.connector
from mysql.connector import Error
import pandas as pd
from unidecode import unidecode


def secondsToMins(time):
    mins = int(time/60)
    if mins > 59:
        hours = int(mins/60)
        mins = int(mins % 60)
        if mins < 10:
            mins = "0" + str(mins)
        seconds = int(time % 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
        return str(hours) + ":" + str(mins) + ":" + str(seconds)
    else:
        if mins < 10:
            mins = "0" + str(mins)
        seconds = int(time % 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
        return str(mins) + ":" + str(seconds)

try:

    db = mysql.connector.connect(host='localhost', database='pei2', user='arthur', password='1234')
    
    if db.is_connected():
        db_Info = db.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        ##TODO in loop, val as json
        # sql = "INSERT INTO medico (ID, ID_PACIENTE, ID_HOSPITAL, NOME, ESPECIALIDADE, TEMPO_MED_ESPERA) VALUES (%s, %s, %s, %s, %s, %s)"
        # val = [
        #
        # ]

        # cursor.executemany(sql, val)

        cursor.execute("SELECT * FROM new_view")

        result = cursor.fetchall()
        df = pd.DataFrame(result)
        dfd = df.copy()

        i = 0
        for time in df[1]:
            dfd.loc[i, 1] = secondsToMins(time)
            i = i + 1
        i = 0
        for time in df[5]:
            dfd.loc[i, 5] = secondsToMins(time)
            i = i + 1

        dfd.to_csv("hospitals.csv", index=False, header=False)
        file = open("hospitals.csv", 'r', encoding='utf-8')
        content = file.read()
        content = unidecode(content)
        file.close()
        file = open("hospitals.csv", 'w')
        file.write('Hospital, Tempo Espera, Pacientes Aguardando, Medico, Especialidade, Tempo Espera Medico\n')
        file.close()
        file = open("hospitals.csv", 'a')
        file.write(content)
        file.close()
        db.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if db.is_connected():
        cursor.close()
        db.close()
        print("MySQL db is closed")
