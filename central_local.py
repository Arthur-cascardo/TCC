import socket
import mysql
import database
from mysql.connector import Error

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    dbs = database
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    dbs.run_db()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_str = data.decode('ascii')
            if ":" in data_str:

                conn.sendall(data)
                break

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
            "SELECT"
            "`hospital`.`ID`, `hospital`.`NOME`, `hospital`.`TEMPO_ESPERA`, `hospital`.`NUM_PACIENTES`, `medico`.`NOME`, `medico`.`ESPECIALIDADE`, `medico`.`TEMPO_MED_ESPERA`"
            "FROM"
            "`medico`"
            "LEFT"
            "OUTER"
            "JOIN"
            "`hospital`"
            "ON"
            "`medico`.`ID_HOSPITAL` = `hospital`.`ID`"
            "WHERE"
            "`hospital`.`NOME` = '%(hosp)s'"
            "AND"
            "`medico`.`ESPECIALIDADE` = '%(esp)s'"
            "UNION"
            "SELECT"
            "`hospital`.`ID`, `hospital`.`NOME`, `hospital`.`TEMPO_ESPERA`, `hospital`.`NUM_PACIENTES`, `medico`.`NOME`, `medico`.`ESPECIALIDADE`, `medico`.`TEMPO_MED_ESPERA`"
            "FROM"
            "`medico`"
            "RIGHT"
            "OUTER"
            "JOIN"
            "`hospital`"
            "ON"
            "`medico`.`ID_HOSPITAL` = `hospital`.`ID`"
            "WHERE"
            "`hospital`.`NOME` = '%(hosp)s'"
            "AND"
            "`medico`.`ESPECIALIDADE` = '%(esp)s'",
            ({'hosp': hosp, 'esp': esp}))
            result = cursor.fetchall()
            df = pd.DataFrame(result)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            print("MySQL db is closed")
