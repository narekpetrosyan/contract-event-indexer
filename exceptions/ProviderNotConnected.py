class ProviderNotConnectedError(Exception):

    def __init__(self, message="Provider not initialized"):
        self.message = message
        super().__init__(self.message)
