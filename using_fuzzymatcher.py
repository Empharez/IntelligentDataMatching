import pandas as pd
import pathlib as Path
import fuzzymatcher

hospital_accounts = pd.read_csv(
    'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'
)
hospital_reimbursement = pd.read_csv(
    'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv'
)

# Columns to match on from df_left
left_on = ["Facility Name", "Address", "City", "State"]

# Columns to match on from df_right
right_on = [
    "Provider Name", "Provider Street Address", "Provider City",
    "Provider State"
]
# Now perform the match
# It will take several minutes to run on this data set
matched_results = fuzzymatcher.fuzzy_left_join(hospital_accounts,
                                               hospital_reimbursement,
                                               left_on,
                                               right_on,
                                               left_id_col='Account_Num',
                                               right_id_col='Provider_Num')
#print(matched_results.head())
df_comb = pd.DataFrame(matched_results)
#save as csv file
df_comb.to_csv("output.csv", index=False)
