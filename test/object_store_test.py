import os
from unittest import TestCase

from pigit.dal.impl import FileSystemObjectStore
from pigit.bean import *
from pigit.dal import SerializerDeserializer
from pigit.exception import InvalidObjectNameException, DuplicateObjectException


class DummySerializer(SerializerDeserializer):
    def serialize(self, object: GitObject):
        return bytes("some_serialized_val", "utf-8")

    def deserialize(self, object_id: str, serialized_bytes: bytes):
        if object_id is None:
            raise ValueError
        if serialized_bytes is None:
            raise ValueError
        return Commit(object_id)


class FileSystemDataStoreTest(TestCase):
    def setUp(self):
        test_working_dir = os.path.join(os.path.dirname(__file__), 'test_files', 'test_working_dir')
        test_git_sub_dir = os.path.join(test_working_dir, '.git_test')

        self.object_store = FileSystemObjectStore(working_dir=test_working_dir, git_sub_directory=test_git_sub_dir,
                                                  serializer=DummySerializer())
        self.existing_object_ids = ['97d3f98f52b5779598424c552428d24c020703b5',
                                    '97cdcfc76e3245f92f6a71094a49bb4af225c367',
                                    '97cd0b35de837bab6f46140e4accc761cd287478']

    def test_fetch_object(self):
        for object_id in self.existing_object_ids:
            obj = self.object_store.get_object(object_id)
            self.assertIsNotNone(obj, "Object is empty")

    def test_fetch_object_fails_for_invalid_object(self):
        self.assertRaises(InvalidObjectNameException, self.object_store.get_object, "__3123")

    def test_fetch_object_should_work_if_object_can_be_uniquely_identified(self):
        test_object_id = '97cdcfc76e3245f92f6a71094a49bb4af225c367'
        self.object_store.get_object(test_object_id)
        self.object_store.get_object(test_object_id[:6])
        self.assertRaises(InvalidObjectNameException, self.object_store.get_object, test_object_id[:4])
        self.assertRaises(InvalidObjectNameException, self.object_store.get_object, test_object_id[:2])

    def test_store_object_fails_if_object_already_exists(self):
        for object_id in self.existing_object_ids:
            git_obj = self.object_store.get_object(object_id)
            self.assertRaises(DuplicateObjectException, self.object_store.store_object, git_obj)

    def test_store_object_succeeds(self):
        dummy_object_id = "some_object_id"
        blob = Blob(dummy_object_id, b"Some blob content")
        try:
            self.object_store.delete_object(dummy_object_id)
        except:
            pass
        self.object_store.store_object(blob)
        self.object_store.delete_object(dummy_object_id)
