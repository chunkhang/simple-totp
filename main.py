from datetime import datetime
import math
import os
import pyotp
import sys
import time
import yaml

CONFIG_FILENAME = '.totp.yml'
DEFAULT_TOTP_ISSUER = '-'
DEFAULT_TOTP_NAME = '-'
DEFAULT_TOTP_INTERVAL = 30
DEFAULT_TOTP_DIGITS = 6
COLUMN_SEPARATOR = '|'


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

    # Getter functions to calculate column value and width
    # Each totp row will have these columns
    column_getters = [
            # Issuer
            {
                'value': lambda totp: totp.issuer,
                'width': lambda totp: len(totp.issuer),
                },
            # Name
            {
                'value': lambda totp: totp.name,
                'width': lambda totp: len(totp.name),
                },
            # Seconds left
            {
                'value': lambda totp: str(math.trunc(totp.interval - (datetime.now().timestamp() % totp.interval))),
                'width': lambda totp: len(str(totp.interval)),
                },
            # Code
            {
                'value': lambda totp: totp.now(),
                'width': lambda totp: totp.digits,
                },
            ]

    # Calculate maximum width for all columns
    column_widths = []
    for getter in column_getters:
        getter['width'](totp)
        widths = map(lambda totp: getter['width'](totp), totps)
        column_widths.append(max(widths))

    try:
        while True:
            for totp in totps:
                values = map(lambda getter: getter['value'](totp), column_getters)
                columns = []
                for i, value in enumerate(values):
                    column = value.ljust(column_widths[i])
                    columns.append(column)
                row = f' {COLUMN_SEPARATOR} '.join(columns)
                sys.stdout.write(row)
                sys.stdout.write('\n')
            sys.stdout.flush()
            # Move cursor up until we reach the top
            sys.stdout.write('\033[F' * len(totps))
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
