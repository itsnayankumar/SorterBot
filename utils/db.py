import json
import os

DB_FILE = "settings.json"

# Initialize keys
sticker_keys = {str(i): None for i in range(1, 16)}
sticker_keys.update({"default": None, "end": None, "spam": None})

DEFAULT_DATA = {
    "dump_channel": 0,
    "auth_users": [],
    "total_files": 0,  # <--- NEW STAT
    "stickers": sticker_keys
}

class Database:
    def __init__(self):
        self.data = self.load()

    def load(self):
        if not os.path.exists(DB_FILE):
            self.create_default()
            return DEFAULT_DATA
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                # Ensure new keys exist if updating old file
                if "total_files" not in data: data["total_files"] = 0
                return data
        except:
            self.create_default()
            return DEFAULT_DATA

    def create_default(self):
        with open(DB_FILE, "w") as f:
            json.dump(DEFAULT_DATA, f, indent=4)

    def save(self):
        with open(DB_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get_sticker(self, key):
        return self.data["stickers"].get(str(key))

    def set_sticker(self, key, file_id):
        self.data["stickers"][str(key)] = file_id
        self.save()

    # <--- NEW HELPER
    def add_files_count(self, count):
        self.data["total_files"] += count
        self.save()

db = Database()

