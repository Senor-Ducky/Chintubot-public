import json
import os

default = {"TOKEN": None, "PREFIX": None, "DATABASE_URL": None}


class Settings:
    def __init__(self):
        raw_data = default
        try:
            with open("settings.json") as f:
                raw_data = json.load(f)

        except FileNotFoundError:
            with open("settings.json", "w") as f:
                json.dump(default, f)
                print(
                    "settings.json created"
                )

        finally:
            self.token = os.environ.get("TOKEN", raw_data.get("TOKEN"))
            self.prefix = os.environ.get("PREFIX", raw_data.get("PREFIX"))
            self.database_url = os.environ.get("DATABASE_URL", raw_data.get("DATABASE_URL"))
