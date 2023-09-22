import pandas as pd
import os
home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


wc_info = pd.read_csv(home_path + '/wc_info.csv').fillna('')
concept_list = []

for row, l in wc_info[wc_info['所属同花顺行业'].str.contains('金属') ].iterrows():
    concept_list = concept_list + l['所属概念'].split(',')
    concept_list =  [x for x in concept_list if x]   # remove ''
hot_concepts = pd.DataFrame(concept_list).apply(pd.value_counts)
#hot_concepts = set(hot_concepts[hot_concepts[0] > 2].index)
hot_concepts.to_csv('cplist.csv')

# | wc_info['所属同花顺行业'].str.contains('家用电器')