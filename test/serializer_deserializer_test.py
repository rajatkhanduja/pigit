import hashlib
import os
import random
import unittest
import logging

from pigit.bean import Blob, Commit, Tree, Signature, TreeEntry
from pigit.bean.enum import GitObjectType
from pigit.dal import DefaultSerializer

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
logging.basicConfig(level=logging.DEBUG)

def get_random_sha1_hash():
    return hashlib.sha1(bytes(str(random.randint(1000, 100000)), "utf-8")).hexdigest()


class SerializerDeserializerTest(unittest.TestCase):
    def setUp(self):
        self.serializer = DefaultSerializer()

    def test_blob_serialization_deserialization(self):
        original_blob_content = "This is a test string for serialization"
        object_id = "some_id"
        blob = Blob(object_id, original_blob_content)
        serialized_val = self.serializer.serialize(blob)
        deserialized_val = self.serializer.deserialize(object_id, serialized_val)

        self.assertEqual(blob, deserialized_val)

    def test_commit_serialization_deserialization(self):
        commit = Commit(get_random_sha1_hash(),
                        parents=[Commit(get_random_sha1_hash())],
                        author=Signature("Some author", "rajat@gmail.com", 1494659418, 330),
                        committer=Signature("ABC", "a@gmail.com", 1494659418, 90),
                        commit_message="Testing commit",
                        tree=Tree(get_random_sha1_hash()))
        deserialized_commit = self.serializer.deserialize(commit.id, self.serializer.serialize(commit))
        self.assertEqual(deserialized_commit, commit, 'Serialized and deserialized commits don\'t match')

    def test_commit_deserialization(self):
        commit_id = '97d3f98f52b5779598424c552428d24c020703b5'
        expected_commit = Commit(commit_id, [Commit('9975c95be19b40f29f9ab6e9d70c48ab508c859d')],
                                 Signature('Rajat Khanduja', 'rajatkhanduja13@gmail.com', 1496291306, 330),
                                 Signature('Rajat Khanduja', 'rajatkhanduja13@gmail.com', 1496291306, 330),
                                 'Added tests, still having issues with timestamp in CommitObject.',
                                 Tree('cafee551bb869ad60cc6ddd82c07ebd6b32c51f5'))

        with open(os.path.join(TEST_FILES_DIR, "commit_" + commit_id), 'rb') as fp:
            commit = self.serializer.deserialize(commit_id, fp.read())
            self.assertEqual(commit, expected_commit, "Deserialized commit doesn't match expectation")

    def test_blob_deserialization(self):
        blob_id = '513106b14edde064256f0a09142e41b723c9f745'
        expected_blob = Blob(blob_id, "Python library and client for git")
        with open(os.path.join(TEST_FILES_DIR, "blob_" + blob_id), 'rb') as fp:
            blob = self.serializer.deserialize(blob_id, fp.read())
            self.assertEqual(blob, expected_blob, "Deserialized blob does't match expectation")

    def test_tree_deserialization(self):
        tree_id = 'some_id'
        # serialized_bytes = b"tree 183\x00100644 __init__.py\x00\x15Y+\xb8\x84\xb8\xe6E\x89\xdb(\xc0[" \
        #                    b"\xfe\xd1'\xf3\xe0\xc24100644 " \
        #                    b"object_store_test.py\x00L\xc342\xe6S\xd8\xd4\x15\x96\xa6\xfeB\xd27\x02\xe5\x90\x8b" \
        #                    b"\xc1100644 serializer_deserializer_test.py\x00\xa2M\xa4\x7f9\xca\x04m3\x95\x01," \
        #                    b"(\xba\x84\xe3\x84\xcfjp40000 test_files\x00\xb2[" \
        #                    b"\xe6G\xc9b\xf7\x19c\xc3\xcfM\x8eQ\x8d\xaf\xc6\xe9I\x05 "
        serialized_bytes = b'x\x01+)JMU0\xb40f040031Q\x88\x8f\xcf\xcc\xcb,' \
                           b'\x89\x8f\xd7+\xa8d\x10\x8d\xd4\xde\xd1\xb2\xe3\x99k\xe7m\x8d\x03\xd1\xff.\xaa\x7f~p\xc8' \
                           b'\x04\xaa,?)+5\xb9$\xbe\xb8$\xbf(' \
                           b'5\xbe$\xb5\xb8\x04\xa4\xde\xe7\xb0\x89\xd1\xb3\xe0\x1bWD\xa7-\xfb\xe7t\xc9\x9c\xe9\xe9' \
                           b'\x84\xee\x83P\xf5\xc5\xa9E\x99\x899\x99U\xa9E\xf1)\xa9H\x1c\x98\xd6E\xbeK\xea-O\xb1\xe4' \
                           b'\x1aOe\xd4\xd1\xd8\xd5\xf2\xb8\xe5|V\x81\x89\x01\x10(' \
                           b'\x80T\xc4\xa7e\xe6\xa4\x163l\x8a~\xe6~2\xe9\xbbd\xf2\xe1\xf3\xbe}\x81\xbd\xeb\x8f\xbd' \
                           b'\xf4d\x05\x00`\xc4N\x87 '
        expected_tree = Tree(tree_id,
                             [
                                 TreeEntry('100644', '__init__.py', '15592bb884b8e64589db28c05bfed127f3e0c234'),
                                 TreeEntry('100644', 'object_store_test.py', '4cc33432e653d8d41596a6fe42d23702e5908bc1'),
                                 TreeEntry('100644', 'serializer_deserializer_test.py', 'a24da47f39ca046d3395012c28ba84e384cf6a70'),
                                 TreeEntry('040000', 'test_files', 'b25be647c962f71963c3cf4d8e518dafc6e94905')
                             ])
        deserialized_tree = self.serializer.deserialize(tree_id, serialized_bytes)
        self.assertEqual(deserialized_tree, expected_tree, "Deserialized tree doesn't match expectation")

    def test_tree_serialization_deserialization(self):
        tree_id = 'some_id'
        tree = Tree(tree_id,
                    [
                        TreeEntry('100644', '__init__.py', '15592bb884b8e64589db28c05bfed127f3e0c234'),
                        TreeEntry('100644', 'object_store_test.py', '4cc33432e653d8d41596a6fe42d23702e5908bc1'),
                        TreeEntry('100644', 'serializer_deserializer_test.py',
                                  'a24da47f39ca046d3395012c28ba84e384cf6a70'),
                        TreeEntry('040000', 'test_files', 'b25be647c962f71963c3cf4d8e518dafc6e94905')
                    ])
        self.assertEqual(self.serializer.deserialize(tree_id, self.serializer.serialize(tree)), tree)