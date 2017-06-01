import zlib
import re

from pigit.bean import GitObject, CommitObject, TreeObject, BlobObject
from pigit.bean.enum import GitObjectType


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


class DefaultSerializer(object):
    def __init__(self):
        pass

    def __commit_object_serialize(self, commit_object: CommitObject):
        template_str = "tree {tree_ref}\n".format(tree_ref=commit_object.tree_reference)
        if commit_object.parent_id is not None:
            template_str += "parent {parent_id}\n".format(parent_id=commit_object.parent_id)

        template_str += "author {author} <{author_email}> {author_timestamp}\n" \
                        + "committer {committer} <{committer_email}> {commit_timestamp}\n\n" \
                        + "{commit_message}\n"
        return template_str.format(commit_message=commit_object.commit_message, author=commit_object.author.name,
                                   author_email=commit_object.author.email,
                                   author_timestamp=commit_object.author.timestamp.strftime("%s %z"),
                                   committer=commit_object.committer.name, committer_email=commit_object.committer.email,
                                   commit_timestamp=commit_object.committer.timestamp.strftime("%s %z"))

    def __commit_object_deserialize(self, object_id: str, content: str) -> GitObject:
        lines = content.split('\n')[:-1]
        tree = lines[0][4:].strip()

        def get_name_email_and_timestamp(line, type):
            match = re.search(type + " (.+) <(.+)> (.+)", line)
            if match:
                name = match.group(1)
                email = match.group(2)
                timestamp = match.group(3)
                return name, email, timestamp
            else:
                print(line)
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

        author, author_email, author_timestamp = None, None, None
        committer, committer_email, commit_timestamp = None, None, None
        parent_id = None
        commit_message = get_commit_message(lines)

        for line in lines[1:]:
            if line.startswith("parent"):
                parent_id = get_parent_id(line)
            elif line.startswith("author"):
                author, author_email, author_timestamp = get_name_email_and_timestamp(line.strip(), "author")
            elif line.startswith("committer"):
                committer, committer_email, commit_timestamp = get_name_email_and_timestamp(line.strip(), "committer")

        return CommitObject(object_id, None, parent_id, tree, author, author_email, author_timestamp, committer,
                            committer_email, commit_timestamp, commit_message)

    def __blob_object_serialize(self, blob_object: BlobObject):
        return blob_object.content + "\n"

    def __tree_object_serialize(self, tree_object: TreeObject):
        raise NotImplementedError

    def serialize(self, obj: GitObject) -> bytes:
        serialized_str = None
        obj_type = None

        if obj.type == GitObjectType.COMMIT:
            serialized_str = self.__commit_object_serialize(obj)
            obj_type = "commit"
        elif obj.type == GitObjectType.BLOB:
            serialized_str = self.__blob_object_serialize(obj)
            obj_type = "blob"
        elif obj.type == GitObjectType.TREE:
            serialized_str = self.__tree_object_serialize(obj)
            obj_type = "tree"

        serialized_str = obj_type + " " + str(len(serialized_str)) + "\x00" + serialized_str
        return zlib.compress(serialized_str.encode('utf-8'))

    def deserialize(self, object_id, serialized_bytes: bytes) -> GitObject:
        decompressed_bytes = zlib.decompress(serialized_bytes)
        print(decompressed_bytes)
        header, content = get_header_content(decompressed_bytes)
        object_type, length = infer_type_and_length(header)

        if object_type == GitObjectType.BLOB:
            return self.__blob_object_deserialize(object_id, content)
        elif object_type == GitObjectType.COMMIT:
            return self.__commit_object_deserialize(object_id, content)
        elif object_type == GitObjectType.TREE:
            return TreeObject(object_id, content)

    def __blob_object_deserialize(self, object_id: str, content: str):
        return BlobObject(object_id, content[:-1])
