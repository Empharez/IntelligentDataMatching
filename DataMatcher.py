import pandas as pd


class IDMatcher:
    def __init__(self):
        self.data = []

    def read_data(self, url):
        data = pd.read_csv(url)
        df = pd.DataFrame(data)
        self.data = df
        return self.data
