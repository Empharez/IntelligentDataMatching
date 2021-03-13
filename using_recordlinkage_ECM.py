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




ecm = rl.ECMClassifier()
matches = ecm.fit_predict(features)
matches = pd.DataFrame(list(matches))
print(matches)




df_comb = pd.DataFrame(matches)
#save as csv file
df_comb.to_csv("matches.csv", index=True)


