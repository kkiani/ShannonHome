
class DisposableToken:
    counts = 3
    value = ""

    def __init__(self, disposeCounts, value):
        self.counts = disposeCounts
        self.value = value