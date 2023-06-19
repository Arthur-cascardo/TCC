import mysql.connector
from mysql.connector import Error
import pandas as pd
from unidecode import unidecode
import time as t


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


def run_db():
    try:

        db = mysql.connector.connect(host='localhost', database='pei2', user='arthur', password='1234')

        if db.is_connected():
            db_Info = db.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            while True:
                cursor = db.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute("SELECT * FROM new_view")

                result = cursor.fetchall()
                df = pd.DataFrame(result)
                dfd = df.copy()
                temp_1 = []
                temp_2 = []

                i = 0
                for time in df[2]:
                    dfd.loc[i, 2] = dfd.loc[i, 2] - 1
                    temp_1.append(dfd.loc[i, 2])
                    dfd.loc[i, 2] = secondsToMins(time)
                    i = i + 1
                i = 0
                for time in df[6]:
                    dfd.loc[i, 6] = dfd.loc[i, 6] - 1
                    temp_2.append(dfd.loc[i, 6])
                    dfd.loc[i, 6] = secondsToMins(time)
                    i = i + 1
                val = []
                i = 0
                for ids in df[0]:
                    val.append((int(temp_1[i]), ids))
                    i = i + 1

                sql = "UPDATE hospital SET TEMPO_ESPERA = %s where ID = %s"
                cursor.executemany(sql, val)
                i = 0
                val.clear()
                for ids in df[0]:
                    val.append((int(temp_2[i]), ids))
                    i = i + 1

                sql = "UPDATE medico SET TEMPO_MED_ESPERA = %s where ID = %s"
                cursor.executemany(sql, val)

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

                t.sleep(1)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            print("MySQL db is closed")


def run_query(hosp, esp):
    try:

        db = mysql.connector.connect(host='localhost', database='pei2', user='arthur', password='1234')

        if db.is_connected():
            db_Info = db.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = db.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute(
            "SELECT "
            "`hospital`.`ID`, `hospital`.`NOME`, `hospital`.`TEMPO_ESPERA`, `hospital`.`NUM_PACIENTES`, `medico`.`NOME`, `medico`.`ESPECIALIDADE`, `medico`.`TEMPO_MED_ESPERA` "
            "FROM "
            "`medico` "
            "LEFT "
            "OUTER "
            "JOIN"
            "`hospital` "
            "ON "
            "`medico`.`ID_HOSPITAL` = `hospital`.`ID` "
            "WHERE "
            "`hospital`.`NOME` = %(hosp)s "
            "AND "
            "`medico`.`ESPECIALIDADE` = %(esp)s "
            "UNION "
            "SELECT "
            "`hospital`.`ID`, `hospital`.`NOME`, `hospital`.`TEMPO_ESPERA`, `hospital`.`NUM_PACIENTES`, `medico`.`NOME`, `medico`.`ESPECIALIDADE`, `medico`.`TEMPO_MED_ESPERA` "
            "FROM "
            "`medico` "
            "RIGHT "
            "OUTER "
            "JOIN "
            "`hospital` "
            "ON "
            "`medico`.`ID_HOSPITAL` = `hospital`.`ID` "
            "WHERE "
            "`hospital`.`NOME` = %(hosp)s "
            "AND "
            "`medico`.`ESPECIALIDADE` = %(esp)s ",
            ({'hosp': hosp, 'esp': esp}))
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            dfd = df.copy()
            i = 0
            for time in df[2]:
                dfd.loc[i, 2] = secondsToMins(time)
                i = i + 1
            i = 0
            for time in df[6]:
                dfd.loc[i, 6] = secondsToMins(time)
                i = i + 1
            return dfd
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        return
