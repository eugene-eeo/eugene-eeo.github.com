import BaseHTTPServer
import CGIHTTPServer
import socket
import cgitb; cgitb.enable()  ## This line enables CGI error reporting

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = (socket.gethostbyname(socket.gethostname()), 8600)
handler.cgi_directories = ['']

print "AEGIS Interface on", server_address[0] + ":" + str(server_address[1])
httpd = server(server_address, handler)
httpd.serve_forever()