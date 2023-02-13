# universal import
from universal_imports import *

#------------------------------

def datetime_convert(target_string):
    """
    DESCRIPTION
        Convert a simple YYYY-MM-DD HH:MM to a datetime object
    """

    return pd.to_datetime(target_string)

#------------------------------

def unique_id_generator():
    """
    DESCRIPTION:
        Generate a unique ID (for each transaction)
        The idea is simple, convert the current datetime.now() into an integer

    OUTPUT SIGNATURE:
        1. unique_id (str): the unique ID
    """
    
    # get current time
    now = datetime.datetime.now()

    # convert to timestamp (seconds since 1970)
    now_float = now.timestamp()

    # convert to a unique integer
    now_int = int(now_float * 10**6)

    # string convert it to avoid scientific notation display
    now_str = str(now_int)

    return now_str

#------------------------------

class data_store():
    """
    DESCRIPTION:
        A simple class to pass around data and objects

    NOTE:
        Re-implement this to have a dictionary-like operation?
    """

    login_status = False

    user = None
    chosen_set_name = None
    set_df = None
    set_path = None

    to_export_df = None
    
    # current entry
    current_index = None

#------------------------------

def df_iterate(df, column):
    '''
    BLUE PRINT FUNCTION
    Use this blue print to loop through a Pandas dataframe
    I swear to God I can't remember the syntax for this even though I worked on Pandas for years lmao
    '''

    # loop through each row
    for i in range (len(df)):

        # access the cell value at the row and column
        cell_at_col = df.at[i, column]

        # adjust the cell value to a random integer
        cell_at_col = random.randint(0, 100)

        # why using .at[] is great? because it adjusts on the original dataframe directly, no messy copy

        # alternatively, you can also use
        cell2_at_col = df[column][i] # attention that it is column then row

        # you can also adjust the value at the cell by
        cell2_at_col = random.randint(0, 100)

        # but this will raise a warning about editing the copy of the dataframe bla bla

#------------------------------

def get_study_sets(user):
    """
    DESCRIPTION
        - Given a user, returns all study sets under that user
    """

    all_users_path = "Data/Users"
    user_path = all_users_path + "/" + user

    # get all files stored in the user's folder
    files = os.listdir(user_path)

    # filter out all files that are not study sets
    study_sets = [file for file in files if file.endswith(".csv")]

    # remove the .csv extension
    study_sets = [file[:-4] for file in study_sets]
    
    return study_sets

#------------------------------

def update_data_after_answer(assessment, df, current_index):
    """
    DESCRIPTION:
        Update the data to keep track of the user's progress on the study set

    INPUT SIGNATURE:
        1. assessment (boolean): whether the user got the answer correct or not
        2. df (Pandas dataframe): the study set dataframe
        3. current_index (int): the index of the current word that is being tested

    OUTPUT SIGNATURE:
        1. df (Pandas dataframe): the updated study set dataframe
    """

    # update Total Tries
    df.at[current_index, "Total Tries"] += 1

    if result == True:

        # update Total Success
        df.at[current_index, "Total Success"] += 1

        # update Mastery
        if df.at[current_index, "Mastery"] < 3:
            df.at[current_index, "Mastery"] += 1

    else:
        # update Mastery
        if df.at[current_index, "Mastery"] > 0:
            df.at[current_index, "Mastery"] -= 1

    return df

#------------------------------

def reformat_set_df(in_df):
    """
    DESCRIPTION:
        - Reformat the study set dataframe

    INPUT SIGNATURE:
        1. in_df (Pandas dataframe): the input dataframe
    
    OUTPUT SIGNATURE:
        1. set_df (Pandas dataframe): the reformatted dataframe
        2. False (boolean): if the dataframe is already reformatted
    """

    # make a copy of the in-df
    set_df = in_df.copy()

    # rename column 0 to "Word"
    set_df.rename(columns = {0: "Word"}, inplace = True)

    # rename column 1 to "Definition"
    set_df.rename(columns = {1: "Definition"}, inplace = True)

    # # rename column 0 and 1
    # mapping = {set_df.columns[0]:'Word', set_df.columns[1]: 'Definition'}
    # set_df = set_df.rename(columns=mapping, inplace = True)

    # add column "Mastery" with all values as 0
    set_df["Mastery"] = 0

    # add column "Total Tries"
    set_df["Total Tries"] = 0

    # add column "Total Success"
    set_df["Total Success"] = 0

    # return the formatted dataframe
    return set_df

#------------------------------

def update_and_export_data(data_store_object):
    """
    DESCRIPTION:
        - Get the latest learning progress from the data store object
        - Export and overwrite to the hard drive
    """

    # make a copy to avoid upstream changes
    data_store = data_store_object

    # update the data
    final_df = data_store.to_export_df.copy()

    # path
    path = data_store.set_path
    
    # export the dataframe
    final_df.to_csv(path, index = False)

    # update the set_df object
    data_store.set_df = final_df

    # return the updated data store object
    return data_store

