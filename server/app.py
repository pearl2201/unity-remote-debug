from flask import Flask, request,render_template,redirect,url_for
from datetime import datetime
import json
app = Flask(__name__)
import sys
logs = []

@app.route('/', methods=['GET','POST'])
@app.route('/device/', methods=['GET','POST'])
def log_device():
	if request.method == "GET":
		devices = list(set([x["device"] for x in logs]))
		return render_template("device.html",devices=devices)
	else:
		device = request.form.get("device")
		log_type = int(request.form.get("log-type"))
		
		return redirect(url_for('view_debug_type',device=device,log_type=log_type))

	
@app.route('/log/<device>/<log_type>', methods=['GET'])
def view_debug_type(device,log_type):
	print ("%s %s" %(device,log_type))
	if int(log_type) == 5:
		collect_logs = [x for x in logs if x["device"] == device]
	else:
		collect_logs = [x for x in logs if x["device"] == device and x["type"] == int(log_type)]
	if len(collect_logs) > 200:
		collect_logs =  collect_logs[-200:]
	for i in range(len(collect_logs)):
		collect_logs[i]["id"] = i
		collect_logs[i]["display"] = collect_logs[i]["condition"][:100] if len(collect_logs[i]["condition"])>100 else collect_logs[i]["condition"]
	devices = list(set([x["device"] for x in logs]))
	return render_template("log.html",logs = collect_logs,devices=devices,current_type=log_type,current_device=device)

		
@app.route('/log/<device>', methods=['GET'])
def view_debug(device):
	return redirect(url_for('view_debug_type',device=device,type=5))

	
@app.route('/debug/', methods=['POST'])
def log_debug():
	if request.method == "POST":
		data = request.json
		data["time"] = datetime.utcnow()
		logs.append(data)

		return "ok",200



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

