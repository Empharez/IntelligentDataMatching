import recordlinkage as rl
import pandas as pd


class IDMatcher:
    def __init__(self, left_on, right_on):
        self.left_on = left_on
        self.right_on = right_on
        self.data = []

    def read_data(self, url):
        data = pd.read_csv(url)
        df = pd.DataFrame(data)
        self.data = df
        return self.data

    def sorter(self, dfA, dfB):
        indexer = rl.Index()
        # Use sorted neighbor as a good option if data is not clean
        indexer.sortedneighbourhood(left_on=self.left_on, right_on=self.right_on)
        pairs = indexer.index(dfA, dfB)
        return pairs

    def compare_for_matches(self, dfA, dfB, threshold):
        pairs = self.sorter(dfA, dfB)
        compare = rl.Compare()
        """
            columns on each table has to be hardcoded,
            the column name used should be changed.
            column name used is for test purposes only
        """
        compare.exact('City', 'Provider City', label='City')
        compare.string('Facility Name',
                       'Provider Name',
                       threshold=threshold,
                       label='Hosp_Name')
        compare.string('Address',
                       'Provider Street Address',
                       method='jarowinkler',
                       threshold=threshold,
                       label='Hosp_Address')
        features = compare.compute(pairs, dfA, dfB)
        return features

    def predict_id_matches(self, dfA, dfB, threshold):
        ecm = rl.ECMClassifier()
        potential_matches = ecm.fit_predict(self.compare_for_matches(dfA, dfB, threshold))
        matches = pd.DataFrame(list(potential_matches), columns=["ID On Table1", "ID on Table2"])
        return matches
