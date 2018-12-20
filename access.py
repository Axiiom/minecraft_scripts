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

def rconSay(server_choice, message):
	os.system("docker exec -i " + server_choice.name + " rcon-cli say " + message)

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
		status = container.status
		name   = container.name
		
		if status == "restarting":
			status = color.DARKCYAN + status + color.END
		if status == "running":
			status = color.GREEN + status + color.END
		if status == "exited":
			status = color.RED + status + color.END
		
		print("%3d | %-15s | %-15s" % (i, name, status))
		i+=1

def restartServer(server_choice):
	choice = int(input(color.END + "How many seconds would you like to delay the server restart by? " + color.RED))
	rconSay(server_choice, ("Restarting server in " + str(choice) + " seconds..."))
	server_choice.restart(timeout=choice)
	
def stopServer(server_choice):
	choice = int(input(color.END + "How many seconds would you like to delay the shutdown of the server by? " + color.RED))
	rconSay(server_choice, ("Shutting down the server in " + str(choice) + " seconds..."))
	server_choice.stop(timeout=choice)

def startServer(server_choice):
	server_choice.start()
	
#def stopServer(server_choice):


def findMenuOptions(server_choice):
	status = server_choice.status
	name   = server_choice.name
	
	if(status == "running"):
		print("1 | Remote Connect [RCON]\n2 | Stop\n3 | Restart\n4 | Logs\n5 | Save\n6 | Go Back\n")
		choice = int(input("What would you like to do? " + color.RED))
		
		if(choice == 1):
			print(color.END + "\nAcessing [RCON] for " + color.CYAN + name + color.END + "...")
			os.system("docker exec -i " + name + " rcon-cli")
		if(choice == 2):
			stopServer(server_choice)
		if(choice == 3):
			restartServer(server_choice)
		if(choice == 4):
			print(color.END)
			os.system("docker logs -f " + name)
		if(choice == 5):
			print(color.END)
			os.system("docker exec -i " + name + " rcon-cli save-all")
		else:
			return False
			
	if(status == "exited"):
		print("1 | Start\n2 | Go Back\n")
		choice = int(input("What would you like to do? " + color.RED))
		
		if(choice == 1):
			print(color.END + "Starting server...")
			startServer(server_choice)
		if(choice == 2):
			return False

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
		os.system("sleep 1")
		os.system("python3 ~/scripts/minecraft/access.py")

		
if __name__ == '__main__':
    main()