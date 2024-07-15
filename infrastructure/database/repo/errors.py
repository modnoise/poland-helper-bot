class MessageLimitExceeded(Exception):
    def __init__(self, message="Exceeded message limit"):
        self.message = message
        super().__init__(self.message)
