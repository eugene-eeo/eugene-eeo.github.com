#!python3
import xmlrpc.server, socket, os, configparser, multiprocessing, sys, time, crypt
if not os.path.exists("user-config.txt"):
	open("user-config.txt","w")
if not os.path.exists("rfcs"):
	os.mkdir("rfcs")
admin_username = "admin"
admin_password = "123456789"
admin_password = crypt.crypt(admin_password, admin_password[-2:])

class Core:
	def create_user(self, username):
		try:
			os.mkdir(username)
			return True
		except OSError:
			return False

	def delete_user(self, username):
		try:
			import shutil
			shutil.rmtree(username)
			xs = open("user-config.txt").readlines()
			y = xs.index("[%s-config]\n"%(username))
			del xs[y+2]
			del xs[y+1]
			del xs[y]
			open("user-config.txt","w").write("")
			for line in xs:
				open("user-config.txt","a").write(line)
			return True
		except OSError:
			return False

	def register_user(self, username, password):
		for line in open("user-config.txt","r").readlines():
			if "[%s-config]" % (username) in line and line[0] == "[":
				return False
			else:
				pass
		password = crypt.crypt(password, password[-5:])
		open("user-config.txt","a").write("\n[%s-config]\nusername=%s\npassword=%s" % (username, username, password))
		return True

	def login_user(self, username, password):
		x = configparser.ConfigParser()
		password = crypt.crypt(password, password[-5:])
		x.read("user-config.txt")
		if str("%s-config" % (username)) in x.sections():
			if password == x["%s-config"%(username)]["password"]:
				return True
			else:
				print ("[%s] - Failed login attempt from user: %s." % (time.strftime("%H:%M:%S"),username))
				return False
		else:
			return False

class API():
	# copies all existing RFCs to the user's
	# inbox.
	def migrate(self, username, password):
		if Core().login_user(username, password) and os.path.exists(username):
			x = {}
			for item in os.listdir("rfcs"):
				if item != ".DS_Store":
					x[item] = open("rfcs/%s" % (item),"r").read()
			print (x)
			for item in x:
				filename = "%s/%s" % (username, item)
				number = 0
				while True:
					number = number + 1
					if os.path.exists(filename):
						filename = "%s/%s" % (username, item) + "[%s]" % (str(number))
					else:
						break
				open(filename,"w").write(x[item])
			print ("[%s] - User %s migrated RFCs" % (time.strftime("%H:%M:%S"),username))
			return True
		else:
			return False

	# reads an RFC
	def read_rfc(self, read_file):
		print ("[%s] - Requested RFC: %s" % (time.strftime("%H:%M:%S"), read_file))
		try:
			contents = open("rfcs/%s" % (read_file),"r").read()
			return contents
		except IOError:
			return False

	# gets a list of RFCs
	def get_rfc(self):
		results = []
		print ("[%s] - RFCs are requested" % (time.strftime("%H:%M:%S")))
		for item in os.listdir("rfcs"):
			if item != ".DS_Store":
				results.append(item)
		return results

	# submits an RFC
	def rfc(self, username, password, subject, contents):
		if Core().login_user(username, password):
			filename = "RFC-" + str(len(os.listdir("rfcs")))
			if os.path.exists(filename):
				filename = "RFC-" + str(len(os.listdir("rfcs")) + 1)
			rfc = open("rfcs/%s" % (filename),"w")
			# so that it's compatible with older 
			# versions of the CLI-client.
			rfc.write("Subject: %s\n" % (subject))
			rfc.write("Author: %s\n" % (username))
			rfc.write(contents)
			rfc.close()
			print ("[%s] - User: %s created RFC: %s" % (time.strftime("%H:%M:%S"), username, filename))
			return True
		else:
			return False

	# registers a user with username and password
	# as his/her login credentials
	def register(self, username, password):
		if username != "." and username != ".." and "@" not in username and ":" not in username and "," not in username and username != "rfcs" and len(password) > 7:
			if Core().register_user(username, password):
				Core().create_user(username)
				print("[" + time.strftime("%H:%M:%S") + "] - User %s has been registered" % (username))
				return True
			else:
				return False
		else:
			return False

	# removes a user from the server
	def remove(self, username, password):
		if Core().login_user(username, password):
			print("[" + time.strftime("%H:%M:%S") + "] - User %s has been removed" % (username))
			return Core().delete_user(username)
		return False

	# allows a user to receieve mail
	def recv(self, username, password):
		if Core().login_user(username, password):
			list_of_mail_items = []
			for item in os.listdir(username):
				if item != ".DS_Store":
					list_of_mail_items.append(item)
			print("[" + time.strftime("%H:%M:%S") + "] - User %s received mail items" % (username))
			return list_of_mail_items
		else:
			return False

	# allows a user to read a specific mail
	# item
	def read(self, username, password, mail):
		if Core().login_user(username, password) and os.path.exists("%s/%s" % (username, mail)):
			try:
				print("[" + time.strftime("%H:%M:%S") + "] - User %s accessed mail (%s)" % (username, mail))
				return open("%s/%s" % (username, mail),"r").read()
			except IOError:
				return False
		else:
			return False

	# allows the user to delete mail items
	def delete(self, username, password, mail):
		if Core().login_user(username, password) and os.path.exists("%s/%s" % (username, mail)):
			os.remove("%s/%s" % (username, mail))
			print("[" + time.strftime("%H:%M:%S") + "] - User %s deleted mail (%s)" % (username, mail))
			return True
		else:
			return False

	# displays a welcome message that can
	# be altered by the admin.
	def welcome_message(self):
		return ["aethermail","Welcome to ATIS, the first AetherMail server."]

	# allows a user to send mail
	def push(self, username, password, send_to, filename, content):
		if Core().login_user(username, password) and os.path.isdir(send_to):
			# now try and find if any replacements are needed in the mail message.
			try:
				include = content.split("<?include=\"")[1]
				include = include.split("\"?>")[0]
				try:
					ui = ""
					ux = open("%s/%s" % (username, include),"r").readlines()
					for line in ux:
						ui += "> " + line
					content = content.replace("<?include=\"%s\"?>" % (include),ui)
				except IOError:
					pass
			except:
				pass
			write_file = username + "[" + filename + "]" + str(len(os.listdir(username)) + 1)
			if not os.path.exists("%s/%s" % (send_to, write_file)):
				pass
			else:
				write_file = username + "[" + filename + "]" + "c" + str(len(os.listdir(username)) + 1)
			file_object = open("%s/%s"%(send_to,write_file),"wb")
			file_object.write(bytes("Subject: %s\n"%(filename),"UTF-8"))
			file_object.write(bytes("Author: %s\n"%(username),"UTF-8"))
			file_object.write(bytes("%s" % (content),"UTF-8"))
			file_object.close()
			print("[" + time.strftime("%H:%M:%S") + "] - User %s pushed mail (%s) to %s" % (username, filename, send_to))
			return True
		else:
			return False

c = xmlrpc.server.SimpleXMLRPCServer((socket.gethostbyname(socket.gethostname()),8000),
	requestHandler=xmlrpc.server.SimpleXMLRPCRequestHandler, logRequests=False)
c.register_instance(API())
try:
	print("[" + time.strftime("%H:%M:%S") + "] - Started server at http://%s:8000" % (socket.gethostbyname(socket.gethostname())))
	c.serve_forever()
except KeyboardInterrupt:
	print ("Have a good day.")
	exit()