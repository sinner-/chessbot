from chessbot.irc.client import IRCClient
from chessbot.irc.logger import Logger
from chessbot.db.sqlite import DB
from chessbot.util.mpfhf import mpfhf

def main():
    db_path = "bot.db"
    server = "irc.freenode.net"
    port = 6697
    nickname = "chessbot"
    channels = ["#testchess"]
    control_pattern = ":#!"

    db = DB(db_path)
    logger = Logger(db)

    irc = IRCClient(server, port, nickname)
    for channel in channels:
        irc.join(channel)

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

        command = message['text'].lstrip(control_pattern)

        #chan based commands
        if message['dst'].startswith("#") and message['dst'] in channels:
            if command == "hello":
                irc.privmsg(message['dst'], "Hello")
            elif command.startswith("mpfhf"):
                irc.privmsg(message['dst'], mpfhf(command, control_pattern))
        #privmsg commands
        else:
            target = message['src'].split("!")[0].strip(":")
            if command.startswith("join"):
                channel = command.split(' ')[1]
                irc.privmsg(target, ("Joining %s" % channel))
                irc.join(channel)
            elif command.startswith("part"):
                channel = command.split(' ')[1]
                irc.privmsg(target, ("Leaving %s" % channel))
                irc.part(channel)
            elif command == "quit":
                irc.privmsg(target, "Quitting!")
                irc.quit()
                db.close()
                exit()
