from mc_server import mc_server
from color import color
import docker
import os
import sys
client = docker.from_env()

def VALUEERROR():
	print("\r" + color.RED + "Invalid input detected!" + color.END)
	os.system("sleep .5")

def formatStatus(status):
	if status == "healthy":
		return color.GREEN + "healthy" + color.END
	elif status == "unhealthy":
		return color.RED + "unhealthy" + color.END
	elif status == "starting":
		return color.YELLOW + "starting" + color.END


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
	print(color.END + color.BOLD + "\nServers:\n" + color.END)
	print(color.UNDERLINE + "%-3s | %-15s | %-15s" % ("Num", "Name", "Status") + color.END)

	i = 1;
	for container in client.containers.list(all):
		server = mc_server(container)
		name   = server.name
		status = formatStatus(server.status())
		
		print("%3d | %-15s | %-15s" % (i, name, status))
		i+=1

#Context-based options interface
def menu(server_choice):
	server = mc_server(server_choice)

	mc_status     = server.status()
	docker_status = server_choice.status
	name = server_choice.name
	
	os.system("clear")
	print()
	server.printInformation()
	print(color.UNDERLINE + color.BOLD + "Menu options (\"ctrl+d\" to go back):" + color.END)

	if(mc_status == "healthy"):
		print("1 | Remote Connect [RCON]\n2 | Stop\n3 | Restart\n4 | Logs\n")
		choice = int(input("What would you like to do? " + color.RED))

		print(color.END)
		if(choice == 1):
			server.rcon()
		if(choice == 2):
			try:
				delay = int(input("Input the number in seconds that you would like to delay the server shutdown: "))
				server.stop(delay)
			except ValueError:
				VALUEERROR()
			except EOFError:
				print()
		if(choice == 3):
			try:
				delay = int(input("Input the number in seconds that you would like to delay the server shutdown: "))
				server.restart(delay)
			except ValueError:
				VALUEERROR()
			except EOFError:
				print()
		if(choice == 4):
			server.printLogs()

	if(mc_status == "starting"):
		print("1 | Logs\n2 | Go Back\n")
		choice = int(input("What would you like to do? " + color.RED))
		
		if(choice == 1):
			server.printLogs()
			
	if(mc_status == "unhealthy" and docker_status == "exited"):
		print("1 | Start\n2 | Go Back\n")

		while(True):
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
		except:
			print(color.END)
			return

		while(True):
			try:
				menu(server_choice)
			except KeyboardInterrupt:
				print(color.YELLOW + "\nExiting script...\n" + color.END)
				os.system("sleep .5")
				sys.exit(0)
			except EOFError:
				print()
				break
		
if __name__ == '__main__':
    main()