import ssl
import socket

class IRCClient:

    def __init__(self, server, port, nick):
        context = ssl.SSLContext()
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_default_certs()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ssl_sock = context.wrap_socket(sock, server_hostname=server)

        self.channels = []

        self._ssl_sock.connect((server, port))
        self.send("USER %s %s %s :IRC ChessBot" % (nick, nick, nick))
        self.send("NICK %s" % nick)

    def send(self, message):
        self._ssl_sock.send(bytes("%s\n" % message, "UTF-8"))

    def get_text(self):
        return self._ssl_sock.recv(512).decode()

    def privmsg(self, dest, msg):
        self.send("PRIVMSG %s :%s" % (dest, msg))

    def join(self, channel):
        self.send("JOIN %s" % channel)
        self.channels.append(channel)

    def part(self, channel):
        self.send("PART %s" % channel)
        self.channels.remove(channel)

    def quit(self):
        self.send("QUIT")
        self._ssl_sock.close()
