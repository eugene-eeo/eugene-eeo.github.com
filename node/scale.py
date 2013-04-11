# coding=utf-8
import xmlrpclib, socket, time
nodeID = "a"
monitor_nodes = ["slave","core-db","core-ajax","java"]
nodes = {}
additional_tasks = []

server = xmlrpclib.Server('http://localhost:8000')
server.register_control(nodeID)
# get the tasks for each node, and count them, then
# place them inside the stack
def index():
	global nodes, additional_tasks, monitor_nodes
	for item in monitor_nodes:
		tasks = server.get_tasks(item)
		nodes[item]=len(tasks)
		if len(tasks) > 5:
			x = "\x1b[31m[]\x1b[0m" * len(tasks)
		else:
			x = "[]" * len(tasks)
		print "%s: %s" % (item, x)

index()
for node in monitor_nodes:
	xs = server.get_tasks(node)
	for task in xs:
		if xs.index(task) != 0:
			additional_tasks.append(task)
			server.finish(node, task)

print "---------------"

while True:
	try:
		time.sleep(5)
		cx = len(monitor_nodes)
		for node in nodes:
			if nodes[node] == 0:
				server.load_task(node, task, nodeID)
				print "Added task %s to %s" % (additional_tasks[0], node)
				del additional_tasks[0]


		for item in monitor_nodes:
			if server.get_tasks(item) == 0:
				cx = cx - 1
			else:
				pass
		if cx == 0:
			break
	except KeyboardInterrupt or IndexError:
		break
index()

server.kill_node("control-node", nodeID)