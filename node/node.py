# import necessary modules- in this case, only the
# XMLRPCServer and socket is required.
import SimpleXMLRPCServer, socket
nodes = {}
control_node = "7e461c30-a191-11e2-9e96-0800200c9a66"

# functions to interact with the client-side nodes
class NodeFunctions:
	global nodes

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
			return None

	# gets the tasks a slave node is supposed to do
	# and execute. Returns a list or False for
	# easy boolean parsing.
	def get_tasks(self, node):
		if self._init_node(node)==node:
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
		if node_id == control_node and self._init_node(node)!=None:
			try:
				del nodes[node_name]
				return True
			except:
				return False
		else:
			return False

	# registers a control node
	def register_control(self, node_id):
		if node_id == control_node and self._init_node("control-node")==None:
			nodes["control-node"] = "control"
			return True
		else:
			return False

	# gets a list of nodes
	def get_nodes(self, node_id):
		if node_id == control_node:
			return nodes
		else:
			return None

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
			c = nodes[node]
			del c[c.index(task)]
			return True
		else:
			return False

	# load a new task. only callable by the control
	# centre.
	def load_task(self, node, task, node_id):
		try:
			if node_id == control_node and self._init_node(node)!=None:
				task += ""
				c = nodes[node]
				c.append(task)
				return True
			else:
				return False
		except TypeError or KeyError:
			return False

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(NodeFunctions())
server.serve_forever()