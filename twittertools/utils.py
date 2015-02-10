# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals


def dbm_iter(dbpath):
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
    kk = db.netkey(k)
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
                tweet = _tweet_from_dbm(db[k])
                if tweet:
                    yield tweet['tweet_text']
                k = db.nextkey(k)
            except KeyError as err:
                k = db.nextkey(k)
                continue
    finally:
        db.close()

    raise StopIteration


def main():
	pass


if __name__ == "__main__":
    main()