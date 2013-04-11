import xmlrpclib, subprocess, time, os
server=xmlrpclib.Server('http://localhost:8000')
node_name="slave"

while True:
	try:
		new=server.get_tasks(node_name)
		if new == "killed":
			break
		if new:
			for item in new:
				subprocess.Popen(item, shell=True,stdout=open("%s-logs.txt"%(node_name),"w"))
				server.finish(node_name, item)
		time.sleep(5)
	except KeyboardInterrupt:
		exit()