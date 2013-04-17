import xmlrpclib, subprocess, time, os
server=xmlrpclib.Server('http://192.168.128.8:8000')
node_name="slave"
tasks={}
server.log(node_name,"%s has started up." % (node_name))
while True:
	try:
		new=server.get_tasks(node_name)
		if new == ["killed"]:
			break
		if new:
			for item in new:
				print("Running task: %s" % (item))
				x=subprocess.Popen(item,shell=True,stdout=open("%s-logs.txt"%(node_name),"w"),stderr=open("%s-logs.txt"%(node_name),"w")).pid
				tasks[item]=x
				server.finish(node_name,item)
		time.sleep(5)
	except KeyboardInterrupt:
		break
server.node_is_offline(node_name)
for item in tasks:
	print os.popen("kill %s" % (tasks[item])).read()
exit()