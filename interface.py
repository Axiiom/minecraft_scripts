import os
import sys
import docker
from color import Color
from mc_server import MC
client = docker.from_env()


def format_status(status):
    # for MC Server Status - spacing is important here because of the color codes.
    if status == "healthy":
        return Color.GREEN + "Healthy  " + Color.END
    elif status == "unhealthy":
        return "         "
    elif status == "starting":
        return Color.YELLOW + "Starting " + Color.END

    # for Docker Container status
    elif status == "running":
        return Color.GREEN + "Running" + Color.END
    elif status == "exited":
        return Color.RED + "Exited" + Color.END


def get_server():
    try:
        containers = client.containers.list(all)
        choice = int(input(Color.END + "\nWhich server would you like to access? " + Color.RED))
        print(Color.END)
        return containers[choice-1]
    except ValueError:
        print()


def print_server_list():
    print(Color.END + Color.BOLD + "\nServers (press any key to refresh | \"ctrl+c\" to close):\n" + Color.END)
    print(Color.UNDERLINE + "%-3s | %-15s | %-10s | %-8s | %-15s" % ("Num", "Name", "Players", "MC Status", "Container Status") + Color.END)

    i = 1
    for container in client.containers.list(all):
        server = MC(container)
        name = server.name
        mc_status = format_status(server.status())
        docker_status = format_status(container.status)

        player_count = server.get_player_count()
        total_players = server.get_total_players()

        players = "None"
        if player_count is not None and total_players is not None:
            players = str(player_count) + "/" + str(total_players)

        print("%3d | %-15s | %-10s | %-8s | %-15s" % (i, name, players, mc_status, docker_status))
        i += 1


# Context-based options interface, takes in a docker container "server_choice"
def menu(server_choice):
    server = MC(server_choice)

    mc_status = server.status()
    docker_status = server_choice.status

    os.system("clear")
    print()

    if mc_status == "healthy":
        server.print_information()
        print(Color.UNDERLINE + Color.BOLD + "Menu options (\"ctrl+d\" to go back):" + Color.END)
        print("1 | " + Color.DARKCYAN + "Remote Connect [RCON]" + Color.END + "\n2 | " + Color.RED
              + "Stop" + Color.END + "\n3 | " + Color.YELLOW + "Restart" + Color.END + "\n4 | "
              + Color.BOLD + "Logs\n" + Color.END)
        choice = int(input("What would you like to do? " + Color.RED))

        print(Color.END)
        if choice == 1:
            server.rcon()
        if choice == 2:
            try:
                stop = input("Are you sure you would like to stop the server? (y/n): ")

                if stop == "y":
                    server.save()
                    server.say("Server stopping in 5 seconds...")
                    os.system("sleep 5")
                    server.stop(0)

                return True
            except ValueError:
                print()
            except EOFError:
                print()
        if choice == 3:
            try:
                restart = input("Are you sure you would like to stop the server? (y/n): ")
                if restart == "y":
                    server.save()
                    server.say("Server restarting in 5 seconds...")
                    os.system("sleep 5")
                    server.restart(0)
            except ValueError:
                print()
            except EOFError:
                print()
        if choice == 4:
            server.attach_logs()

    if mc_status == "starting":
        server.attach_logs()

    if mc_status == "unhealthy" and docker_status == "exited":
        server.print_information()
        print(Color.UNDERLINE + Color.BOLD + "\nMenu options (\"ctrl+d\" to go back):" + Color.END)
        print("1 | " + Color.GREEN + "Start\n" + Color.END)

        choice = int(input("What would you like to do? " + Color.RED))
        if choice == 1:
            print(Color.END + "Starting server...")
            server.start()


def main():
    os.system("clear")

    while True:
        os.system("clear")
        try:
            print_server_list()
            server_choice = get_server()
            if server_choice:
                menu(server_choice)
        except KeyboardInterrupt:
            print(Color.YELLOW + "\nExiting script...\n" + Color.END)
            os.system("sleep .5")
            sys.exit(0)
        except EOFError:
            print(Color.END)


if __name__ == '__main__':
    main()