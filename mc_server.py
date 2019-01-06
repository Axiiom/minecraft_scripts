import os
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

    # gets the current player count of the server as a string
    def get_player_count(self):
        if self.is_running:
            raw_pc = self.__rcon_call("list")[0]
            pc = raw_pc.replace("There are ", "").replace(" of a max ", "/").replace(" players online: ", " | ")

            index_of_break = pc.find(" | ")
            try:
                pc[index_of_break + 4]
                return pc
            except:
                return pc.replace(" | ", "")

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
        players = self.get_player_count()

        if version:
            print("Version: %s" % version)
        if players:
            print("Players: %s" % players)

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
