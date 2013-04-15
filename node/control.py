import xmlrpclib, socket
nodeID = ""
svr_con = False

class initialize():
	# check if the server variable is defined
	# or remains False.
	def __init__(self):
		if svr_con:
			pass
		else:
			return False

	# is the main shell.
	def shell(self):
		while True:
			command = raw_input("> ")
			try:
				call, args = command.split(":")
				if call == "load":
					try:
						node, task = args.split("=")
						if server.load_task(node, task, nodeID):
							print "Loaded Task %s at node: %s" % (task, node)
					except ValueError:
						print "Invalid Parameters."
				elif call == "create":
					if server.create_node(args, nodeID):
						print "Created node: %s" % (args)
				elif call == "status":
					x = server.get_status(args, nodeID)
					if x:
						print "%s status: %s" % (args, x)
					else:
						print "Cannot get status of node: %s" % (args)
				elif call == "kill":
					if server.kill_node(args, nodeID):
						print "Killed node: %s" % (args)
					else:
						print "Node is not killed."
				else:
					print "Invalid Command."

			except ValueError:
				if command == "exit":
					server.kill_control(nodeID)
					exit()
				elif command == "list":
					n = server.get_nodes(nodeID)
					if n:
						for item in n:
							print "Stack [%s]:" % (item)
							if n[item] == nodeID:
								print "    Controller Node"
							else:
								for item in n[item]:
									print "    " + item
				else:
					print "Invalid Command."

print ("Control Node Interface (CNI) v0.0.1 (10 4 2013)")
print ("Written by Eugene Eeo [http://eugene-eeo.github.com]")
svr_url = str(raw_input("Server URL: "))
port = str(raw_input("Server Port: "))
try:
	server = xmlrpclib.Server('%s:%s' % (svr_url, port))
	nodeID = raw_input("Node ID: ")
	if server.register_control(nodeID):
		print "Registred as Control Node. at %s" % (svr_url)
		svr_con = True
		initialize().shell()
	else:
		print "Cannot register as Control Node."
except socket.error as error:
	print str(error)