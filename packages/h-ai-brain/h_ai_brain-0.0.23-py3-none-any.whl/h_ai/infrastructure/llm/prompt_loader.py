import json
import os


class PromptLoader:
    def __init__(self, file_path):
        # Resolve a relative path to an absolute path
        absolute_file_path = os.path.abspath(file_path)

        with open(absolute_file_path, "r") as file:
            self.config = json.load(file)

    def get_config_value(self, key):
        return self.config.get(key)

    def get_entire_config(self):
        return json.dumps(self.config, indent=2)

