from flask import Flask, render_template,request
from flask_socketio import SocketIO
from datetime import datetime
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
users_log = dict()
@app.route('/')
def sessions():

    return render_template('session.html')

def messageReceived(methods=['GET']):
    print('Message was received!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('Received my event: ' + str(json))
    log_file = open("log_file.txt","a+")
    current_time = datetime.now().strftime("%d-%m-%Y:%S-%M-%H") 
    if(json["host"] not in users_log):
        users_log[json["host"]] = 1
    else:
        users_log[json["host"]] = users_log[json["host"]] + 0.2


    json["font"] = 50/users_log[json["host"]]

    if(json["font"]<10):
        json["font"] = 50
        users_log[json["host"]] = 0

    print(json)
    log_file.write(str({"date:":current_time,"host":json["host"],"message":json["message"]})+"\n")
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True,port=80,host="0.0.0.0")