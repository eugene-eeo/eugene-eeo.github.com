#!/usr/local/bin/python3
import xmlrpc.client, sys, os, getpass, crypt
username = ""; password = ""; server_address = "";
print ("AetherMail Client 0.1.2 [OSX 10.6.8+]")
def connect(server_address):
	global x
	x = xmlrpc.client.ServerProxy(server_address, encoding="utf8")
	message = x.welcome_message()
	if message[0] == "aethermail":
		print(message[1])
	else:
		print("Server type is not aethermail.")
		print("Press enter to proceed, or control+c to exit.")
		input()

def login():
	global username, password, server_address
	username = input("  \x1b[1mUsername:\x1b[0m\x1b[36m ")
	password = getpass.getpass("\x1b[0m  \x1b[1mPassword:\x1b[0m ")
	password = crypt.crypt(password, password[-2:])
	server_address = input("    \x1b[1mServer:\x1b[0m \x1b[36m")
	sys.stdout.write("\x1b[0m")
	try:
		connect(server_address)
	except:
		print ("[\x1b[31m!\x1b[0m] Bad Connection.")
		exit()

try:
	if sys.argv[1] == "send:rfc":
		os.system("vi send_rfc.txt")
		content = open("send_rfc.txt","r").read()
		login()
		title = input("   Subject: ")
		if x.rfc(username, password, title, content):
			print ("RFC submitted.")
			os.remove("send_rfc.txt")
		else:
			print ("RFC is not submitted.")

	elif sys.argv[1] == "get:rfc":
		login()
		for item in x.get_rfc():
			c = x.read_rfc(item)
			sujet = c.split("Subject: ")[1]
			sujet = sujet.split("\nAuthor: ")[0]
			author = c.split("Author: ")[1]
			author = author.split("\n")[0]
			xsls = c.split(author+"\n")[1:]
			content = ""
			for line in xsls:
				content += line
			print ("\nSubject:\x1b[1m " + sujet + "\x1b[0m")
			print ("Author:\x1b[1m " + author + "\x1b[0m")
			content = content.replace("<u>","\x1b[4m")
			content = content.replace("</u>","\x1b[0m")
			content = content.replace("<g>","\x1b[32m")
			content = content.replace("</g>","\x1b[0m")
			content = content.replace("<b>","\x1b[1m")
			content = content.replace("</b>","\x1b[0m")
			print (content)
		
	elif sys.argv[1] == "send":
		os.system("vi send_text.txt")
		content = open("send_text.txt","r").read()
		login()
		title = input("   Subject: ")
		send_to = input("   Send to: ")
		if x.push(username, password, send_to, title, content):
			print ("Message sent.")
			os.remove("send_text.txt")
		else:
			print ("Message not sent.")

	elif sys.argv[1] == "deactivate":
		login()
		if x.remove(username, password):
			print ("Successfully removed account.")
		else:
			print ("Account is not removed.")

	elif sys.argv[1] == "register":
		print ("Usernames cannot be \".\" or \"..\".")
		print ("Passwords must be at least 7 characters long.")
		server_address = input("   Server Adddress: ")
		username = input("          Username: ")
		password = getpass.getpass("  Desired Password: ")
		pass2 = getpass.getpass("  Confirm Password: ")
		if pass2 == password:
			connect(server_address)
			password = crypt.crypt(password, password[-2:])
			if x.register(username, password):
				print ("Registered user: %s" % (username))
			else:
				print ("Error during registration. You may have")
				print ("registered?")
		else:
			print ("Passwords do not match.")

	elif sys.argv[1] == "get":
		login()
		mails = x.recv(username, password)
		try:
			iter(mails)
			for item in mails:
				try:
					print("\nMailfile:\x1b[36m",item,"\x1b[0m")
					c = x.read(username, password, item)
					sujet = c.split("Subject: ")[1]
					sujet = sujet.split("\nAuthor: ")[0]
					author = c.split("Author: ")[1]
					author = author.split("\n")[0]
					xsls = c.split(author+"\n")[1:]
					content = ""
					for line in xsls:
						content += line
					print ("Subject:\x1b[1m " + sujet + "\x1b[0m")
					print ("Author:\x1b[1m " + author + "\x1b[0m")
					try:
						content = content.replace("<u>","\x1b[4m")
					except ValueError:
						pass
					try:
						content = content.replace("</u>","\x1b[0m")
					except ValueError:
						pass
					try:
						content = content.replace("<g>","\x1b[32m")
					except ValueError:
						pass
					try:
						content = content.replace("</g>","\x1b[0m")
					except ValueError:
						pass
					try:
						content = content.replace("<b>","\x1b[1m")
					except ValueError:
						pass
					try:
						content = content.replace("</b>","\x1b[0m")
					except ValueError:
						pass
					print (content)
				except TypeError as error:
					print (str(error))
			if len(mails) == 0:
				print ("No mail for %s" % (username))
		except TypeError:
			print ("You are not authenticated. Perhaps you should")
			print ("retype your credentials.")

	elif sys.argv[1] == "delete":
		if sys.argv[2]:
			login()
			if sys.argv[2] != "<all>":
				if x.delete(username, password, sys.argv[2]):
					print ("Deleted %s." % (sys.argv[2]))
				else:
					print ("%s is not deleted." % (sys.argv[2]))
			elif sys.argv[2] == "<all>":
				d = x.recv(username, password)
				if d:
					for item in d:
						x.delete(username, password, item)
				else:
					print ("Not authenticated.")
		else:
			print ("Extra variable needed.")

	elif sys.argv[1] == "--help" or sys.argv[1] == "help":
		raise IndexError
	else:
		raise IndexError
except KeyboardInterrupt:
	print ("\n")
	exit()
except IndexError:
	print ("Usage: %s [command]" % (sys.argv[0]))
	print ("Where [command] is one of:")
	print ("               send  -  Sends a mail message.")
	print ("  delete [mailfile]  -  Deletes mail onboard the server.")
	print ("                get  -  Fetches and reads mail.")
	print ("           register  -  Registers an account on a server.")
	print ("         deactivate  -  Removes an account.")
	print ("            get:rfc  -  Gets RFCs.")
	print ("           send:rfc  -  Submits an RFC.")