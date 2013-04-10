import xmlrpclib, subprocess, time
server = xmlrpclib.Server('http://localhost:8000')
node_name = "slave"
c = 0

while True:
	new = server.get_tasks(node_name)
	for item in new:
		subprocess.Popen(item, shell=True)
		server.finish(node_name, item)
	time.sleep(0.5)