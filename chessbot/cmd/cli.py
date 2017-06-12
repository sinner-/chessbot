import re
import datetime
from chessbot.irc.client import IRCClient
from chessbot.db.sqlite import DB

def main():
    db_path = "bot.db"
    server = "irc.freenode.net"
    port = 6697
    nickname = "chessbot"
    channels = ["#testchess"]
    control_pattern = ":#!"

    db = DB(db_path)

    irc = IRCClient(server, port, nickname)
    for channel in channels:
        irc.join(channel)

    channel_pattern = re.compile("#\w+")

    while 1:
        response = irc.get_text().split(' ', 3)
        print(' '.join(response), end="")
        if len(response) > 3:
            db.cursor.execute("INSERT INTO logs VALUES (?, ?, ?, ?);",
                              (str(datetime.datetime.now().time()),
                               response[0],
                               response[2],
                               response[3],
                              ))
            db.commit()

        if response[0] == "PING":
            irc.send("PONG %s\r\n" % response[1])
            print("PONG sent.")

        if response[1] == "PRIVMSG" and response[3].startswith(control_pattern):
            targets = re.findall(channel_pattern, response[2])

            if targets:
                if response[3].startswith("%shello" % control_pattern):
                    irc.privmsg(targets[0], "Hello")
                    continue
            else:
                target = response[0].split("!")[0].strip(":")

                if response[3].startswith("%sjoin" % control_pattern):
                    channel = response[3].split(' ')[1]
                    irc.privmsg(target, "Joining %s" % channel)
                    irc.join(channel)
                    continue
                if response[3].startswith("%spart" % control_pattern):
                    channel = response[3].split(' ')[1]
                    irc.privmsg(target, "Leaving %s" % channel)
                    irc.part(channel)
                    continue
                if response[3].startswith("%squit" % control_pattern):
                    irc.privmsg(target, "Quitting!")
                    irc.quit()
                    db.close()
                    exit()
