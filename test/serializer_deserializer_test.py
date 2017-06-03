import unittest
import hashlib
import random
import os
import pprint

from pigit.dal import DefaultSerializer
from pigit.bean import Blob, Commit, Tree, Signature, GitObject
from datetime import datetime, timezone, timedelta
from pytz import timezone

TEST_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")


def get_random_sha1_hash():
    return hashlib.sha1(bytes(str(random.randint(1000, 100000)), "utf-8")).hexdigest()


class DefaultSerializerTest(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.maxDiff = None

    def test_blob_serialization_deserialization(self):
        original_blob_content = "This is a test string for serialization"
        object_id = "some_id"
        blob = Blob(object_id, original_blob_content)
        serializer = DefaultSerializer()
        serialized_val = serializer.serialize(blob)
        deserialized_val = serializer.deserialize(object_id, serialized_val)

        self.assertEqual(blob, deserialized_val)

    def test_commit_serialization_deserialization(self):
        commit = Commit(get_random_sha1_hash(),
                        parents=[Commit(get_random_sha1_hash())],
                        author=Signature("Some author", "rajat@gmail.com", 1494659418, 330),
                        committer=Signature("ABC", "a@gmail.com", 1494659418, 90),
                        commit_message="Testing commit",
                        tree=Tree(get_random_sha1_hash()))
        serializer = DefaultSerializer()
        deserialized_commit = serializer.deserialize(commit.id, serializer.serialize(commit))
        self.assertEqual(deserialized_commit, commit, 'Serialized and deserialized commits don\'t match')

    def test_commit_deserialization(self):
        serializer = DefaultSerializer()
        commit_id = '97d3f98f52b5779598424c552428d24c020703b5'
        expected_commit = Commit(commit_id, [Commit('9975c95be19b40f29f9ab6e9d70c48ab508c859d')],
                                 Signature('Rajat Khanduja', 'rajatkhanduja13@gmail.com', 1496291306, 330),
                                 Signature('Rajat Khanduja', 'rajatkhanduja13@gmail.com', 1496291306, 330),
                                 'Added tests, still having issues with timestamp in CommitObject.',
                                 Tree('cafee551bb869ad60cc6ddd82c07ebd6b32c51f5'))

        with open(os.path.join(TEST_FILES_DIR, "commit_" + commit_id), 'rb') as fp:
            commit = serializer.deserialize(commit_id, fp.read())
            self.assertEqual(commit, expected_commit)
