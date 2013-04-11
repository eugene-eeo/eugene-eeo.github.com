import xmlrpclib, subprocess, time
server=xmlrpclib.Server('http://localhost:8000')
node_name="slave"
while True:
	new=server.get_tasks(node_name)
	if new:
		for item in new:
			subprocess.Popen(item, shell=True)
			server.finish(node_name, item)
	time.sleep(2)