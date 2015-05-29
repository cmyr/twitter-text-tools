# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import re
import sys
import requests
import shutil

def dbm_iter(dbpath, raw=False):
    try:
        import gdbm
    except ImportError:
        print('database manipulation requires gdbm')

    db = gdbm.open(dbpath)
    k = db.firstkey()
    # kk will stride x2, to check for recursion
    kk = k
    if not k:
        print('failed to find first key', file=sys.stderr)
        raise StopIteration
    # ignore first key, which is metadata
    last_k = k
    k = db.nextkey(k)
    kk = db.nextkey(k)
    if kk == k:
        print("recursion in dbm file %s" % dbpath, file=sys.stderr)
        raise StopIteration
    try:
        while k:
            if k == last_k:
                print('breaking on key loop for key %s' % k, file=sys.stderr)
                break
            last_k = k
            try:
                item = dict_from_dbm(db[k])
                if item:
                    if raw:
                        yield item
                    else:
                        yield item.get('text')
                k = db.nextkey(k)
            except KeyError as err:
                k = db.nextkey(k)
                continue
    finally:
        db.close()

    raise StopIteration


def dict_from_dbm(dbm_tweet):
    try:
        values = re.split(unichr(0017), dbm_tweet.decode('utf-8'))
        t = dict()
        t['id'] = int(values[0])
        t['hash'] = values[1]
        t['text'] = values[2]
        return t
    except ValueError:
        return None


def prune_dict(indict, dict_template):
    """
    given two dictionaries, returns a new dictionary with those key/value
    pairs from the first dictionary that are present in the second. If value
    is a dictionary, performs recursively.
    """

    outdict = dict()
    for key, value in dict_template.items():
        keep = indict.get(key)
        if isinstance(keep, dict) and isinstance(value, dict):
            outdict[key] = prune_dict(keep, value)
        else:
            outdict[key] = keep
    return outdict


def save_image(url, path):
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    with open(path, 'wb') as tmp:
        shutil.copyfileobj(response.raw, tmp)


def main():
    pass


if __name__ == "__main__":
    main()
