import os
import re
from color import Color


def print_with_border(txt):
    text = txt.splitlines()
    maxLength = max(len(s) for s in text)
    colwidth = maxLength + 2

    print('+' + '-' * colwidth + '+')
    for s in text:
        print('| %-*.*s |' % (maxLength, maxLength, s))

    print('+' + '-' * colwidth + '+')


class MC:
    def __init__(self, container):
        self.container = container
        self.name = container.name
        self.is_running = (container.status == "running")

    # calls "message" on this servers' rcon-cli and returns the result
    def __rcon_call(self, message):
        if self.is_running:
            return os.popen("docker exec " + self.name + " rcon-cli " + message).readlines()

    # calls "message" on this servers' rcon-cli and prints the result to the console
    def __rcon_call_loud(self, message):
        if self.is_running:
            os.system("docker exec " + self.name + " rcon-cli " + message)

    # interactively calls "message" on this servers' rcon-cli and returns the result
    def __rcon_call_interactive(self, message):
        if self.is_running:
            return os.popen("docker exec -i" + self.name + " rcon-cli " + message).readlines()

    # starts the container
    def start(self):
        if not self.is_running:
            self.container.start()

    # stops the container
    def stop(self, delay):
        if self.is_running:
            self.container.stop(timeout=delay)

    # restarts the container
    def restart(self, delay):
        if self.is_running:
            self.container.restart(timeout=delay)

    # calls save on the servers' rcon-cli
    def save(self):
        if self.is_running:
            self.__rcon_call_loud("save-all")

    # writes "message" to the server using rcon-cli
    def say(self, message):
        if self.is_running:
            self.__rcon_call_loud("say " + message)

    # gets the version of the server
    def get_version(self):
        if self.is_running:
            output = os.popen("docker exec " + self.name + " mcstatus localhost status").readlines()
            version = output[0].replace("version: ", "")
            return version.strip()

    # gets the current player count of the server as an integer
    def get_player_count(self):
        if self.is_running:
            player_count = self.__rcon_call("list")[0]
            player_count = player_count.replace("There are ", "").replace(" of a max ", "/").replace(" players online: ","|")
            index_of_break = player_count.index("|")
            player_count = player_count[:index_of_break].strip()

            players = list(re.findall('\d+', player_count))
            return int(players[0])

    # gets the total player count of the server as an integer
    def get_total_players(self):
        if self.is_running:
            player_count = self.__rcon_call("list")[0]
            player_count = player_count.replace("There are ", "").replace(" of a max ", "/").replace(" players online: ","|")
            index_of_break = player_count.index("|")
            player_count = player_count[:index_of_break].strip()

            players = list(re.findall('\d+', player_count))
            return int(players[1])

    # returns the online players in a list of strings
    def get_online_players(self):
        if self.is_running:
            player_count = self.__rcon_call("list")[0]
            index = str.index(player_count, "online: ") + 8
            player_count = player_count[index:].strip()
            if player_count is "":
                return None
            else:
                return player_count.split(", ")

    # prints current server information to the console in the format:
    #
    # +-------------+
    # | server_name |
    # +-------------+
    # Version: xxxxxx
    # Players: xxxxxx
    def print_information(self):
        print_with_border(self.name)
        version = self.get_version()
        player_count = self.get_player_count()
        total_players = self.get_total_players()
        players_online = self.get_online_players()

        if version:
            print("Version: %s" % version)
        if players_online:
            players = ""
            for s in players_online:
                players += s + ", "
            print("Players: %d/%d | %s" % (player_count, total_players, players))
        else:
            print("Players: %d/%d" % (player_count, total_players))

    # prints and attaches to this servers' logs
    def attach_logs(self):
        if self.is_running:
            print(Color.END)
            os.system("docker logs -f " + self.name)

    # prints this servers' logs
    def print_logs(self):
        if self.is_running:
            print(Color.END)
            os.system("docker logs " + self.name)

    # attaches to this servers' rcon-cli
    def rcon(self):
        if self.is_running:
            command = "docker exec -i " + self.name + " rcon-cli"
            print(
                Color.END + "\nAccessing [RCON] for " + Color.CYAN + self.name + Color.END
                + "... (\"ctrl+c\" or \"ctrl+d\" to exit)")
            os.system(command)

    # gets the status of the docker container
    def status(self):
        output = os.popen("docker container inspect -f \"{{.State.Health.Status}}\" " + self.name).readlines()
        status = output[0].strip('\n')
        return status
