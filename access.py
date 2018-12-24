from io import StringIO
import docker
import os
import sys
client = docker.from_env()

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_with_border(txt):
	text = txt.splitlines()
	maxlen = max(len(s) for s in text)
	colwidth = maxlen+2

	print('+' + '-'*colwidth + '+')
	for s in text:
		print('| %-*.*s |' % (maxlen, maxlen, s))

	print('+' + '-'*colwidth + '+')

class mc_server:
	def __init__(self, container):
		self.container = container
		self.name = container.name
	def restart(self, delay):
		self.say("Server will restart in " + str(delay) + " seconds...")
		self.container.restart(timeout=delay)
	def stop(self, delay):
		self.say("Server will stop in " + str(delay) + " seconds...")
		self.container.stop(timeout=delay)
	def start(self):
		self.container.start()
	def say(self, message):
		os.system("docker exec -i " + self.name + " rcon-cli say " + message)
	def printInformation(self):
		print_with_border(self.name)
		output = os.popen("docker exec " + self.name + " mcstatus localhost status").readlines()
		print("-> " + output[0] + "-> " + output[2])
	def printLogs(self):
		print(color.END)
		os.system("docker logs -f " + self.name)
	def rcon(self):
		print(color.END + "\nAcessing [RCON] for " + color.CYAN + self.name + color.END + "...")
		os.system("docker exec -i " + self.name + " rcon-cli")
	def status(self):
		output = os.popen("docker container inspect -f \"{{.State.Health.Status}}\" " + self.name).readlines()
		status = output[0]
		if status == "healthy\n":
			return color.GREEN + "healthy" + color.END
		elif status == "unhealthy\n":
			return color.RED + "unhealthy" + color.END
		elif status == "starting\n":
			return color.YELLOW + "starting" + color.END
	def status_no_format(self):
		output = os.popen("docker container inspect -f \"{{.State.Health.Status}}\" " + self.name).readlines()
		status = output[0]
		if status == "healthy\n":
			return "healthy"
		elif status == "unhealthy\n":
			return "unhealthy"
		elif status == "starting\n":
			return "starting"

def getServerChoice():
   containers = client.containers.list(all)
   choice     = int(input(color.END + "\nWhich server would you like to access? " + color.RED))
   print(color.END)
   
   return containers[choice-1]
   
def printServerList():
	print(color.END + color.BOLD + "\nServers:\n" + color.END)
	print(color.UNDERLINE + "%-3s | %-15s | %-15s" % ("Num", "Name", "Status") + color.END)

	i = 1;
	for container in client.containers.list(all):
		server = mc_server(container)
		name   = server.name
		status = server.status()
		
		print("%3d | %-15s | %-15s" % (i, name, status))
		i+=1

#Context-based options interface
def findMenuOptions(server_choice):
	server = mc_server(server_choice)

	mc_status = server.status_no_format()
	docker_status = server_choice.status
	name   = server_choice.name
	
	if(mc_status == "healthy"):
		print("1 | Remote Connect [RCON]\n2 | Stop\n3 | Restart\n4 | Logs\n6 | Go Back\n")
		choice = int(input("What would you like to do? " + color.RED))
		print(color.END)
		
		if(choice == 1):
			server.rcon()
		if(choice == 2):
			delay = int(input("Input the number in seconds that you would like to delay the server shutdown: "))
			server.stop(delay)
		if(choice == 3):
			delay = int(input("Input the number in seconds that you would like to delay the server shutdown: "))
			server.restart(delay)
		if(choice == 4):
			server.printLogs()

	if(mc_status == "starting"):
		print("1 | Logs\n2 | Go Back\n")
		choice = int(input("What would you like to do? " + color.RED))
		
		if(choice == 1):
			server.printLogs()
			
	if(mc_status == "unhealthy" and docker_status == "exited"):
		print("1 | Start\n2 | Go Back\n")
		choice = int(input("What would you like to do? " + color.RED))
		
		if(choice == 1):
			print(color.END + "Starting server...")
			server.start()

def main():
	try:
		os.system("clear")
		
		while True:
			os.system("clear")
			printServerList()
			server_choice = getServerChoice()
			print(color.UNDERLINE + color.BOLD + "Menu for " + "\'" + server_choice.name + "\'" + color.END)
			findMenuOptions(server_choice)
	except KeyboardInterrupt:
		print("\n")
		sys.exit(0)
	except:
		print(color.RED + "Error ~~~ Restarting script")
		os.system("sleep .5")
		os.system("python3 ~/scripts/minecraft/access.py")

		
if __name__ == '__main__':
    main()