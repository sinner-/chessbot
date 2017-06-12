import ssl
import socket
import sys

class IRCClient:

    def __init__(self, server, port, nick):
        context = ssl.SSLContext()
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_default_certs()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc = context.wrap_socket(self.sock, server_hostname=server)

        print("connecting to %s:%d" % (server, port))
        self.irc.connect((server, port))
        self.send("USER %s %s %s :IRC ChessBot\n" % (nick, nick, nick))
        self.send("NICK %s\n" % nick)

    def send(self, string):
        self.irc.send(bytes(string, "UTF-8"))

    def privmsg(self, chan, msg):
        self.send("PRIVMSG %s %s\n" % (chan, msg))

    def join(self, channel):
        self.send("JOIN %s\n" % channel)

    def part(self, channel):
        self.send("PART %s\n" % channel)

    def quit(self):
        self.send("QUIT\n")

    def get_text(self):
        text = self.irc.recv(2040)

        if text.find(bytes("PING", "UTF-8")) != -1:
            self.send("PONG %s\r\n" % text.split()[1])

        return text.decode()
