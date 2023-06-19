import socket
import database


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    dbs = database
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                dbs.run_db()
                break
            data_str = data.decode('ascii')
            if ":" in data_str:
                temp = data_str.split(":")
                query_result = dbs.run_query(temp[0], temp[1])
                print(query_result)
                conn.sendall(query_result)
                break
