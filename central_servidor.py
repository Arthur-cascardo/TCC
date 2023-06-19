import json
import socket
from flask import request, Flask, render_template, make_response
import pandas as pd


app = Flask(__name__)


@app.route("/")
def game():
    data = ""
    createPage(data)
    return render_template('front.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    select1 = request.form.get('hosp')
    select2 = request.form.get('esp')
    data = getLocalCentralInfo(select1, select2)
    createPage(data)
    return render_template('front.html')


@app.route("/api/rank/escaped")
def escaped():
    args = request.args.to_dict()


def getLocalCentralInfo(op1, op2):
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server
    data = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        args = op1 + ":" + op2
        s.sendall(bytes(args, 'ascii'))

    return data


def createPage(data):
    df = pd.read_csv("hospitals.csv")
    html = df.to_html(classes='mystyle')

    hosp_temp = df['Hospital']
    esp_temp = df[' Especialidade']
    esp = ""
    hosp = ""
    check_lst = []
    i = 1

    for h in hosp_temp:
        if str(h) in check_lst:
            continue
        check_lst.append(str(h))
        hosp = hosp + '<option value="' + str(h) + '">' + str(h) + '</option>' + '\n'
        i = i + 1
    check_lst.clear()
    for e in esp_temp:
        if str(e) in check_lst:
            continue
        check_lst.append(str(e))
        esp = esp + '<option value="' + str(e) + '">' + str(e) + '</option>' + '\n'
        i = i + 1

    # write html to file
    text_file = open("templates/front.html", "w")
    text_file.write("<html>\n"
        "<head>\n"
            '<link rel= "stylesheet" type= "text/css" href= "{{ url_for("static",filename="styles/df_style.css") }}">\n'
        "</head>\n"
        "<center><h1> Tabela dos hospitais por disponibilidade de atendimento</h1></center>\n"
        "<center>\n"
        '<body>\n'
        '<div class="float-container">'
        '<form class="form-inline" method="POST" action="{{ url_for("search") }}">'
            '<div class="float-child">'
                '<div class="green">'
                    
                        '<label for="hosp">Escolha por Especialidade:   </label>'
                            '<select name="esp" id="esp">'
                            +
                                esp
                            +
                            '</select>'
                     
                '</div>'
            '</div>'
            
            '<div class="float-child">'
                '<div class="green">'
                    '<label for="hosp">Escolha por Hospital:    </label>'
                        '<select name="hosp" id="hosp">'
                        +
                            hosp
                        +
                        '</select>'
                    
                '</div>'
            '</div>'
                    
                '<div class="float-button">'
                    '<div class="green">'
                            '<button type="submit" class="button-37" role="button">Pesquisar Hospitais</button>'
                        
                    '</div>'
                '</div>'   
            '</div>'
        '</form>'
        '</div>'
        '<br>'
        '<br>'
        '<br>'
        '<br>'
                    )
    text_file.close()
    text_file = open("templates/front.html", "a")
    text_file.write(html)
    text_file.write('</center>\n'
                    '</body>\n'
                    '</html>')
    text_file.close()


app.run()

