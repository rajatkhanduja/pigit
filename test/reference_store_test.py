import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from pigit.store import FileSystemReferenceStore
from pigit.exception import *


class ReferenceStoreTest(unittest.TestCase):
    def tearDown(self):
        super().tearDown()

    def setUp(self):
        super(ReferenceStoreTest, self).setUp()
        self.reference_store = FileSystemReferenceStore(git_dir=Path(".git"))

