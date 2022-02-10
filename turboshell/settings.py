class Settings:

    def __init__(self, **kwargs) -> None:
        self.include_header = True
        self.include_builtins = True
        self.add_info = True
        self.add_stubs = False
        self.set(**kwargs)

    def set(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)