#!/usr/bin/env python
import web 
import subprocess
import datetime
import setproctitle

# Redirects URL from GET-command to the corresponding file including input arguments 
urls = ( '/','index',
		 '/favicon.ico','icon')

# create template objet with path as input
render = web.template.render('templates/', base="layout")

setproctitle.setproctitle("raspControl")    

# Class defintion for logfile
class Log:
        array = []
        def __init__(self):
                array =[]
        def add(self,msg):
                timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
                self.array.append("["+ timestamp + "]..." + msg)
        def printlog(self):
                for i in self.array:
                        print i
	def get(self):
		return self.array
	def clear(self):
		self.array=[]
                timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
                self.array.append("["+ timestamp + "]...INFO: Log cleared.")
		return self.array

# Process favicon.ico requests
class icon:
    def GET(self): raise web.seeother("/static/favicon.ico")
	
# Command class	
class Cmd:
	dict = {}
        filename = "cmd_dict.txt"
        sep = " : "
	def __init__(self):
		with open(self.filename, "r") as f:
        		for line in f:
            			values = line.split(self.sep)
       				self.dict.update({values[0]:values[1]})
	def __len__(self):
		return len(self.dict)
	def get(self,value):
		return self.dict[value]
	def keys(self):
		print self.dict.keys()
	def reload(self):
                with open(self.filename, "r") as f:
                        for line in f:
                                values = line.split(self.sep)
                                self.dict.update({values[0]:values[1]})

# Defintion main class with index.html as main site
class index:
    log = Log()
    log.add("INFO: Server started")
    cmd = Cmd()
    log.add("INFO: " + str(len(cmd)) + " commands loaded")
    def GET(self):
        return render.index(self.log.get())
    def POST(self):
        form = web.input() # Get value from button
        if form.value == "cmds_reload":
		self.cmd.reload()
		self.log.add("INFO: " + str(len(self.cmd)) + " commands loaded")
        elif form.value == "clear_log":
		self.log.clear()
        else:
		value = self.cmd.get(form.value) # redirect value to command
		self.log.add("SEND: " + form.value)
		ans = subprocess.Popen(value, shell=True, stdout=subprocess.PIPE).stdout.read()
		self.log.add("ANSWER: " + ans)
        return render.index(self.log.get()) # Call url parse with input argument value

# Start webserver
if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()


