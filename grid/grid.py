import SimpleXMLRPCServer, socket, ConfigParser, os, shutil

class ClientError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Core():
	# deletes a user
	def delete_user(self, username, password=False):
		config = ConfigParser.SafeConfigParser().readfp(open("%s/.config-cfg" % (username)))
		del_user = False
		s = config.get("user-config","password")
		if s == "None":
			del_user = True
			pass
		else:
			if password == s:
				del_user = True
			else:
				del_user = False
				raise ClientError("Invalid password")
				return False
		if del_user:
			shutil.rmtree(username)
			return True
		return False

	# lets the server recieve data or download things
	def recieve_data(self, username, filename, data):
		try:
			open("%s/%s" %(username, filename), "wb").write(data)
			return True
		except IOError or OSError:
			return False

	# creates a user in the current directory
	def create_user(self, username, password=False):
		string = '[user-config]\npassword=%s'
		if password == False:
			string = string % ("None")
			pass
		else:
			string = string % (hash(str(password)))
		if os.path.exists(username) and os.path.isdir(username):
			return False
		else:
			os.mkdir(username)
			open("%s/.config-cfg" % (username),"w").write(string)
		return True


server = SimpleXMLRPCServer.SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()), 8000))
server.register_instance(Core())
print ("Serving XMLRPC at %s:8000" % (socket.gethostbyname(socket.gethostname())))
server.serve_forever()