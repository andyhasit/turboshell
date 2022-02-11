
class Settings:
    
    def __init__(self, **kwargs) -> None:
        self.include_header = True
        self.handle_not_found = True
        self.include_builtins = True
        self.add_info = True
        self.add_stubs = False
        self.set(**kwargs)

    def set(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise KeyError(f"Turboshell settings has no attr {k}")
            setattr(self, k, v)