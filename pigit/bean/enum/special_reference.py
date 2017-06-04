from enum import Enum


class SpecialReference(Enum):
    HEAD = 'HEAD'
    FETCH_HEAD = 'FETCH_HEAD'
    ORIG_HEAD = 'ORIG_HEAD'
    MERGE_HEAD = 'MERGE_HEAD'
    CHERRY_PICK_HEAD = 'CHERRY_PICK_HEAD'
