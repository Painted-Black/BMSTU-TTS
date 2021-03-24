import os
from rocksdb import *
import gc


class Database:
    def __init__(self, db_path: str, name: str, ttl=None):
        option = Options()
        option.create_if_missing = True
        option.write_buffer_size = 2 ** 20
        if ttl is not None:
            option.wal_ttl_seconds = ttl

        self.db = DB('{path}{delim}{name}.db'.format(path=db_path, delim=os.path.sep, name=name), option)

    def write(self, key: bytearray, value: bytearray) -> None:
        self.db.put(key, value)

    def read(self, key: bytearray) -> bytearray:
        return self.db.get(key)

    def close(self):  # bad
        del self.db
        gc.collect()


class DBAccessManager:
    def __init__(self):
        self.databases = {}

    def create_db(self, db_path: str, name: str, ttl=None) -> Database:
        db = Database(db_path=db_path, name=name, ttl=ttl)
        self.databases[name] = db
        return db

    def get_db(self, name: str) -> Database:
        if self.databases.__contains__(name):
            return self.databases[name]
        else:
            return None

    def close_db(self, name: str):
        if self.databases.__contains__(name):
            self.databases[name].close()


db_access_manager = DBAccessManager()
