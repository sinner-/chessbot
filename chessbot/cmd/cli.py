from chessbot.irc.client import IRCClient
from chessbot.irc.logger import Logger
from chessbot.db.sqlite import DB

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

        command = message['text'].lstrip(control_pattern).split(' ')

        #chan based commands
        if message['dst'].startswith("#") and message['dst'] in channels:
            if command[0] == "hello":
                irc.privmsg(message['dst'], "Hello")

        #privmsg commands
        else:
            target = message['src'].split("!", 1)[0].strip(":")
            if command[0] == "join" and len(command) == 2:
                channel = command[1]
                if channel in channels:
                    irc.privmsg(target, "Already in %s" % channel)
                    continue
                irc.privmsg(target, ("Joining %s" % channel))
                irc.join(channel)
            elif command[0] == "part" and len(command) == 2:
                channel = command[1]
                if channel not in channels:
                    irc.privmsg(target, "Not in %s" % channel)
                    continue
                irc.privmsg(target, ("Leaving %s" % channel))
                irc.part(channel)
            elif command[0] == "quit":
                irc.privmsg(target, "Quitting!")
                irc.quit()
                db.close()
                exit()
