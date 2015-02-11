# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import re
import sys

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
                tweet = tweet_from_dbm(db[k])
                if tweet:
                    if raw:
                        yield tweet
                    else:
                        yield tweet['tweet_text']
                k = db.nextkey(k)
            except KeyError as err:
                k = db.nextkey(k)
                continue
    finally:
        db.close()

    raise StopIteration

def tweet_from_dbm(dbm_tweet):
    
    try:
        tweet_values = re.split(unichr(0017), dbm_tweet.decode('utf-8'))
        t = dict()
        t['tweet_id'] = int(tweet_values[0])
        t['tweet_hash'] = tweet_values[1]
        t['tweet_text'] = tweet_values[2]
        return t
    except ValueError:
        return None

def main():
	pass


if __name__ == "__main__":
    main()