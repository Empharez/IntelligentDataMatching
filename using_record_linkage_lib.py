import pandas as pd
import recordlinkage as rl


# Re-read in the data using the index_col
hospital_accounts = pd.read_csv(
    'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv',
    index_col='Account_Num'
)
hospital_reimbursement = pd.read_csv(
    'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv',
    index_col='Provider_Num'
)

#print(hospital_reimbursement.head())
#print(hospital_accounts.head())
df_a = pd.DataFrame(hospital_accounts)
df_b = pd.DataFrame(hospital_reimbursement)
#print(df_a, df_b)

indexer = rl.Index()
#indexer.block(left_on='State', right_on='Provider State')

# Use sortedneighbor as a good option if data is not clean
indexer.sortedneighbourhood(left_on='State', right_on='Provider State')
candidates = indexer.index(df_a, df_b)
print(len(candidates))

# 14s using sorted neighbor
# 7s using blocking
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
features = compare.compute(candidates, hospital_accounts,
                           hospital_reimbursement)

print(features)



"""true_linkage = pd.Series(YOUR_GOLDEN_DATA, index=pd.MultiIndex(YOUR_MULTI_INDEX))

logrg = rl.LogisticRegressionClassifier()
logrg.fit(features[true_linkage.index], true_linkage)

logrg.predict(features)
"""

# Sum the comparison results.
features.sum(axis=1).value_counts().sort_index(ascending=False)
# Get the potential matches
potential_matches = features[features.sum(axis=1) > 1].reset_index()
potential_matches['Score'] = potential_matches.loc[:, 'City':'Hosp_Address'].sum(axis=1)
#print(matched_results.head())
df_comb = pd.DataFrame(potential_matches)
#save as csv file
df_comb.to_csv("rl-output.csv", index=False)
potential_matches.head()
print(hospital_accounts.loc[51216,:])
print(hospital_reimbursement.loc[268781,:])