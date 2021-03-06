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
    print(Color.UNDERLINE + "%-3s | %-20s | %-10s | %-8s | %-15s" % ("Num", "Name", "Players", "MC Status", "Container Status") + Color.END)

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

        print("%3d | %-20s | %-10s | %-8s | %-15s" % (i, name, players, mc_status, docker_status))
        i += 1


def server_management(server):
    os.system("clear")

    server.print_information()
    print(Color.UNDERLINE + Color.BOLD + "Menu options (\"ctrl+d\" to go back):" + Color.END)
    print("1 | " + Color.RED + "Stop" + Color.END + "\n" +
          "2 | " + Color.YELLOW + "Restart" + Color.END + "\n")

    choice = int(input("What would you like to do? " + Color.RED))
    print(Color.END)
    if choice == 1:
        stop = input("Are you sure you would like to stop the server? (y/n): ")

        if stop == "y":
            server.save()
            server.say("Server stopping in 5 seconds...")
            os.system("sleep 5")
            server.stop(0)

    elif choice == 2:
        restart = input("Are you sure you would like to restart the server? (y/n): ")

        if restart == "y":
            server.save()
            server.say("Server restarting in 5 seconds...")
            os.system("sleep 5")
            server.restart(0)


#WIP
def user_management(server):
    os.system("clear")

    server.get_server_name_border()
    print(Color.UNDERLINE + Color.BOLD + "Online players (\"ctrl+d\" to go back):" + Color.END)

    players = server.get_online_players()
    i = 1
    for p in players:
        print(str(i) + " | " + p)
        i = i + 1

    choice = int(input("\nWhich player would you like to manage? " + Color.RED))
    player = players[choice-1]

    os.system("clear")
    print(Color.END + "Managing " + Color.BOLD + player + Color.END + " on server "
          + Color.CYAN + server.get_server_name() + Color.END + "\n")

    print(Color.UNDERLINE + Color.BOLD + "Menu options (\"ctrl+d\" to go back):" + Color.END)
    print("1 | " + Color.DARKCYAN + "Teleport" + Color.END + "\n" +
          "2 | " + Color.GREEN + "Kick/Ban" + Color.END + "\n" +
          "3 | " + Color.YELLOW + "Give Item" + Color.END + "\n" +
          "4 | " + Color.BOLD + "Modify State/Stats" + Color.END + "\n")

    choice = int(input("What would you like to do? "))
    if choice == 1:
        tp(server, player, players)
    elif choice == 2:
        kick_or_ban(server, player)
    elif choice == 3:
        give(server, player)
    elif choice == 4:
        modify_player(server, player)


def modify_player(server, player):
    print("1 | " + Color.DARKCYAN + "Change Gamemode" + Color.END + "\n" +
          "2 | " + Color.GREEN + "Give/Remove Operator Permissions" + Color.END + "\n" +
          "3 | " + Color.YELLOW + "Kill" + Color.END + "\n" +
          "4 | " + Color.BOLD + "Give XP" + Color.END + "\n")

    choice = int(input("What would you like to do to " + Color.CYAN + player + Color.END + "? "))
    if choice == 1:
        print("1 | " + Color.DARKCYAN + "Survival" + Color.END + "\n" +
              "2 | " + Color.GREEN + "Creative" + Color.END + "\n" +
              "3 | " + Color.YELLOW + "Adventure" + Color.END + "\n" +
              "4 | " + Color.BOLD + "Spectator" + Color.END + "\n")
        gamemode = int(input("Select Gamemode: "))
        if gamemode == 1:
            server.rcon_call("gamemode survival " + player)
        if gamemode == 2:
            server.rcon_call("gamemode creative " + player)
        if gamemode == 3:
            server.rcon_call("gamemode adventure " + player)
        if gamemode == 4:
            server.rcon_call("gamemode spectator " + player)

    elif choice == 2:
        print("1 | " + Color.DARKCYAN + "Give Operator Permissions" + Color.END + "\n" +
              "2 | " + Color.GREEN + "Remove Operator Permissions" + Color.END + "\n")
        op = int(input("What would you like to do? "))
        if op == 1:
            server.rcon_call("op " + player)
        elif op == 2:
            server.rcon_call("deop " + player)

    elif choice == 3:
        kill = input("Are you sure you want to kill " + Color.CYAN + player + Color.END + "(y/n)? ")

        if kill == "y":
            server.rcon_call("kill " + player)

    elif choice == 4:
        print("1 | " + Color.DARKCYAN + "Add XP" + Color.END + "\n" +
              "2 | " + Color.GREEN + "Set XP" + Color.END + "\n")

        choice = int(input("What would you like to do?"))
        xp = input("\nEnter the amount of XP followed by whether you are adding\n" +
                   "levels or individual points (i.e: 10 levels | 10 points): ")

        if choice == 1:
            server.rcon_call("xp add " + player + " " + xp)
        elif choice == 2:
            server.rcon_call("xp set " + player + " " + xp)


def give(server, player):
    stuff = input("Input the item followed by the amount as such: \"Item Amount\"\n")
    server.rcon_call("give " + player + " " + stuff)


def kick_or_ban(server, player):
    print("1 | " + Color.YELLOW + "Kick " + Color.END + player + "\n" +
          "2 | " + Color.RED + "Ban " + Color.END + player + "\n")

    choice = (int(input("What wold you like to do? ")))
    if choice == 1:
        message = input("Input a reason for ban: ")
        server.rcon_call("kick " + player + " " + message)
    elif choice == 2:
        ban = input("Are you sure you would like to" + Color.BOLD + " ban " + Color.END +
                    player + "?(y/n): ")
        if ban == "y":
            server.rcon_call("ban " + player)


def tp(server, player, players):
    print("1 | " + Color.DARKCYAN + "Teleport to player" + Color.END + "\n" +
          "2 | " + Color.GREEN + "Teleport to coordinates" + Color.END + "\n")

    choice = (int(input("What wold you like to do? ")))
    if choice == 1:
        print(Color.BOLD + "\nWho would you like to teleport " + Color.CYAN + player
              + Color.END + Color.BOLD + " to?" + Color.END)

        it = 1
        for pl in players:
            print(str(it) + " | " + pl)
            it = it + 1

        choice = (int(input("Enter the player's cooresponding number: ")))
        tp_to = players[choice - 1]
        server.rcon_call("tp " + player + " " + tp_to)

    elif choice == 2:
        tp_to = input("Enter the coordinates in X Y Z that you would like to teleport "
                      + Color.CYAN + player + Color.END + " to: \n")
        print("\nTeleporting " + Color.CYAN + player + Color.END + " to [" + tp_to + "]...")
        server.rcon_call("tp " + player + " " + tp_to)
        os.system("sleep 1")


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
        print("1 | " + Color.DARKCYAN + "Remote Connect [RCON]" + Color.END + "\n" +
              "2 | " + Color.GREEN + "Server Management" + Color.END + "\n" +
              "3 | " + Color.YELLOW + "Player Management" + Color.END + "\n" +
              "4 | " + Color.BOLD + "Logs" + Color.END + "\n")
        choice = int(input("What would you like to do? " + Color.RED))

        print(Color.END)
        if choice == 1:
            server.rcon()
        if choice == 2:
            server_management(server)
        if choice == 3:
            user_management(server)
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
