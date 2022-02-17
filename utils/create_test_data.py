''' Creates a dummy dataset 
    
    This script should ask the user for the number of entries requested, and it'll generate random rows 

    Should work with any time-series data 
'''

# import libraries 
import pandas as pd 
import numpy as np
from datetime import ( 
    datetime,
    timedelta
)
import random

cols = ['entry_id', 'activity', 'time_elapsed', 'date_inserted', 'time_inserted']
allowed_activities = ['meditate', 'workout', 'walk_dog']


def generate_random_date(start_date, end_date):
    ''' Returns a random date that's between a given start and end date
    '''
    time_between = end_date - start_date 
    days_between = time_between.days 

    # now pick a random date 
    random_num_days = random.randrange(days_between)
    random_date = start_date + timedelta(days=random_num_days)
    return random_date 

def generate_random_timestamp(): 
    '''
    '''
    pass 


def create_test_data(num_entries, start_date, end_date): 
    '''
    '''
    dates = [] 
    activities = [] 
    time_entries = np.random.randint(0, 1000, num_entries)
    for i in list(range(0,num_entries)): 
        dates += [generate_random_date(start_date, end_date)]
        activities += [allowed_activities[random.randrange(len(allowed_activities))]]
    
    # TODO: create list of random time_stamps

    # create dataframe 
    data = pd.DataFrame(data={'activity':activities, 'time_elapsed':time_entries, 'date_inserted':dates})  

    # insert primary key 
    data['entry_id'] = data.index 
    return data[['entry_id','activity','time_elapsed','date_inserted']]



def export_data(num_entries): 
    '''
    '''

    pass 


if __name__ == "__main__": 
    from sys import argv 
    num_entries = int(argv[1])
    start_date = datetime.strptime(argv[2], '%m/%d/%Y').date()
    end_date =  datetime.strptime(argv[3], '%m/%d/%Y').date()

    df = create_test_data(num_entries, start_date, end_date)
    import pdb; pdb.set_trace() 
    # export_data(df) 
