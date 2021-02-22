from datetime import datetime
import math
import os
import pyotp
import sys
import time
import yaml

CONFIG_FILENAME = '.otp.yml'
DEFAULT_TOTP_ISSUER = '-'
DEFAULT_TOTP_NAME = '-'
DEFAULT_TOTP_INTERVAL = 30
DEFAULT_TOTP_DIGITS = 6
COLUMN_SEPARATOR = ' | '
REFRESH_RATE = 250  # ms


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
            issuer=document['issuer'] if 'issuer' in document else DEFAULT_TOTP_ISSUER,
            name=document['name'] if 'name' in document else DEFAULT_TOTP_NAME,
        )
        totps.append(totp)

    # Helper functions to set up columns for a totp row
    column_helpers = [
        # Issuer
        {
            'width': lambda totp: len(totp.issuer),
            'value': lambda totp: totp.issuer,
            'format': lambda value, width: value.ljust(width),
        },
        # Name
        {
            'width': lambda totp: len(totp.name),
            'value': lambda totp: totp.name,
            'format': lambda value, width: value.ljust(width),
        },
        # Seconds left
        {
            'value': lambda totp: math.trunc(totp.interval - (datetime.now().timestamp() % totp.interval)),
            'width': lambda totp: len(str(totp.interval)),
            'format': lambda value, width: str(value).rjust(width),
        },
        # Code
        {
            'value': lambda totp: totp.now(),
            'width': lambda totp: totp.digits,
            'format': lambda value, width: value.ljust(width),
        },
    ]

    # Calculate maximum width for all columns
    column_widths = []
    for helper in column_helpers:
        widths = map(lambda totp: helper['width'](totp), totps)
        column_widths.append(max(widths))

    try:
        while True:
            for totp in totps:
                values = map(lambda helper: helper['value'](totp), column_helpers)
                columns = []
                for i, value in enumerate(values):
                    column = column_helpers[i]['format'](value, column_widths[i])
                    columns.append(column)
                row = COLUMN_SEPARATOR.join(columns)
                sys.stdout.write(row)
                sys.stdout.write('\n')
            sys.stdout.flush()
            # Move cursor up until we reach the top
            sys.stdout.write('\033[F' * len(totps))
            time.sleep(REFRESH_RATE / 1000)
    except KeyboardInterrupt:
        # Keep quiet when quitting
        pass
    finally:
        # Make sure whatever has been printed remains
        sys.stdout.write('\n' * len(totps))
        sys.stdout.flush()


if __name__ == '__main__':
    main()
