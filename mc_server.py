from color import color
import docker
import os
import sys

def print_with_border(txt):
	text = txt.splitlines()
	maxlen = max(len(s) for s in text)
	colwidth = maxlen+2

	print('+' + '-'*colwidth + '+')
	for s in text:
		print('| %-*.*s |' % (maxlen, maxlen, s))

	print('+' + '-'*colwidth + '+')

class MC:
	def __init__(self, container):
		self.container = container
		self.name = container.name
	def restart(self, delay):
		self.say("Server will restart in " + str(delay) + " seconds...")
		os.system("docker exec -i " + self.name + " rcon-cli save-all")
		os.system("sleep .5")
		self.container.restart(timeout=delay)
	def stop(self, delay):
		self.say("Server will stop in " + str(delay) + " seconds...")
		os.system("docker exec -i " + self.name + " rcon-cli save-all")
		os.system("sleep .5")
		self.container.stop(timeout=delay)
	def start(self):
		self.container.start()
	def say(self, message):
		os.system("docker exec -i " + self.name + " rcon-cli say " + message)
	def printInformation(self):
		output = os.popen("docker exec " + self.name + " mcstatus localhost status").readlines()
		print_with_border(self.name)
		print( "-> " + output[0] + "-> " + output[2])
	def printLogs(self):
		print(color.END)
		os.system("docker logs -f " + self.name)
	def rcon(self):
		print(color.END + "\nAcessing [RCON] for " + color.CYAN + self.name + color.END + "... (\"ctrl+c\" or \"ctrl+d\" to exit)")
		os.system("docker exec -i " + self.name + " rcon-cli")
	def status(self):
		output = os.popen("docker container inspect -f \"{{.State.Health.Status}}\" " + self.name).readlines()
		status = output[0]
		if status == "healthy\n":
			status = "healthy"
		elif status == "unhealthy\n":
			status = "unhealthy"
		elif status == "starting\n":
			status = "starting"
		return status
