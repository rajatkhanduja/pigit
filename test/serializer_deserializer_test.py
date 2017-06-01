import unittest
import hashlib
import random

from pigit.dal import DefaultSerializer
from pigit.bean import BlobObject, CommitObject, TreeObject


def get_random_sha1_hash():
    return hashlib.sha1(bytes(str(random.randint(1000, 100000)), "utf-8")).hexdigest()


class DefaultSerializerTest(unittest.TestCase):
    def test_blob_serialization_deserialization(self):
        original_blob_content = "This is a test string for serialization"
        object_id = "some_id"
        blob = BlobObject(object_id, original_blob_content)
        serializer = DefaultSerializer()
        serialized_val = serializer.serialize(blob)
        deserialized_val = serializer.deserialize(object_id, serialized_val)

        self.assertEqual(blob, deserialized_val)

    def test_commit_serialization_deserialization(self):
        commit = CommitObject(get_random_sha1_hash(), None, get_random_sha1_hash(), get_random_sha1_hash(),
                              "Some author", "rajat@gmail.com", "1496111685 +0530", "ABC", "a@gmail.com",
                              "1496111685 +0130", "Testing commit")
        serializer = DefaultSerializer()
        deserialized_commit = serializer.deserialize(commit.id, serializer.serialize(commit))
        self.assertEqual(deserialized_commit, commit)