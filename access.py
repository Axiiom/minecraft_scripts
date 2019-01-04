from mc_server import MC
from color import color
import mc_server
import docker
import os
import sys
client = docker.from_env()

def VALUEERROR():
	print("\r" + color.RED + "Invalid input detected!" + color.END)
	os.system("sleep .5")

def formatStatus(status):
	#for MC Server Status - spacing is important here because of the color codes.
	if status == "healthy":
		return color.GREEN + "Healthy  " + color.END
	elif status == "unhealthy":
		return "         "
	elif status == "starting":
		return color.YELLOW + "Starting " + color.END

	#for Container Status
	elif status == "running":
		return color.GREEN + "Running" + color.END
	elif status == "exited":
		return color.RED + "Exited" + color.END

def getServer():
	containers = client.containers.list(all)

	while True:
		try:
			choice = int(input(color.END + "\nWhich server would you like to access? " + color.RED))
			print(color.END)
			return containers[choice-1]
		except ValueError:
			VALUEERROR()
   
def printServerList():
	print(color.END + color.BOLD + "\nServers (\"ctrl+c\" to close):\n" + color.END)
	print(color.UNDERLINE + "%-3s | %-15s | %-8s | %-15s" % ("Num", "Name", "MC Status", "Container Status") + color.END)

	i = 1;
	for container in client.containers.list(all):
		server = MC(container)
		name   = server.name
		status = formatStatus(server.status())
		docker_status = formatStatus(container.status)
		
		print("%3d | %-15s | %-8s | %-15s" % (i, name, status, docker_status))
		i+=1

#Context-based options interface
def menu(server_choice):
	server = MC(server_choice)

	mc_status     = server.status()
	docker_status = server_choice.status
	name = server_choice.name
	
	os.system("clear")
	print()

	if(mc_status == "healthy"):
		server.printInformation()
		print(color.UNDERLINE + color.BOLD + "Menu options (\"ctrl+d\" to go back):" + color.END)
		print("1 | " + color.DARKCYAN + "Remote Connect [RCON]" + color.END + "\n2 | " + color.RED 
			+ "Stop" + color.END + "\n3 | " + color.YELLOW + "Restart" + color.END
			+ "\n4 | " + color.BOLD + "Logs\n" + color.END)
		choice = int(input("What would you like to do? " + color.RED))

		print(color.END)
		if(choice == 1):
			server.rcon()
		if(choice == 2):
			try:
				server.save()
				server.say("Server stopping in 5 seconds...")
				os.system("sleep 5")
				server.stop(0)
				return True
			except ValueError:
				VALUEERROR()
			except EOFError:
				print()
		if(choice == 3):
			try:
				server.save()
				server.say("Server restarting in 5 seconds...")
				os.system("sleep 5")
				server.restart(0)
			except ValueError:
				VALUEERROR()
			except EOFError:
				print()
		if(choice == 4):
			server.attachLogs()

	if(mc_status == "starting"):
		server.attachLogs()
			
	if(mc_status == "unhealthy" and docker_status == "exited"):
		server.printInformation()
		print(color.UNDERLINE + color.BOLD + "\nMenu options (\"ctrl+d\" to go back):" + color.END)
		print("1 | " + color.GREEN + "Start\n" + color.END)

		choice = int(input("What would you like to do? " + color.RED))
		if(choice == 1):
			print(color.END + "Starting server...")
			server.start()

def main():
	os.system("clear")
		
	while True:
		os.system("clear")
		printServerList()
		try:
			server_choice = getServer()
		except KeyboardInterrupt:
			print(color.YELLOW + "\nExiting script...\n" + color.END)
			os.system("sleep .5")
			sys.exit(0)
		except:
			print(color.END)
			return

		while(True):
			try:
				menu(server_choice)
				break
			except KeyboardInterrupt:
				print(color.YELLOW + "\nExiting script...\n" + color.END)
				os.system("sleep .5")
				sys.exit(0)
			except EOFError:
				print(color.END)
				break
		
if __name__ == '__main__':
    main()
