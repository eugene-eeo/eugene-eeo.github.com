import xmlrpclib
nodeID = "7e461c30-a191-11e2-9e96-0800200c9a66"

server = xmlrpclib.Server('http://localhost:8000')
server.register_control(nodeID)
server.create_node("slave", nodeID)
server.load_task("slave","git status",nodeID)
server.load_task("slave","git push",nodeID)
server.load_task("slave","git --version", nodeID)
print server.get_nodes(nodeID)