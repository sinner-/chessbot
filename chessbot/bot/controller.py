import random
from base64 import b64decode
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
from chessbot.irc.client import IRCClient
from chessbot.irc.logger import Logger
from chessbot.db.sqlite import DB

class Controller(object):
    def __init__(self, db_path, server, port, nickname, channels, admin_key):
        self._token_rand_bits = 16
        self._control_pattern = ":#!"

        self._db = DB(db_path)
        self._logger = Logger(self._db)
        self._irc = IRCClient(server, int(port), nickname)

        self._tokens = []
        try:
            self._admin_key = VerifyKey(admin_key.encode(), encoder=HexEncoder)
        except ValueError:
            print("Invalid BOT_ADMIN_KEY")
            exit(1)

        for channel in channels.split(","):
            self._irc.join(channel)

        random.seed()

    def _auth(self, response):
        token = None

        try:
            signed = b64decode(response.encode())
            token = self._admin_key.verify(signed).decode()
            self._tokens.remove(token)
        except:
            return False

        return True

    def _chan_handler(self, command, channel):
        if command[0] == "hello":
            self._irc.privmsg(channel, "Hello")

    def _priv_handler(self, command, target):
        if command[0] == "get_token":
            token = str(random.getrandbits(self._token_rand_bits))
            self._tokens.append(token)
            self._irc.privmsg(target, token)
        elif command[0] == "join" and len(command) == 3:
            if not self._auth(command[2]):
                return
            channel = command[1]
            if channel in self._irc.channels:
                self._irc.privmsg(target, "Already in %s" % channel)
                return
            self._irc.privmsg(target, ("Joining %s" % channel))
            self._irc.join(channel)
        elif command[0] == "part" and len(command) == 3:
            if not self._auth(command[2]):
                return
            channel = command[1]
            if channel not in self._irc.channels:
                self._irc.privmsg(target, "Not in %s" % channel)
                return
            self._irc.privmsg(target, ("Leaving %s" % channel))
            self._irc.part(channel)
        elif command[0] == "quit" and len(command) == 2:
            if not self._auth(command[1]):
                return
            self._irc.privmsg(target, "Quitting!")
            self._irc.quit()
            self._db.close()
            exit(0)

    def _input_handler(self):
        response = self._irc.get_text().split(' ', 3)
        print(' '.join(response), end="")

        if response[0] == "PING":
            self._irc.send("PONG %s" % response[1])
            print("PONG sent.")
            return

        if len(response) != 4:
            return

        message = {}
        message['src'] = response[0]
        message['type'] = response[1]
        message['dst'] = response[2]
        message['text'] = response[3].strip()

        self._logger.log(
            message['src'],
            message['dst'],
            message['text']
        )

        if not (message['type'] == "PRIVMSG" and message['text'].startswith(self._control_pattern)):
            return

        command = message['text'].lstrip(self._control_pattern).split(' ')

        #chan based commands
        if message['dst'].startswith("#") and message['dst'] in self._irc.channels:
            self._chan_handler(command, message['dst'])

        #privmsg commands
        else:
            target = message['src'].split("!", 1)[0].strip(":")
            self._priv_handler(command, target)

    def start(self):
        while True:
            try:
                self._input_handler()
            except KeyboardInterrupt:
                print("Quitting.")
                exit(0)
