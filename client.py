import xmlrpc.client
x = xmlrpc.client.ServerProxy("http://192.168.128.9:8000")
print(x.login("eugene","eeo-jun"))