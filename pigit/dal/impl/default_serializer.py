import zlib
import re

from pigit.bean import GitObject, Commit, Tree, Blob, Signature
from pigit.bean.enum import GitObjectType
from ..serializer_deserializer import SerializerDeserializer
from abc import ABCMeta, abstractmethod


def get_header_content(file_content: bytes) -> (str, str):
    header_bytes, content_bytes = file_content.split(b'\x00')
    header = header_bytes.decode("utf-8")
    content = content_bytes.decode("utf-8")
    return header, content


def infer_type_and_length(header) -> (GitObjectType, int):
    object_type = None
    length = 0
    if header.startswith('blob'):
        object_type = GitObjectType.BLOB
        length = int(header[4:].strip())
    elif header.startswith('commit'):
        object_type = GitObjectType.COMMIT
        length = int(header[6:].strip())
    elif header.startswith('tree'):
        object_type = GitObjectType.TREE
        length = int(header[4:].strip())

    return object_type, length


def serialize_timestamp(signature: Signature):
    offset_minutes = signature.offset_minutes

    offset = "{sign}{hour:02d}{minute:02d}".format(sign='+' if offset_minutes > 0 else '-',
                                                   hour=int(offset_minutes / 60),
                                                   minute=offset_minutes % 60)
    return str(signature.timestamp) + " " + offset


class GitObjectSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, obj: GitObject) -> str:
        pass

    @abstractmethod
    def deserialize(self, object_id, content: str) -> GitObject:
        pass


class CommitSerializer(GitObjectSerializer):
    def serialize(self, commit: Commit):
        template_str = "tree {tree_ref}\n".format(tree_ref=commit.tree.id)

        if commit.parents is not None:
            for parent in commit.parents:
                template_str += "parent {parent_id}\n".format(parent_id=parent.id)

        template_str += "author {author} <{author_email}> {author_timestamp}\n" \
                        + "committer {committer} <{committer_email}> {commit_timestamp}\n\n" \
                        + "{commit_message}\n"
        author_timestamp_str = serialize_timestamp(commit.author)
        committer_timestamp_str = serialize_timestamp(commit.committer)
        return template_str.format(commit_message=commit.message, author=commit.author.name,
                                   author_email=commit.author.email,
                                   author_timestamp=author_timestamp_str,
                                   committer=commit.committer.name, committer_email=commit.committer.email,
                                   commit_timestamp=committer_timestamp_str)

    def deserialize(self, object_id, content: str):
        lines = content.split('\n')[:-1]

        def parse_timezone(tz_str: str) -> int:
            offset_minutes = int(tz_str[1:3]) * 60 + int(tz_str[3:])
            if tz_str[0] == '-':
                offset_minutes *= -1
            return offset_minutes

        def get_signature(line, type):
            match = re.search(type + " (.+) <(.+)> (.+)", line)
            if match:
                name = match.group(1)
                email = match.group(2)
                timestamp_str = match.group(3)
                timestamp = int(timestamp_str.split()[0])
                tz = parse_timezone(str(timestamp_str.split()[1]))
                return Signature(name, email, timestamp, tz)
            else:
                raise ValueError("Input not formatted as expected")

        def get_parent_id(line):
            match = re.search("parent (.+)", line)
            if match:
                parent_id = match.group(1)
                return parent_id
            else:
                raise ValueError("Input not formatted as expected")

        def get_commit_message(lines):
            commit_message_lines = []
            reversed_lines = reversed(lines)
            for line in reversed_lines:
                if line.startswith("committer"):
                    break
                commit_message_lines.append(line)
            return '\n'.join(reversed(commit_message_lines[:-1]))

        tree = None
        author = None
        committer = None, None, None
        parents = []
        commit_message = get_commit_message(lines)

        for line in lines:
            if line.startswith("tree"):
                tree = Tree(line[4:].strip())
            elif line.startswith("parent"):
                parent_id = get_parent_id(line)
                parents.append(Commit(parent_id))
            elif line.startswith("author"):
                author = get_signature(line.strip(), "author")
            elif line.startswith("committer"):
                committer = get_signature(line.strip(), "committer")

        return Commit(object_id, parents, author, committer, commit_message, tree)


class BlobSerializer(GitObjectSerializer):
    def serialize(self, blob: Blob):
        return blob.content + "\n"

    def deserialize(self, object_id, content: str):
        return Blob(object_id, content[:-1])


class TreeSerializer(GitObjectSerializer):
    def serialize(self, tree: Tree):
        raise NotImplementedError

    def deserialize(self, object_id, content: str):
        raise NotImplementedError


class DefaultSerializer(SerializerDeserializer):
    def _get_serializer(self, obj_type: GitObjectType) -> GitObjectSerializer:
        serializer_mapping = {
            GitObjectType.COMMIT: CommitSerializer,
            GitObjectType.TREE: TreeSerializer,
            GitObjectType.BLOB: BlobSerializer
        }
        return serializer_mapping[obj_type]()

    def serialize(self, obj: GitObject) -> bytes:
        obj_type = obj.type.value
        serialized_str = self._get_serializer(obj.type).serialize(obj)
        serialized_str = obj_type + " " + str(len(serialized_str)) + "\x00" + serialized_str
        return zlib.compress(serialized_str.encode('utf-8'))

    def deserialize(self, object_id, serialized_bytes: bytes) -> GitObject:
        decompressed_bytes = zlib.decompress(serialized_bytes)
        header, content = get_header_content(decompressed_bytes)
        object_type, length = infer_type_and_length(header)
        return self._get_serializer(object_type).deserialize(object_id, content)

