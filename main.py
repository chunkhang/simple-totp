from contextlib import contextmanager
from datetime import datetime
import pyotp
import time
import sys
import math

ENTRIES = [
        {
            'identifier': 'facebook:hello',
            'secret': 'test',
            },
        {
            'identifier': 'google:banana',
            'secret': 'funny',
            },
        ]


def main():
    with wrapper():
        items = []
        for entry in ENTRIES:
            item = {}
            item['identifier'] = entry['identifier']
            item['totp'] = pyotp.TOTP(entry['secret'])
            items.append(item)

        # Calculate max width for each column
        identifier_width = max(map(lambda item: len(item['identifier']), items))
        code_width = max(map(lambda item: item['totp'].digits, items))
        seconds_width = max(map(lambda item: len(str(item['totp'].interval)), items))

        while True:
            for i, item in enumerate(items):
                identifier = item['identifier']
                code = item['totp'].now()
                time_left = item['totp'].interval - (datetime.now().timestamp() % item['totp'].interval)
                seconds = str(math.trunc(time_left))

                row = '{} | {} | {}'.format(
                        identifier.ljust(identifier_width),
                        seconds.rjust(seconds_width, '0'),
                        code.ljust(code_width),
                        )
                sys.stdout.write(f'{row}\n')

            sys.stdout.flush()

            # Move cursor up until we reach the top
            sys.stdout.write('\033[F' * len(items))

            time.sleep(1)


# Setup and teardown for curses
@contextmanager
def wrapper():
    try:
        yield
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
