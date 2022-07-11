from mmap import mmap
import struct
from timeit import default_timer
from multiprocessing import Manager
from pyshmht import HashTable


class shared_immutable_dict:
    def __init__(self, a):
        self.hs = 1 << (len(a) * 3).bit_length()
        kvp = self.hs * 4
        ht = [0xffffffff] * self.hs
        kvl = []
        for k, v in a.iteritems():
            h = self.hash(k)
            while ht[h] != 0xffffffff:
                h = (h + 1) & (self.hs - 1)
            ht[h] = kvp
            kvp += self.kvlen(k) + self.kvlen(v)
            kvl.append(k)
            kvl.append(v)

        self.m = mmap(-1, kvp)
        for p in ht:
            self.m.write(uint_format.pack(p))
        for x in kvl:
            if len(x) <= 0x7f:
                self.m.write_byte(chr(len(x)))
            else:
                self.m.write(uint_format.pack(0x80000000 + len(x)))
            self.m.write(x)

    def hash(self, k):
        h = hash(k)
        h = (h + (h >> 3) + (h >> 13) + (h >> 23)) * 1749375391 & (self.hs - 1)
        return h

    def get(self, k, d=None):
        h = self.hash(k)
        while True:
            x = uint_format.unpack(self.m[h * 4:h * 4 + 4])[0]
            if x == 0xffffffff:
                return d
            self.m.seek(x)
            if k == self.read_kv():
                return self.read_kv()
            h = (h + 1) & (self.hs - 1)

    def read_kv(self):
        sz = ord(self.m.read_byte())
        if sz & 0x80:
            sz = uint_format.unpack(chr(sz) + self.m.read(3))[0] - 0x80000000
        return self.m.read(sz)

    def kvlen(self, k):
        return len(k) + (1 if len(k) <= 0x7f else 4)

    def __contains__(self, k):
        return self.get(k, None) is not None

    def close(self):
        self.m.close()

uint_format = struct.Struct('>I')


def uget(a, k, d=None):
    return to_unicode(a.get(to_str(k), d))


def uin(a, k):
    return to_str(k) in a


def to_unicode(s):
    return s.decode('utf-8') if isinstance(s, str) else s


def to_str(s):
    return s.encode('utf-8') if isinstance(s, unicode) else s


def mmap_test():
    n = 1000000
    d = shared_immutable_dict({str(i * 2): '1' for i in xrange(n)})
    start_time = default_timer()
    for i in xrange(n):
        if bool(d.get(str(i))) != (i % 2 == 0):
            raise Exception(i)
    print 'mmap speed: %d gets per sec' % (n / (default_timer() - start_time))


def manager_test():
    n = 100000
    d = Manager().dict({str(i * 2): '1' for i in xrange(n)})
    start_time = default_timer()
    for i in xrange(n):
        if bool(d.get(str(i))) != (i % 2 == 0):
            raise Exception(i)
    print 'manager speed: %d gets per sec' % (n / (default_timer() - start_time))


def shm_test():
    n = 1000000
    d = HashTable('tmp', n)
    d.update({str(i * 2): '1' for i in xrange(n)})
    start_time = default_timer()
    for i in xrange(n):
        if bool(d.get(str(i))) != (i % 2 == 0):
            raise Exception(i)
    print 'shm speed: %d gets per sec' % (n / (default_timer() - start_time))


if __name__ == '__main__':
    mmap_test()
    manager_test()
    shm_test()
