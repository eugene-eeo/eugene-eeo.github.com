#!/usr/local/bin/python3
import cgi, crypt, os, time, socket
user_css = """
a {color:blue;}
\nbody {padding:5px; width: 750px; margin:auto; font-family: Times New Roman; font-size:12pt;}\n
h2 {margin-bottom: 5px;}\ncode {font-size: 1em; font-family:monospace;}\ntable {font-size: inherit;}\ncode{font-family:Menlo,monospace; font-size:10pt;}
textarea {width:100%; margin-top:5px;}\ninput {font-family:monospace;}\nrfc {font-family:Menlo, monospace; font-size:10pt;} g {color:#4AA02C;}
"""
action = False; query = False

users = {"admin" : "eugene-eeo"}
data = {"eugene-eeo" : "12345678" }
official_users = {
	#secret : #displayed name
}

if not os.path.isdir("rfc"):
	os.mkdir("rfc")

client_ip =  cgi.escape(os.environ["REMOTE_ADDR"])

def welcome_message():
	me = """Welcome to my RFC server."""
	return me

def create(contents, username):
	username = username.replace("<","&lt;")
	username = username.replace(">","&gt;")
	try:
		username = username.split("[")[1]
		username = username.split("]")[0]
		if username in official_users:
			username = "<g>" + official_users[username] + "</g>"
	except IndexError:
		pass
	filename = "RFC" + str(len(os.listdir("rfc")))
	if os.path.exists("rfc/%s" % (filename)):
		filename = "RFC" + str(len(os.listdir("rfc")) + 1)
	rfc = open("rfc/%s" % (filename),"w")
	if "<g>" not in username:
		username = username + " [%s]" % (client_ip)
	rfc.write("Author: %s\nSubmitted: %s" % (username, time.asctime()))
	rfc.write("\n%s" % (contents))
	rfc.close()
	return True

def get_env():
	global action, username, password, query, content, author, to_read
	try:
		to_read = cgi.FieldStorage().getlist("read")[0]
	except:
		to_read = False
	try:
		action = cgi.FieldStorage().getlist("action")[0]
	except:
		action = False
	try:
		query = cgi.FieldStorage().getlist("search")[0]
	except:
		query = False
	try:
		username = cgi.FieldStorage().getlist("username")[0]
	except:
		username = False
	try:
		password = cgi.FieldStorage().getlist("password")[0]
	except:
		password = False
	try:
		author = cgi.FieldStorage().getlist("author")[0]
	except:
		author = False
	try:
		content = cgi.FieldStorage().getlist("content")[0]
	except:
		content = False

def logged_in():
	global logged_in
	get_env()
	if password and username:
		if password == admin_pass and username == admin_username:
			logged_in = True
			return True
		else:
			logged_in = False
			return False
	else:
		logged_in = False
		return False

print ("Content-type: text/html\n")
get_env()
logged_in = True
print ("<html>\n<head><style type='text/css'>%s" % (user_css))
print ("</style>\n<title>Web-RFC</title>\n</head>\n")
print ("<body>")
print ("<h2><a href='http://%s:8600/main.py'>Atis-RFC</a> Web Interface</h2>" % (socket.gethostbyname(socket.gethostname())))
try:
	if logged_in:
		print ("<a href='http://%s:8600/main.py?action=index'>Index</a> | <a href='http://%s:8600/main.py?action=edit'>Author</a>" % (socket.gethostbyname(socket.gethostname()),socket.gethostbyname(socket.gethostname())))
		print ("| <form style='display:inline;'>Search: <input type='text' name='search'></form>")
except NameError:
	pass
print ("<hr/>")

if to_read == False and action == False and author == False and query == False:
	print ("""<h3>Welcome to Atis-RFC</h3>
	<p>
	This is a server which allows absolutely anyone to create either anonymous RFCs (Request For Comments, or just documents) and submit them
	onboard the server. Though there are generally no formatting rules (apart from no HTML), for an overview of the formatting rules, please check
	<a href="http://%s:8600/main.py?read=RFC6">RFC6</a>.
	<p>
	RFCS authored by anonymous sources are black, while RFCs published by official authors are in <g>green</g>.
		""" % (socket.gethostbyname(socket.gethostname())))

try:
	if action == "login":
		logged_in = False
		login_form()


	if action == "index" and logged_in:
		print ("<table cellspacing='10' align='left'>")
		for item in os.listdir('rfc'):
			if item != ".DS_Store":
				print ("<tr>")

				print ("<td align='left'>")
				print ("[<a href='http://%s:8600/main.py?read=%s'>%s</a>]" % (socket.gethostbyname(socket.gethostname()),item, item))
				print ("</td>")
				x = open("rfc/%s" % (item), "r").read()
				author = x.split("Author: ")[1]
				author = author.split("\n")[0]

				print ("<td align='left'>")
				print ("<code>%s</code>" % (author))
				print ("</td>")
				times = x.split("Submitted: ")[1]
				times = times.split("\n")[0]

				print ("<td>")
				print (times)
				print ("</td>")
				print ("</tr>")
		print ("</table>")

	elif action == "edit" and logged_in:
		print ("<form>")
		print ("Author: <input type='text' name='author'><br/>")
		print ("<textarea rows='15' name='content'>\nType away.")
		print ("</textarea>")
		print ("<input type='submit' value='Submit'>")
		print ("</form>")

except NameError:
	print ("HAHA")

try:
	if query != False:
		print ("<h3>Search Results for \"<span style='font-weight:normal;'><g>%s</g></span>\":</h3>\n<ul>" % (query))
		results = 0
		for item in os.listdir("rfc"):
			if item != ".DS_Store":
				c = open("rfc/%s" % (item),"rt").read()
				if query in c:
					print ("<li><a href='http://" + socket.gethostbyname(socket.gethostname()) + ":8600/main.py?read=" + item + "'>" + item + "</a></li>")
					results = results + 1
				if query in item or item in query:
					print ("<li><a href='http://" + socket.gethostbyname(socket.gethostname()) + ":8600/main.py?read=" + item + "'>" + item + "</a></li>")
					results = results + 1
		print ("</ul>")
		if results == 0:
			print ("No results found.")
except NameError:
	pass

try:
	if content and author and logged_in:
		if create(content, author):
			print ("<p>RFC Successfully created.")
		else:
			print ("<p>Please retry in creating the RFC.")
except NameError:
	pass

try:
	if to_read:
		try:
			cont = open("rfc/%s" % (to_read),"r").read()
			author = cont.split("Author: ")[1]
			author = author.split("Submitted: ")[0]
			submitted = cont.split("Submitted: ")[1]
			submitted = submitted.split("\n")[0]
			cont = cont.split(submitted)[1]
			cont = cont.replace("<","&lt;")
			cont = cont.replace(">","&gt;")
			cont = cont.replace("[?pre?]","<pre>")
			cont = cont.replace("[?/pre?]","</pre>")
			cont = cont.replace("\n","<br/>")
			print ("<rfc>")
			print ("Author: <b>",author,"</b>")
			print ("<br/>Submitted: <b>",submitted,"</b><br/>")
			print (cont)
			print ("</rfc>")
		except IOError:
			print ("RFC not found.")
		print ('<hr/>\n<p><center>[<a href="http://' + socket.gethostbyname(socket.gethostname()) + ':8600/main.py?action=index">Back to Index</a>]</center>')
except NameError:
	pass
print ("</body></html>")