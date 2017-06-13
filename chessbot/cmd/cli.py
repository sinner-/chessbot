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

    while 1:
        response = irc.get_text().split(' ', 3)
        print(' '.join(response), end="")

        if response[0] == "PING":
            irc.send("PONG %s" % response[1])
            print("PONG sent.")

        if len(response) > 3:
            message = {}
            message['src'] = response[0]
            message['type'] = response[1]
            message['dst'] = response[2]
            message['text'] = response[3].strip()

            logger.log(message['src'], message['dst'], message['text'])

            if message['type'] == "PRIVMSG" and message['text'].startswith(control_pattern):
                message['text'] = message['text'].lstrip(control_pattern)

                if message['dst'].startswith("#"):
                    if message['text'] == "hello":
                        irc.privmsg(message['dst'], "Hello")
                        continue
                    if message['text'].startswith("mpfhf"):
                        irc.privmsg(message['dst'], mpfhf(message['text'], control_pattern))
                        continue
                else:
                    target = message['src'].split("!")[0].strip(":")

                    if message['text'].startswith("join"):
                        channel = message['text'].split(' ')[1]
                        irc.privmsg(target, ("Joining %s" % channel))
                        irc.join(channel)
                        continue
                    if message['text'].startswith("part"):
                        channel = message['text'].split(' ')[1]
                        irc.privmsg(target, ("Leaving %s" % channel))
                        irc.part(channel)
                        continue
                    if message['text'] == "quit":
                        irc.privmsg(target, "Quitting!")
                        irc.quit()
                        db.close()
                        exit()
