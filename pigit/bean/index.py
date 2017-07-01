# IndexEntry = collections.namedtuple('IndexEntry', [
#     'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode',
#     'uid', 'gid', 'size', 'sha1', 'flags', 'path',
# ])


class IndexEntry(object):

    def __init__(self, ctime_s: int, ctime_n: int, mtime_s: int, mtime_n: int, dev, ino, mode, uid, gid, size, sha1: str,
                 flags, path: str):
        self.ctime_s = ctime_s
        self.ctime_n = ctime_n
        self.mtime_s = mtime_s
        self.mtime_n = mtime_n
        self.dev = dev
        self.ino = ino
        self.mode = mode
        self.uid = uid
        self.gid = gid
        self.size = size
        self.sha1 = sha1
        self.flags = flags
        self.path = path

    def __repr__(self):
        return repr(self.__dict__)


class Index(object):

    def __init__(self, signature: str, version: int):
        self.signature = signature
        self.version = version
        self.index_entries = []

    def add_index_entry(self, entry: IndexEntry):
        self.index_entries.append(entry)

    def __repr__(self):
        return repr(self.__dict__)