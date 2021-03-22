import unittest
import pandas as pd
import pandas.testing as pd_testing
import id_matcher



class TestIDMatcher(unittest.TestCase):
    def setUp(self):
        from IdMatcherPredictor import IDMatcher

        self.matcher = IDMatcher("State", "Provider State")

        self.csv_url1 = 'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'
        self.csv_url2 = 'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv'
        self.csv_a = pd.read_csv(self.csv_url1)
        self.dfA = pd.DataFrame(self.csv_a)
        self.csv_b = pd.read_csv(self.csv_url2)
        self.dfB = pd.DataFrame(self.csv_b)
        pass

        def test_dfA():
            self.assertEqual(self.matcher.read_data(
                'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'), self.dfA)





if __name__ == '__main__':
    unittest.main()
