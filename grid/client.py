import xmlrpclib

svr = xmlrpclib.Server("http://192.168.128.8:8000")
svr.delete_user("eugene")