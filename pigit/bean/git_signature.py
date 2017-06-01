import pytz

from datetime import datetime, timezone, timedelta


class GitSignature(object):
    def __init__(self, name: str, email: str, timestamp: datetime = None, **kwargs):
        self.name = name
        self.email = email
        self.timestamp = timestamp
        if 'timezone' in kwargs:
            self.timezone = kwargs['timezone']

    @classmethod
    def from_string_timestamp(cls, name: str, email: str, timestamp: str):
        signature = GitSignature(name, email)
        signature.update_timestamp_from_string(timestamp)
        return signature

    def update_timestamp_from_string(self, timestamp_string: str):
        print(timestamp_string)
        timestamp, tz_offset = timestamp_string.split()
        timestamp = int(timestamp)
        offset_mins = int(tz_offset[1:3]) * 60 + int(tz_offset[3:])
        if tz_offset.startswith("-"):
            offset_mins *= -1
        self.timestamp = datetime.utcfromtimestamp(timestamp + offset_mins * 60).replace(tzinfo=pytz.FixedOffset(offset_mins))
        print(self.timestamp)

    def __repr__(self):
        return repr(self.__dict__)
