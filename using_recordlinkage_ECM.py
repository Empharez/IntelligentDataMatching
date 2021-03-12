import pickle

import recordlinkage as rl
import pandas as pd

dfA = pd.read_csv(
    'https://github.com/chris1610/pbpython/raw/master/data/hospital_account_info.csv'
)
dfB = pd.read_csv(
    'https://raw.githubusercontent.com/chris1610/pbpython/master/data/hospital_reimbursement.csv'
)

indexer = rl.Index()
#indexer.block(left_on='State', right_on='Provider State')

# Use sortedneighbor as a good option if data is not clean
indexer.sortedneighbourhood(left_on='State', right_on='Provider State')
candidates = indexer.index(dfA, dfB)
#print(len(candidates))

# Comparison step
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
features = compare.compute(candidates, dfA,
                           dfB)


#features_df = features.sum(axis=1).value_counts().sort_index(ascending=False)
"""features_df = features[features.sum(axis=1) > 1].reset_index()
print(features_df)
df_comb = pd.DataFrame(features_df)
#save as csv file
df_comb.to_csv("features.csv", index=False)"""

ecm = rl.ECMClassifier()
matches = ecm.fit_predict(features)
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(matches, f)

potential_matches = pd.DataFrame(list(matches)) #convert tuple to dataframe
potential_matches = potential_matches[potential_matches.sum(axis=1) > 1].reset_index(inplace=True)
potential_matches['score'] = potential_matches.loc[:, 'City':'Hosp_Address'].sum(axis=1)
#print(matches)

df_comb = pd.DataFrame(potential_matches)
#save as csv file
df_comb.to_csv("matches.csv", index=False)
"""

true_linkage = pd.Series(features, index=pd.MultiIndex(matches))

logrg = rl.LogisticRegressionClassifier()
logrg.fit(features[true_linkage.index], true_linkage)

pred = logrg.predict(matches)

print("pred--->>>", pred)"""

