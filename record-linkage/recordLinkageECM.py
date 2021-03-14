import recordlinkage as rl
import pandas as pd

"""
dfA = pd.read_csv(
    'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'
)
dfB = pd.read_csv(
    'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv'
)"""


def sorter(dfA, dfB, left_on, right_on):
    """Sorter to to make a subset of the record space (A * B) also accounting for spelling mistakes.

		Args:
			dfA : Dataframe on the left or first dataframe
			dfB : Dataframe on the right or second dataframe
			left_on(string) : The column name of the sorting key of the first/left dataframe.
			right_on(string) : The column name of the sorting key of the second/right dataframe.


		Returns:
			pairs : returns a multi-index of the pairs
		"""
    indexer = rl.Index()
    # Use sortedneighbor as a good option if data is not clean
    indexer.sortedneighbourhood(left_on=left_on, right_on=right_on)
    pairs = indexer.index(dfA, dfB)
    return pairs


# print(sorted)

def comparison(sorted_table, arg1, arg2, arg3, tableA, tableB):
    # Comparison step
    compare = rl.Compare()
    arg1
    arg2
    arg3
    features = compare.compute(sorted_table, tableA, tableB)
    return features


def compare_exact_val(col_left, col_right, new_col_label):
    compare = rl.Compare()
    return compare.exact(col_left, col_right, label=new_col_label)


def compare_string_with_prob(col_left, col_right, prob, new_col_label):
    compare = rl.Compare()
    res = compare.string(col_left,
                         col_right,
                         method='jarowinkler',
                         threshold=prob,
                         label=new_col_label)
    return res


"""test = compare_exact_val('City', 'Provider City', 'City')
test2 = compare_string_with_prob('Facility Name', 'Provider Name', 0.85, "Hosp_Name")
test3 = compare_string_with_prob('Address', 'Provider Street Address', 0.85, 'Hosp_Address')
result = comparison(sorted, test, test2, test3,dfA, dfB)
print(result)"""


def compare_data(dfA, dfB, left_on, right_on):
    pairs = sorter(dfA, dfB, left_on, right_on)
    compare = rl.Compare()
    compare.exact('City', 'Provider City', label='City')
    compare.string('Facility Name',
                   'Provider Name',
                   threshold=0.85,
                   label='Hosp_Name')
    compare.string('Address',
                   'Provider Street Address',
                   method='jarowinkler',
                   threshold=0.85,
                   label='Hosp_Address')
    features = compare.compute(pairs, dfA, dfB)
    return features


# print(test(dfA, dfB, "State", "Provider State"))

def predict_matches(dfA, dfB, left_on, right_on):
    ecm = rl.ECMClassifier()
    potential_matches = ecm.fit_predict(compare_data(dfA, dfB, left_on, right_on))
    matches = pd.DataFrame(list(potential_matches))
    return matches


# print(predict_matches(dfA, dfB, "State", "Provider State"))
