from unittest import TestCase

from pigit.id_generator import SerializerBasedIdGenerator
from pigit.serializer import DefaultSerializer
from pigit.bean import Blob
from hashlib import sha1


class IdGeneratorTest(TestCase):
    def setUp(self):
        self.id_generator = SerializerBasedIdGenerator(serializer=DefaultSerializer(), hasher=sha1)

    def testIdGeneratorForBlob(self):
        blob_id = '513106b14edde064256f0a09142e41b723c9f745'
        blob_content = b'Python library and client for git\n'
        blob = Blob(None, blob_content)
        self.assertEqual(self.id_generator.generate_id(blob), blob_id)
