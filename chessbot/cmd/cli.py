from chessbot.irc.client import IRCClient
import re

def main():
    server = "irc.freenode.net"
    port = 6667
    nickname = "chessbotr"
    channels = ["#testchess"]

    irc = IRCClient()
    irc.connect(server, port, nickname)
    for channel in channels:
        irc.join(channel)

    while 1:
        response = irc.get_text()
        print(response, end="")

        channel_pattern = re.compile("#\w+")

        if "PRIVMSG" in response:
            from_chan = re.findall(channel_pattern, response)
            if "hello" in response:
                irc.privmsg(from_chan[0], "Hello")
            if "part" in response:
                irc.privmsg(from_chan[0], "Leaving %s" % from_chan[0])
                irc.part(from_chan[0])
            if "quit" in response:
                irc.privmsg(from_chan[0], "Quitting!")
                irc.quit()
                exit()
