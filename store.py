'''
    Creates a data store and
    Syncs it every second to a file
'''

import pickle
from datetime import timedelta
from timeloop import Timeloop
from data_types import Store

SYNC_INTERVAL_SEC = 5

STORE = Store()

PICKLE_SYNC = Timeloop()

@PICKLE_SYNC.job(interval=timedelta(seconds=SYNC_INTERVAL_SEC))
def sync_store():
    ''' Sync the store in memory to a store file'''
    # print("Syncing Store...")

    data = get_store()
    with open('store.p', 'wb') as file:
        pickle.dump(data, file)

    # print("Sync Complete!")

def get_store():
    ''' Return the global store '''
    global STORE
    return STORE


def start_store_sync():
    '''
        Loads a store into memory or creates new
        Then, Starts the sync scheduler
    '''
    # Initial Syncing store file to store in memeory
    global STORE
    try:
        STORE = pickle.load(open("store.p", "rb"))
    except FileNotFoundError:
        print("No store files found...")

    # Start scheduler to sync variable to file
    PICKLE_SYNC.start(block=False)
