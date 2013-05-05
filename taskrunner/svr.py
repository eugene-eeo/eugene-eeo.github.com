import xmlrpc.server, subprocess, os, threading, time, sys, signal
pid = {}
objects = {}
server_addr = ("localhost",8000)

class Core():
	global pid, objects
	# returns formatted time
	def _time(self):
		return time.strftime("\x1b[32m%H:%M:%S\x1b[0m")

	# logs output
	def _log(self, output, remote=True):
		print(output)
		return True

	# allows client to deploy a specific file onboard the
	# server
	def deploy(self, filename, contents):
		xname = filename
		while True:
			if os.path.exists(xname):
				xname = xname + "-23"
			else:
				break
		print ("\x1b[1m\x1b[32m>>\x1b[0m\x1b[1m Receiving binary: \x1b[32m%s\x1b[0m" % (xname))
		try:
			if open(xname,"w").write(contents):
				if xname == filename:
					return True
				else:
					return xname
			else:
				return False
		except IOError:
			return False

	# polls the queue for terminated tasks and updates the
	# process queue
	def _poll(self):
		while True:
			try:
				for item in objects:
					req = objects[item]
					if req.poll() != None:
						print("\x1b[1m\x1b[32m>>\x1b[0m \x1b[1mRemoving stacked task: \x1b[32m%s\x1b[0m" % (item))
						del objects[item]
						del pid[item]
			except RuntimeError:
				pass

	# runs a specified task
	def run_task(self, task):
		y = subprocess.Popen(task, shell=True)
		try:
			task = task.split(" ")[0]
		except ValueError:
			pass
		process_id = y.pid
		task = task + "-" + str(len(pid) + 1)
		objects[task] = y
		pid[task] = process_id
		self._log("\x1b[1mRunning task: \x1b[32m%s \x1b[0m\x1b[1m| PID: \x1b[32m%s\x1b[0m" % (task, process_id),remote=False)
		return True

	# gets the currently running tasks
	def get_task(self, task=False):
		if not task:
			return pid
		else:
			try:
				return pid[task]
			except KeyError:
				return False

	# kills a task
	def kill_task(self, task):
		try:
			if pid[task]:
				os.kill(int(pid[task]), signal.SIGKILL)
				del objects[task]
				del pid[task]
				self._log("\x1b[1m\x1b[32m>>\x1b[0m\x1b[1m Killed task: "+task+"\x1b[0m",remote=False)
				return True
			else:
				return False
		except KeyError:
			return False

svr = xmlrpc.server.SimpleXMLRPCServer(server_addr,requestHandler=xmlrpc.server.SimpleXMLRPCRequestHandler,logRequests=False)
svr.register_instance(Core())
sys.stdout.write("\x1b[1mStarted TaskRunner.Server at \x1b[32m%s\x1b[0m\x1b[1m:\x1b[32m%s\x1b[0m" % (server_addr[0], server_addr[1]))
sys.stdout.write(" | \x1b[1mRoot PID: %s\x1b[0m\n" % (os.getpid()))

worker = threading.Thread(target=Core()._poll)
worker.daemon = True

worker.start()
svr.serve_forever()