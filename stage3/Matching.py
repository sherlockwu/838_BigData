import py_entitymatching as em
import pandas as pd

table_a = em.read_csv_metadata('anime_1.csv', key='ID')
table_b = em.read_csv_metadata('animePlayer.csv', key='ID')

type_blocker = em.AttrEquivalenceBlocker()
type_blocker_result = type_blocker.block_tables(table_a, table_b, 'Type', 'Type')
print(type_blocker_result)

overlap_blocker = em.OverlapBlocker()
overlap_blocker_result = overlap_blocker.block_candset(type_blocker_result, 'Genres', 'Genres', overlap_size=4)
print(overlap_blocker_result)

year_blocker = em.OverlapBlocker()
year_blocker_result = year_blocker.block_candset(overlap_blocker_result, 'Year','Year',q_val=4 , word_level=False,overlap_size=4)
print(year_blocker_result)

year_blocker_result.to_csv('candidate_set.csv')

#max = overlap_blocker_result.max()
#print '%s, %s, %s' % (max['_id'], max['ltable_ID'], max['rtable_ID'])
#C = ab.block_tables(A, B, 'zipcode', 'zipcode', l_output_attrs=['name'], r_output_attrs=['name'])
#csv = pd.read_csv('animePlayerFilter.csv',error_bad_lines=False)
