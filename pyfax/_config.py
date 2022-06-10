import os


class Config:
    _entries = {}

    def __getattr__(self, a):
        if a in self._entries:
            return self._entries[a]
        return None

    def __setattr__(self, a, b):
        self._entries[a] = b


config = Config()
config.build_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    os.path.join("..", "_pages"))

config.teletext_button = "TELETEXT BUTTON"
