import json
import pathlib


class DB(object):
    DB_PATH: pathlib.Path = pathlib.Path.cwd() / "db.json"

    @classmethod
    def get_db(cls):
        if not cls.DB_PATH.exists():
            cls.DB_PATH.touch()
        with cls.DB_PATH.open() as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                return {}

    @classmethod
    def update_user_and_chat_id(cls, user_id, chat_id) -> None:
        db = cls.get_db()
        db[str(user_id)] = chat_id
        with cls.DB_PATH.open(mode="w") as f:
            json.dump(db, f, indent=2)

    @classmethod
    def get_chat_id_by_user(cls, user_id) -> str:
        db = cls.get_db()
        return db.get(str(user_id))

    @classmethod
    def get_all_user_and_chat_ids(cls):
        db = cls.get_db()
        return ((uid, cid) for uid, cid in db.items())
