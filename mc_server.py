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
		self.is_running = (container.status == "running")


	#restarts the container
	def restart(self, delay):
		if(self.is_running):
			self.container.restart(timeout=delay)


	#stops the container
	def stop(self, delay):
		if(self.is_running):
			self.container.stop(timeout=delay)


	#calls save on the servers' rcon-cli
	def save(self):
		if(self.is_running):
			self.rcon_call_loud("save-all")


	#starts the container
	def start(self):
		if(not self.is_running):
			self.container.start()


	#calls "message" on this servers' rcon-cli and prints the result to the console
	def rcon_call_loud(self, message):
		if(self.is_running):
			os.system("docker exec " + self.name + " rcon-cli " + message)


	#calls "message" on this servers' rcon-cli and returns the result
	def rcon_call(self, message):
		if(self.is_running):
			return os.popen("docker exec " + self.name + " rcon-cli " + message).readlines()


	#interactively calls "message" on this servers' rcon-cli and returns the result
	def rcon_call_interactive(self, message):
		if(self.is_running):
			return os.popen("docker exec -i" + self.name + " rcon-cli " + message).readlines()


	#writes "message" to the server using rcon-cli
	def say(self, message):
		if(self.is_running):
			os.system("docker exec -i " + self.name + " rcon-cli say " + message)


	#gets the current player count of the server as a string
	def getPlayerCount(self):
		if(self.is_running):
			raw_playercount = self.rcon_call("list")[0]
			playercount = raw_playercount.replace("There are ","").replace(" of a max ","/").replace(" players online: "," | ")
			index_of_break = playercount.find(" | ")
			try:
				playercount[index_of_break + 4]
				return playercount
			except:
				return playercount.replace(" | ","")


	#gets the version of the server
	def getVersion(self):
		if(self.is_running):
			output  = os.popen("docker exec " + self.name + " mcstatus localhost status").readlines()
			version = output[0].replace("version: ", "")
			return version.strip()


	# prints current server information to the console in the format:
	# 
	# +-------------+
	# | server_name |
	# +-------------+
	# Version: xxxxxx
	# Players: xxxxxx
	def printInformation(self):
		print_with_border(self.name)
		version = self.getVersion()
		players = self.getPlayerCount()

		if(version):
			print("Version: %s" % (version))
		if(players):
			print("Players: %s" % (players))


	#prints and attaches to this servers' logs
	def attachLogs(self):
		if(self.is_running):
			print(color.END)
			os.system("docker logs -f " + self.name)


	#prints this servers' logs
	def printLogs(self):
		if(self.is_running):
			print(color.END)
			os.system("docker logs " + self.name)


	#attaches to this servers' rcon-cli
	def rcon(self):
		if(self.is_running):
			print(color.END + "\nAcessing [RCON] for " + color.CYAN + self.name + color.END + "... (\"ctrl+c\" or \"ctrl+d\" to exit)")
			os.system("docker exec -i " + self.name + " rcon-cli")


	#gets the status of the docker container
	def status(self):
		output = os.popen("docker container inspect -f \"{{.State.Health.Status}}\" " + self.name).readlines()
		status = output[0].strip('\n')
		return status
