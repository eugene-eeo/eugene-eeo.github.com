import xmlrpc.client, time, mimetypes

server = xmlrpc.client.ServerProxy("http://localhost:8000")
def _time():
	return time.strftime("%H:%M:%S")

def _green():
	return '\x1b[32m'

def _bold():
	return '\x1b[1m'

def _reset():
	return '\x1b[0m'

def deploy(item):
	x = mimetypes.guess_type(item)[0]
	name = item.split("/")[-1]
	y = server.deploy(name, open(item,"r").read())
	if "image" not in x and y:
		print ("[%s%s%s] Deployed \"%s\" to remote end" % (_green(),_time(),_reset(),item))
		if y != True:
			print ("%s>>%s Binary is renamed as: %s" % (_green(), _reset(), y))
	else:
		print("%s>>%s Failed to deploy binary: %s" % (_green(),_reset(),item))

def push_task(task):
	if server.run_task(task):
		print ("[%s%s%s] Pushed task \"%s\" to remote end" % (_green(),_time(),_reset(),task))
	else:
		print ("[%s%s%s] Task \"%s\" failed to be pushed" % (_green(),_time(),_reset(),task))

def kill_task(task):
	if server.kill_task(task):
		print ("[%s%s%s] Killed task: \"%s\"" % (_green(),_time(),_reset(),task))
	else:
		print ("[%s%s%s] Task \"%s\" is not killed" % (_green(),_time(),_reset(),task))

def get_task(task=False):
	if task:
		y = server.get_task(task)
		if y:
			print ("%s>>%s %s PID: %s" % (_green(),_reset(),task, y))
		else:
			print ("%s>>%s Failed to retrieve PID of task: %s" % (_green(),_reset(),task))
	else:
		y = server.get_task()
		for item in y:
			print (item + " " * (20 - len(item)) + str(y[item]))

while True:
	eval(input(": "))