import os
import argparse
from base64 import b64encode
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g",
                        "--gen-signing-key",
                        action="store_true",
                        dest="gen_signing_key")
    parser.add_argument("-k",
                        "--print-admin-key",
                        action="store_true",
                        dest="print_admin_key")
    parser.add_argument("-s",
                        "--sign-token",
                        action="store_true",
                        dest="sign_token")
    parser.add_argument("-t",
                        "--token",
                        type=str,
                        dest="token")
    args = parser.parse_args()

    if args.gen_signing_key:
        print(
            SigningKey.generate().encode(encoder=HexEncoder).decode()
        )
        return

    try:
        key_text = os.environ['BOT_ADMIN_SIGNKEY']
    except KeyError:
        print("You must define $BOT_ADMIN_SIGN_KEY")
        exit(1)

    signing_key = SigningKey(key_text.encode(), encoder=HexEncoder)

    if args.print_admin_key:
        print(
            signing_key.verify_key.encode(encoder=HexEncoder).decode()
        )
    elif args.sign_token:
        if not args.token:
            print("You must call --sign-token with --token.")
            exit(1)

        print(
            b64encode(
                signing_key.sign(args.token.encode())
            ).decode()
        )
