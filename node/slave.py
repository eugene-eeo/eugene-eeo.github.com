import xmlrpclib, subprocess, time
server=xmlrpclib.Server('http://192.168.128.7:8000')
node_name="slave"
server.log(node_name,"slave has started up.")
while True:
	try:
		new=server.get_tasks(node_name)
		if new == "killed":
			break
		if new:
			for item in new:
				print ("Running task: %s" % (item))
				subprocess.Popen(item,shell=True,stdout=open("%s-logs.txt"%(node_name),"w"),stderr=open("%s-logs.txt"%(node_name),"w"))
				server.finish(node_name,item)
		time.sleep(5)
	except KeyboardInterrupt:
		break
server.node_is_offline(node_name)
exit()