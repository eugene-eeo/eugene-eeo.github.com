# import necessary modules- in this case, only the
# XMLRPCServer and socket is required.
import SimpleXMLRPCServer, socket, random, time
nodes = {}
control_node = "a"


# functions to interact with the client-side nodes
class NodeFunctions:
	global nodes

	# checks if the control node is still present
	def _control_present(self):
		try:
			nodes["control-node"]
			return True
		except KeyError:
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
			return nodes[node]
		else:
			return False

	# creates a new node, only callable by the control
	# node/centre.
	def create_node(self, node_name, node_id):
		if node_id == control_node:
			nodes[node_name] = []
			return True
		else:
			return False

	# kills the node.
	def kill_node(self, node_name, node_id):
		global nodes
		if node_id == control_node and self._init_node(node_name)!=None and self._control_present():
			try:
				del nodes[node_name]
				return True
			except:
				return False
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
		if self._init_node(node)!=None and task in nodes[node]:
			try:
				c = nodes[node]
				del c[c.index(task)]
				return True
			except KeyError:
				return False
		else:
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
			kill_node("control-node")
			return True
		else:
			return False

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(NodeFunctions())
server.serve_forever()