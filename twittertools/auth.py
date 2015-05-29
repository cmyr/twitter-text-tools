# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import os
from twitter.oauth import OAuth

def load_auth(path, raw=False):
    if not os.path.exists(path):
        raise OSError("path not found")
    with open(path) as f:
        args = f.read().splitlines()
        if raw:
            return args
        else:
            return OAuth(*args)


def save_auth(path, access_key, access_secret, consumer_key, consumer_secret):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            for line in [access_key, access_secret, consumer_key, consumer_secret]:
                print(line, file=f)
    else:
        print('specified path exists. remove or rename and try again.')








def main():
    pass

if __name__ == "__main__":
    main()