import xmlrpclib
nodeID = "a"

server = xmlrpclib.Server('http://192.168.128.129:8000')
server.register_control(nodeID)
server.broadcast("control-node","haha")
print server.get_nodes(nodeID)
print server.receive_messages()
server.kill_control(nodeID)