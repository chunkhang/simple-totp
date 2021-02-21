from contextlib import contextmanager
from datetime import datetime
import math
import os
import pyotp
import sys
import time
import yaml

CONFIG_FILENAME = '.totp.yml'
DEFAULT_TOTP_INTERVAL = 30
DEFAULT_TOTP_DIGITS = 6


def main():
    # Read config data
    home = os.path.expanduser('~')
    config_path = os.path.join(home, CONFIG_FILENAME)
    with open(config_path) as file:
        config = yaml.full_load(file)

    # Parse config data
    totps = []
    for document in config['totp']:
        totp = pyotp.TOTP(
                s=document['secret'],
                interval=document['interval'] if 'interval' in document else DEFAULT_TOTP_INTERVAL,
                digits=document['digits'] if 'digits' in document else DEFAULT_TOTP_DIGITS,
                issuer=document['issuer'],
                name=document['name'],
                )
        totps.append(totp)

    # Calculate max width for each column
    identifier_width = max(map(lambda totp: len(get_totp_identifier(totp)), totps))
    code_width = max(map(lambda totp: totp.digits, totps))
    seconds_width = max(map(lambda totp: len(str(totp.interval)), totps))

    try:
        while True:
            for i, totp in enumerate(totps):
                seconds_left = math.trunc(totp.interval - (datetime.now().timestamp() % totp.interval))
                row = '{} | {} | {}'.format(
                        get_totp_identifier(totp).ljust(identifier_width),
                        str(seconds_left).rjust(seconds_width),
                        totp.now().ljust(code_width),
                        )
                sys.stdout.write(f'{row}\n')
            sys.stdout.flush()
            # Move cursor up until we reach the top
            sys.stdout.write('\033[F' * len(totps))
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def get_totp_identifier(totp):
    return '{}:{}'.format(
            totp.issuer,
            totp.name
            )


if __name__ == '__main__':
    main()
