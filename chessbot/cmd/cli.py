import random
from hashlib import sha256
from chessbot.irc.client import IRCClient
from chessbot.irc.logger import Logger
from chessbot.db.sqlite import DB

def auth(token, tokens):
    if token in tokens:
        tokens.remove(token)
        return True
    else:
        return False

def main():
    db_path = "bot.db"
    server = "irc.freenode.net"
    port = 6697
    nickname = "chessbot"
    channels = ["#testchess"]
    control_pattern = ":#!"
    tokens = []

    db = DB(db_path)
    logger = Logger(db)

    irc = IRCClient(server, port, nickname)
    for channel in channels:
        irc.join(channel)

    random.seed()

    while True:
        response = irc.get_text().split(' ', 3)
        print(' '.join(response), end="")

        if response[0] == "PING":
            irc.send("PONG %s" % response[1])
            print("PONG sent.")

        if len(response) != 4:
            continue

        message = {}
        message['src'] = response[0]
        message['type'] = response[1]
        message['dst'] = response[2]
        message['text'] = response[3].strip()

        logger.log(message['src'], message['dst'], message['text'])

        if not (message['type'] == "PRIVMSG" and message['text'].startswith(control_pattern)):
            continue

        command = message['text'].lstrip(control_pattern).split(' ')

        #chan based commands
        if message['dst'].startswith("#") and message['dst'] in channels:
            if command[0] == "hello":
                irc.privmsg(message['dst'], "Hello")

        #privmsg commands
        else:
            target = message['src'].split("!", 1)[0].strip(":")
            if command[0] == "get_token":
                token = sha256(str(random.getrandbits(256)).encode()).hexdigest()
                tokens.append(token)
                irc.privmsg(target, token)
            elif command[0] == "join" and len(command) == 3:
                if not auth(command[2], tokens):
                    continue
                channel = command[1]
                if channel in channels:
                    irc.privmsg(target, "Already in %s" % channel)
                    continue
                irc.privmsg(target, ("Joining %s" % channel))
                irc.join(channel)
                channels.append(channel)
            elif command[0] == "part" and len(command) == 3:
                if not auth(command[2], tokens):
                    continue
                channel = command[1]
                if channel not in channels:
                    irc.privmsg(target, "Not in %s" % channel)
                    continue
                irc.privmsg(target, ("Leaving %s" % channel))
                irc.part(channel)
                channels.remove(channel)
            elif command[0] == "quit" and len(command) == 2:
                if not auth(command[1], tokens):
                    continue
                irc.privmsg(target, "Quitting!")
                irc.quit()
                db.close()
                exit(0)
