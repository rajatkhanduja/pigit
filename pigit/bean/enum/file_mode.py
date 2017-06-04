from enum import Enum


class FileMode(Enum):
    UNREADABLE = '000000'
    TREE = '040000',
    BLOB = '100644',
    BLOB_EXECUTABLE = '100755',
    LINK = '120000',
    COMMIT = '160000',
