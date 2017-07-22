import os
from pathlib import Path
from unittest import TestCase

from datetime import datetime

from pigit import Pigit, NothingToCommitException
from tempfile import TemporaryDirectory

from pigit.bean import Signature


class MemoryRepositoryTest(TestCase):
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        self.tmp_dir_path = Path(self.tmp_dir.name)
        self.repo = Pigit.get_memory_repository()
        os.chdir(self.tmp_dir.name)

    def tearDown(self):
        super().tearDown()
        self.tmp_dir.cleanup()

    def test_adding_file(self):
        test_file = Path("file1")
        with test_file.open('wb') as fp:
            fp.write(b"Some new line")
        self.repo.add(test_file)

        self.assertEqual(len(self.repo.index.entries), 1)

        index_entry = self.repo.index.entries[0]
        self.assertEqual(index_entry.path, test_file.name)

    def test_nothing_to_commit_exception_thrown_when_nothing_to_commit(self):
        timestamp = int(datetime.now().timestamp())
        with self.assertRaises(NothingToCommitException):
            self.repo.commit(message="First commit",
                             author=Signature('Rajat', 'rajatkhanduja13@gmail.com', timestamp, 330))

    def test_first_commit(self):
        # dummy_file = "file2"
        #
        # with open(dummy_file, 'wb') as fp:
        #     fp.write(b"Additional line")
        #
        # self.repo.add(dummy_file)
        #
        # self.assertEqual(len(self.repo.index.entries), 1)
        # timestamp = int(datetime.now().timestamp())
        # commit = self.repo.commit(message="First commit",
        #                           author=Signature('Rajat', 'rajatkhanduja13@gmail.com', timestamp, 330))
        commit = self.make_first_commit()
        self.assertEqual(self.repo.head.commit, commit.id)

    def test_nothing_to_commit_exception_right_after_a_commit(self):
        self.make_first_commit()

        timestamp = int(datetime.now().timestamp())
        author = Signature('Rajat', 'rajatkhanduja13@gmail.com', timestamp, 330)
        author.timestamp = int(datetime.now().timestamp())
        with self.assertRaises(NothingToCommitException):
            self.repo.commit(message="Second commit", author=author)

    def make_commit(self, filename: str):
        self.repo.add(filename)
        timestamp = int(datetime.now().timestamp())
        author = Signature('Rajat', 'rajatkhanduja13@gmail.com', timestamp, 330)
        commit = self.repo.commit(message="First commit", author=author)
        return commit

    def make_first_commit(self):
        new_file = "file3"
        with open(new_file, 'wb') as fp:
            fp.write(b"All of this better work!")
        return self.make_commit(new_file)

    def make_second_commit(self):
        dummy_file = "file2"

        with open(dummy_file, 'wb') as fp:
            fp.write(b"Additional line")
        return self.make_commit(dummy_file)

    def test_parent_is_correctly_set_for_commit(self):
        commit = self.make_first_commit()
        commit2 = self.make_second_commit()

        self.assertEqual(len(commit2.parents), 1)
        self.assertEqual(commit2.parents[0], commit)
