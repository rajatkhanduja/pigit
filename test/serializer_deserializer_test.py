import hashlib
import os
import random
import unittest
import logging
import zlib

from pigit.bean import Blob, Commit, Tree, Signature, TreeEntry, Tag
from pigit.bean.enum import GitObjectType
from pigit.dal import DefaultSerializer

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
logging.basicConfig(level=logging.INFO)


def get_random_sha1_hash():
    return hashlib.sha1(bytes(str(random.randint(1000, 100000)), "utf-8")).hexdigest()


class SerializerDeserializerTest(unittest.TestCase):
    def setUp(self):
        self.serializer = DefaultSerializer()

    def test_blob_serialization_deserialization(self):
        original_blob_content = b"This is a test string for serialization"
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
            commit = self.serializer.deserialize(commit_id, zlib.decompress(fp.read()))
            self.assertEqual(commit, expected_commit, "Deserialized commit doesn't match expectation")

    def test_blob_deserialization(self):
        blob_id = '513106b14edde064256f0a09142e41b723c9f745'
        expected_blob = Blob(blob_id, b"Python library and client for git\n")
        with open(os.path.join(TEST_FILES_DIR, "blob_" + blob_id), 'rb') as fp:
            blob = self.serializer.deserialize(blob_id, zlib.decompress(fp.read()))
            self.assertEqual(blob, expected_blob, "Deserialized blob does't match expectation")

    def test_blob_deserialization_for_binary_file(self):
        blob_id = '729292c493cc1387621ea65332d1d9df5d25a4de'
        blob_content = b'x\x01\xa5\x8eAN\xc40\x10\x049\xe7\x15s_\xb4\xb2\x93\xd8\xc9H\x08-\xe2\xc8\x01\x89\x1f' \
                       b'\x8c\xc7\x93\x8d\xb3q\xb2\x8a\'\xf0}\x02\xe2\x07\x1c\xab\xd5\xaan^sN\n5v\x0f\xba\x89' \
                       b'\x00\xd3 \xe2\x9c\r\xa1\xf7H\xd1\x1bf\x1fc\xeck6\x9d\x84\xe8CS\xb3\xb3\x83\xab\xee\xb4' \
                       b'\xc9\xa2\x80\xd89F\x17\xc4bh\xcdP\xe3\x80\x14\xbc`\xec\x0c\xb7=\x05gz\xee\x1d\xc6\x8av' \
                       b'\x1d\xd7\r>h"\x85\xb7\x91\x96\xb8O\x04O\xdb\x0f\xdf\xfe\xd06\x97k\xa64\x9fy\xcd\xcf`[' \
                       b'\xf45\xda\xc6x8\x19\xd7\x98\xeaH\x8f\xaf*\xff\xb3T/1J\x04\x95\xa2\xe5\x11\x8a\xa6y\x86' \
                       b'\x91>\xd3r\x85T\xca.\x05\xbe\x92\x8e\xa0)\x1f\r\xcawH\x0b\xbc\xfe.\xbf\x87IX\xcf\xd57' \
                       b'\x19pb\x93'
        expected_blob = Blob(blob_id, blob_content)
        serialized_blob_file_path = os.path.join(TEST_FILES_DIR, 'blob_' + blob_id)
        with open(serialized_blob_file_path, 'rb') as fp:
            blob = self.serializer.deserialize(blob_id, zlib.decompress(fp.read()))
            self.assertEqual(blob, expected_blob, "Deserialized blob doesn't match for binary data")

    def test_tree_deserialization(self):
        tree_id = 'some_id'
        serialized_bytes = b"tree 183\x00100644 __init__.py\x00\x15Y+\xb8\x84\xb8\xe6E\x89\xdb(\xc0[" \
                           b"\xfe\xd1'\xf3\xe0\xc24100644 " \
                           b"object_store_test.py\x00L\xc342\xe6S\xd8\xd4\x15\x96\xa6\xfeB\xd27\x02\xe5\x90\x8b" \
                           b"\xc1100644 serializer_deserializer_test.py\x00\xa2M\xa4\x7f9\xca\x04m3\x95\x01," \
                           b"(\xba\x84\xe3\x84\xcfjp40000 test_files\x00\xb2[" \
                           b"\xe6G\xc9b\xf7\x19c\xc3\xcfM\x8eQ\x8d\xaf\xc6\xe9I\x05"
        expected_tree = Tree(tree_id,
                             [
                                 TreeEntry('100644', '__init__.py', '15592bb884b8e64589db28c05bfed127f3e0c234'),
                                 TreeEntry('100644', 'object_store_test.py',
                                           '4cc33432e653d8d41596a6fe42d23702e5908bc1'),
                                 TreeEntry('100644', 'serializer_deserializer_test.py',
                                           'a24da47f39ca046d3395012c28ba84e384cf6a70'),
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

    def test_tag_deserialization(self):
        tag_id = 'some_id'
        serialized_bytes = b'tag 159\x00object 751796a3a414321be1805cee9cb8b32023fa6bf7\ntype commit\ntag ' \
                           b'testTag\ntagger Rajat Khanduja <rajatkhanduja13@gmail.com> 1496564731 +0530\n\nA trivial' \
                           b' test tag\n'
        expected_tag = Tag(tag_id, 'testTag', Signature('Rajat Khanduja', 'rajatkhanduja13@gmail.com', 1496564731, 330),
                           '751796a3a414321be1805cee9cb8b32023fa6bf7', GitObjectType.COMMIT, 'A trivial test tag\n')
        self.assertEqual(self.serializer.deserialize(tag_id, serialized_bytes), expected_tag)

    def test_tag_serialization(self):
        tag = Tag('some_id', 'testTag', Signature('Rajat Khanduja', 'rajatkhanduja13@gmail.com', 1496564731, 330),
                  '751796a3a414321be1805cee9cb8b32023fa6bf7', GitObjectType.COMMIT, 'A trivial test tag')
        serialized_bytes = self.serializer.serialize(tag)
        tag_from_bytes = self.serializer.deserialize(tag.id, serialized_bytes)
        self.assertEqual(tag, tag_from_bytes)
