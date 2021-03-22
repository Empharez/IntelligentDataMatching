import unittest
import pandas as pd
import pandas.testing as pd_testing
import id_matcher


class TestIDMatcher(unittest.TestCase):
    def setUp(self):
        from IdMatcherPredictor import IDMatcher
        from recordLinkageECM import sorter, compare_data

        self.matcher = IDMatcher("State", "Provider State")

        self.csv_url1 = 'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'
        self.csv_url2 = 'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv'
        self.csv_a = pd.read_csv(self.csv_url1)
        self.dfA = pd.DataFrame(self.csv_a)
        self.csv_b = pd.read_csv(self.csv_url2)
        self.dfB = pd.DataFrame(self.csv_b)
        self.sorter = sorter(self.dfA, self.dfB, "State", "Provider State")
        self.compare = compare_data(self.dfA, self.dfB, "State", "Provider State")
        pass

    def test_dfA(self):
        pd_testing.assert_frame_equal(self.matcher.read_data(
            'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'), self.dfA)

    def test_dfB(self):
        pd_testing.assert_frame_equal(self.matcher.read_data(
            'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv'), self.dfB)

    def test_sorter(self):
        pd.testing.assert_index_equal(
            self.matcher.sorter(self.dfA, self.dfB),
            self.sorter
        )

    def test_compare(self):
        self.assertEquals(self.matcher.compare_for_matches(self.dfA, self.dfB, 0.85),
                          self.compare)


if __name__ == '__main__':
    unittest.main()
