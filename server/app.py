from flask import Flask, request,render_template,redirect,url_for
from datetime import datetime
from flask_socketio import SocketIO
import json
from flask_socketio import join_room, leave_room,send,emit
import sys

app = Flask(__name__)
socketio = SocketIO(app)
dict_logs = {}


@app.route('/', methods=['GET','POST'])
@app.route('/device/', methods=['GET','POST'])
def log_device():
	if request.method == "GET":
		devices = dict_logs.keys()
		return render_template("device.html",devices=devices)
	else:
		device = request.form.get("device")
		log_type = int(request.form.get("log-type"))
		
		return redirect(url_for('view_debug_type',device=device,log_type=log_type))
		

	
@app.route('/log/<device>/<log_type>', methods=['GET'])
def view_debug_type(device,log_type):
	if (device in  dict_logs and int(log_type) >=0 and int(log_type) <=5):
		print ("%s %s" %(device,log_type))
		if int(log_type) == 5:
			collect_logs = dict_logs[device]
		else:
			collect_logs = [x for x in dict_logs[device] if x["type"] == int(log_type)]
		if len(collect_logs) > 200:
			collect_logs =  collect_logs[-200:]
		for i in range(len(collect_logs)):
			collect_logs[i]["id"] = i
			
		devices = dict_logs.keys()
		return render_template("log.html",logs = collect_logs,devices=devices,current_type=log_type,current_device=device)
	else:
		return redirect(url_for('log_device'))

		
@app.route('/log/<device>', methods=['GET'])
def view_debug(device):
	return redirect(url_for('view_debug_type',device=device,type=5))

	
@app.route('/debug/', methods=['POST'])
def log_debug():
	if request.method == "POST":
		data = request.json
		data["time"] = str(datetime.utcnow())
		data["display"] = data["condition"][:130] if len(data["condition"])>130 else data["condition"]
		if data["device"] in dict_logs:
			dict_logs[data["device"]].append(data)
			socketio.emit("debug-log",data,room=data["device"])
		else:
			dict_logs[data["device"]] = [data]
			socketio.emit("new-device",{"device":data["device"]},broadcast=True)
		
		return "ok",200

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

@socketio.on('leave')
def on_leave(data):
	room = data['room']
	leave_room(room)

if __name__ == '__main__':
    #app.run(debug=True, use_reloader=True)
	socketio.run(app,debug=True,use_reloader=True,extra_files=["templates/log.html"])

