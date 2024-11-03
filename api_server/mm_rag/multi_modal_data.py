class MultiModalData:
    def __init__(self, data_uri, duration: int = None):
        self.data_uri = data_uri

        # unit: second
        self.duration = duration