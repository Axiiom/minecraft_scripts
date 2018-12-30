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
	print(color.END + color.BOLD + "\nServers (\"ctrl+c\" to close):\n" + color.END)
	print(color.UNDERLINE + "%-3s | %-15s | %-15s" % ("Num", "Name", "Status") + color.END)

	i = 1;
	for container in client.containers.list(all):
		server = MC(container)
		name   = server.name
		status = formatStatus(server.status())
		
		print("%3d | %-15s | %-15s" % (i, name, status))
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
				delay = int(input("Input the number in seconds that you would like to delay the server shutdown: "))
				server.stop(delay)
				return True
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
			os.system("sleep 5")

	if(mc_status == "starting"):
		mc_server.print_with_border(name)
		print(color.UNDERLINE + color.BOLD + "\nMenu options (\"ctrl+d\" to go back):" + color.END)
		print("1 | " + color.BOLD + "Logs\n" + color.END)
		choice = int(input("What would you like to do? " + color.RED))
		
		if(choice == 1):
			server.printLogs()
			
	if(mc_status == "unhealthy" and docker_status == "exited"):
		mc_server.print_with_border(name)
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
