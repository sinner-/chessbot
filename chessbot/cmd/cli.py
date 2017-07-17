import os
from chessbot.bot.controller import Controller

def main():

    try:
        db_path = os.environ['BOT_DB_PATH']
    except KeyError:
        db_path = "bot.db"

    try:
        server = os.environ['BOT_IRC_SERVER']
    except KeyError:
        server = "irc.freenode.net"

    try:
        port = os.environ['BOT_IRC_PORT']
    except KeyError:
        port = "6697"

    try:
        nickname = os.environ['BOT_NICKNAME']
    except KeyError:
        nickname = "chessbot"

    try:
        channels = os.environ['BOT_CHANNELS']
    except KeyError:
        channels = "#playchess"

    try:
        admin_key = os.environ['BOT_ADMIN_KEY']
    except KeyError:
        print("You must define $BOT_ADMIN_KEY")
        exit(1)

    controller = Controller(
        db_path,
        server,
        port,
        nickname,
        channels,
        admin_key
    )
    controller.start()
