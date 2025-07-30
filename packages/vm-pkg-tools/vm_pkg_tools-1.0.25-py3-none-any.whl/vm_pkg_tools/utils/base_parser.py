class BaseParser:
    """Base class for parsers."""

    def __init__(self, content):
        self.content = content

    def parse(self):
        raise NotImplementedError("Subclasses should implement this method.")
