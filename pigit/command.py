from abc import ABCMeta, abstractmethod
from typing import List

from pigit.bean import GitObject, Reference
from pigit.store import ObjectStore, ReferenceStore


class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self) -> Exception:
        pass

    @abstractmethod
    def rollback(self):
        pass


class ObjectStoreCommand(Command):
    def __init__(self, object_store: ObjectStore, git_object: GitObject):
        self.object_store = object_store
        self.object_to_store = git_object

    def execute(self):
        self.object_store.store_object(self.object_to_store)

    def rollback(self):
        self.object_store.delete_object(self.object_to_store.id)


class ReferenceStoreCommand(Command):
    def __init__(self, reference_store: ReferenceStore, reference: Reference):
        self.reference_store = reference_store
        self.reference_to_store = reference

    def execute(self):
        self.reference_store.store_reference(reference=self.reference_to_store, update=True)

    def rollback(self):
        self.reference_store.remove_reference(self.reference_to_store.name)


class Commands(Command):

    def __init__(self, commands: List[Command]=[]):
        self.commands = commands
        self.executed = []  # type: List[Command]

    def add_command(self, command: Command):
        self.commands.append(command)

    def execute(self):
        for command in self.commands:
            command.execute()
            self.executed.append(command)

    def rollback(self):
        while len(self.executed) > 0:
            self.executed.pop().rollback()
