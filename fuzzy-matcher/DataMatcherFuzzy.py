import pandas as pd
import fuzzymatcher
from DataMatcher import DataMatcher


class DataMatcherFuzzy(DataMatcher):

    def __int__(self):
        self.left_on = []
        self.right_on = []

    def to_match(self, left_on, right_on):
        self.left_on = left_on
        self.right_on = right_on

        matched_results = fuzzymatcher.fuzzy_left_join(DataMatcher.read_data_one(self, data_one=None),
                                                       DataMatcher.read_data_two(self, data_two=None),
                                                       left_on,
                                                       right_on,
                                                       left_id_col='Account_Num',
                                                       right_id_col='Provider_Num')
