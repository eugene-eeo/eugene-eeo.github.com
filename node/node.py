# import necessary modules- in this case, only the
# XMLRPCServer and socket is required.
import SimpleXMLRPCServer, socket, time
nodes = {}
control_node = "a"
node_status = {}

# functions to interact with the client-side nodes
class NodeFunctions:
	global nodes, node_status
	# checks if the control node is still present
	def _control_present(self):
		try:
			nodes["control-node"]
			return True
		except KeyError:
			return False

	# lets the control node know if the selected
	# node is offline or online.
	def get_status(self, node, node_id):
		if node_id==control_node and self._control_present():
			try:
				return node_status[node]
			except KeyError:
				return False
		return False

	# reports to the server that the current node is
	# offline.
	def node_is_offline(self, node_name):
		if self._init_node(node_name):
			node_status[node_name]="offline"
			return True
		else:
			return False

	# required for fancy output.
	def get_server_name(self):
		return socket.gethostbyname(socket.gethostname())

	# registers the node and is basic authentication
	# function, and returns data for that node only.
	def _init_node(self, node):
		try:
			nodes[node]
			return node
		except KeyError:
			return False

	# gets the tasks a slave node is supposed to do
	# and execute. Returns a list or False for
	# easy boolean parsing.
	def get_tasks(self, node):
		if self._init_node(node)==node and self._control_present():
			node_status[node]="online"
			return nodes[node]
		else:
			return False

	# creates a new node, only callable by the control
	# node/centre.
	def create_node(self, node_name, node_id):
		if node_id == control_node:
			nodes[node_name] = []
			node_status[node_name] = "unknown"
			return True
		else:
			return False


	# kills the node.
	def kill_node(self, node_name, node_id):
		global nodes
		if node_id == control_node and self._init_node(node_name)!=None and self._control_present():
			nodes[node_name] = "killed"
			node_status[node_name] = "killed"
			return True
		else:
			return False

	# registers a control node, but there can only
	# be one node.
	def register_control(self, node_id):
		if node_id == control_node:
			try:
				if nodes["control-node"]:
					return False
			except KeyError or IndexError:
				nodes["control-node"] = node_id
				return True
		else:
			return False

	# gets a list of nodes
	def get_nodes(self, node_id):
		if control_node == node_id and self._control_present():
			return nodes
		else:
			return False

	# checks if the node is online.
	def is_node(self, node_name):
		try:
			nodes[node_name]
			return True
		except KeyError:
			return False


	# tells the server a node has finished a task
	def finish(self, node, task):
		try:
			if self._init_node(node)!=None and nodes[node]!="killed" and task in nodes[node]:
				try:
					c = nodes[node]
					del c[c.index(task)]
					return True
				except KeyError or TypeError:
					return False
			else:
				return False
		except IndexError:
			return False

	# load a new task. only callable by the control
	# centre.
	def load_task(self, node, task, node_id):
		try:
			if node_id == control_node and self._init_node(node)!=False and self._control_present():
				task += ""
				c = nodes[node]
				c.append(task)
				return True
			else:
				return False
		except TypeError or KeyError:
			return False

	# kills the control node to make way for another
	# control node. Is very forceful and painful.
	def kill_control(self, node_id):
		if node_id == control_node:
			self.kill_node("control-node", node_id)
			return True
		else:
			return False

server = SimpleXMLRPCServer.SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()), 8000))
server.register_instance(NodeFunctions())
print "Node Server 0.0.1 Running at %s" % (socket.gethostbyname(socket.gethostname()))
print "Written by eugene-eeo [eugene-eeo.github.com]"
server.serve_forever()