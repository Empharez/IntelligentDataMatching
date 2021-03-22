import recordlinkage
import pandas as pd


class IDMatcher:
    def __init__(self, request, answer):
        self.request = request
        self.answer = answer
        self.data = []

    def read_data(self, file_path):
        """Function to read in data from a csv file using pandas. The source can be a url or the file-path.
         the data is then converted to a data frame.
        Args:
            file_path (string): path name of a file to read from.
        Returns:
            self.data (attribute): assign the data to attribute data.

        """
        data = pd.read_csv(file_path)
        df = pd.DataFrame(data)
        self.data = df
        return self.data

    def sorter(self, payload, kpi_records):
        """Sorter is a function to make a subset of the record space (A * B) also accounting for spelling mistakes.
        Args:
            payload (data attribute) : Dataframe on the left or first dataframe.
            kpi_records (data attribute) : Dataframe on the right or second dataframe.
        Returns:
            pairs (pandas multi-index) : returns a multi-index of the indexed data
        """
        indexer = recordlinkage.Index()
        # Use sorted neighbor as a good option if data is not clean
        indexer.sortedneighbourhood(left_on=self.request, right_on=self.answer)
        pairs = indexer.index(payload, kpi_records)
        return pairs

    def compare_for_matches(self, payload, kpi_records, threshold):
        """Compare for matches is a function that compares both data frames and return a multi index of the matches.
            uses the return value "pairs" from sorter.
                Args:
                    payload (dataframe) : Dataframe on the left or first dataframe.
                    kpi_records (dataframe) : Dataframe on the right or second dataframe.
                    threshold : probability
                Returns:
                    features : returns matches rows
                """
        pairs = self.sorter(payload, kpi_records)
        compare = recordlinkage.Compare()
        """
            columns on each table has to be hardcoded,
            the column name used should be changed.
            column name used is for test_id-matcher.py purposes only
        """
        compare.string('first_name', 'first_name',
                       threshold=threshold,
                       label='FIRST_NAME')
        compare.string('last_name',
                       'last_name',
                       threshold=threshold,
                       label='LAST_NAME')
        compare.string('email',
                       'email',
                       threshold=threshold,
                       label='EMAIL')
        compare.exact('phone_number',
                       'phone_number',
                       label='PHONE_NUMBER')
        compare.exact('date_of_birth',
                      'date_of_birth',
                      label='DOB')

        features = compare.compute(pairs, payload, kpi_records)
        return features

    def find_possible_matches(self, payload, kpi_records, threshold):
        """
        find_possible_matches is a methos that uses ECM Classifier to predict IDs that match using the return value
         "features" from compare_for_matches method
            Args:
                payload (dataframe) : Dataframe on the left or first dataframe.
                kpi_records (dataframe) : Dataframe on the right or second dataframe.
                threshold : probability
            Returns:
                matches : returns a dataframe of IDs of matches from each table in two columns named ID on Table1 and ID on Table2 respectively
        """
        ecm = recordlinkage.ECMClassifier()
        potential_matches = ecm.fit_predict(self.compare_for_matches(payload, kpi_records, threshold))
        matches = list(potential_matches)
        #matches = pd.DataFrame(list(potential_matches), columns=["ID On Table1", "ID on Table2"])
        return matches
