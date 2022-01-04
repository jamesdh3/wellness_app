import pandas as pd 
import pdb
import matplotlib.pyplot as plt 

input_file = pd.read_csv('C:/Users/baba/Documents/phone_apps/tmp_db/test_db_graph.csv')


import pdb; pdb.set_trace() 
activities = input_file['activity'].unique().tolist()
'''
tuple_dict = dict() 
for a in activities: 
    # subset to activity 
    this_activity = input_file.loc[input_file['activity'].eq(a), ]

    # create tuple for each entry 
    this_activity['xy_vals'] = list(zip(this_activity['date_inserted'], this_activity['time_elapsed']))
    xy_vals = this_activity['xy_vals'].unique().tolist() 

    # save to dict 
    tuple_dict[a] = xy_vals

'''
m_vals = input_file.loc[input_file['activity'].eq('meditate'), ]
plt.plot(m_vals['date_inserted'], m_vals['time_elapsed'], label='meditate')

w_vals = input_file.loc[input_file['activity'].eq('workout'), ] 
plt.plot(w_vals['date_inserted'], w_vals['time_elapsed'], label='workout') 

d_vals = input_file.loc[input_file['activity'].eq('walk_dog'), ]
plt.plot(d_vals['date_inserted'], d_vals['time_elapsed'], label='walk dog')


plt.legend() 
plt.show() 

