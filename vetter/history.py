class History:
    """Message history

    Attributes:
        processed (int): number of messages that have been sent to and
          responded by GPT
        messages (list): list of message dictionaries
        errors (list): list of errors that have been encountered

    """
    def __init__(self, *messages):
        self.processed = 0
        self.errors = []
        self.messages = messages or [
            {"role": "system", "content": "You are a helpful assistant."},
        ]

    def __str__(self):
        return str(self.count)

    def add(self, role: str, text: str):
        """Append a to the list of messages.

        Args:
            role (str): "system", "user" or "assistant"
            text (str): message content
        """
        self.messages.append({"role": role, "content": text})

    @property
    def count(self) -> int:
        """Total number of messages."""
        return len(self.messages)

    @property
    def last(self) -> dict:
        """The last message."""
        return self.messages[-1]

    @property
    def should_query(self):
        """Return True if there are messages that need to be processed."""
        return (self.count > 1) and (self.processed < self.count)
