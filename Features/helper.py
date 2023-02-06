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

def check_person(tag):
    """
    DESCRIPTION:
        This function is solely for the use of the main developer of this program.
    
    INPUT SIGNATURE:
        1. tag (string): a tag from the original dataframe

    OUTPUT SIGNATURE:
        2. name (string): the name of the person said tag is referring to
    """

    person_tags = ['duy_nguyen', 'nhim',\
       'minh_tran', 'zhihan',\
       'antonio', 'huong_trinh', 'ori', 'grandparents',\
       'john_win', 'Friends', 'rachel_blossom', 'professional_relationships']

    if tag in person_tags:

        # replace _ with space
        name = tag.replace("_", " ")

        # capitalize the first letter of each word
        name = name.title()

        return name

    else:
        return False

#------------------------------

def update_data_after_answer(result, df, current_index):

    """
    DESCRIPTION:
        Update the data to keep track of the user's progress on the study set
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

def single_account_transactions(in_main_df, account_name):
    """
    DESCRIPTION:
        Return all transactions of a specific account

    INPUT SIGNATURE:
        1. main_df (dataframe): the main dataframe
        2. account_name (string): the name of the account

    OUTPUT SIGNATURE:
        1. account_df: pandas dataframe
    """

    # filter the main dataframe with the account name
    account_df = in_main_df[in_main_df["Account Name"] == account_name]

    # reset the index
    account_df.reset_index(drop=True, inplace=True)

    # return the account dataframe
    return account_df

#------------------------------

def my_metrics(in_account_objects):
    """
    DESCRIPTION:
        Given a list of tallied account objects, return the networth of the user
    """
    my_networth = 0
    my_cash = 0
    my_asset = 0

    for account in in_account_objects:

        my_networth += account.get_value()
        my_networth += account.get_asset()

        my_cash += account.get_value()

        my_asset += account.get_asset()

    return my_networth, my_cash, my_asset

#------------------------------

def sum_lendings(in_lending_tracker_df):
    """
    DESCRIPTION:
        Given a dataframe containing all the lendings, return a dictionary with the following structure:
        {person 1 : amount lended, person 2 : amount lended, ...}

        also returns the total amount lended (int)
    """

    lendings_dict = {}
    total_lendings = 0

    # loop through the dataframe and read the Amount and Labels column
    for i in range(len(in_lending_tracker_df)):

        # get the amount
        amount = in_lending_tracker_df.at[i, "Amount"]
        total_lendings += amount

        # get the labels
        tag = in_lending_tracker_df.at[i, "Labels"]

        # if there are two tag, take the first one
        if tag.find(" ") != -1:
            tag = tag[:tag.find(" ")]
        else:
            pass

        # if the tag is not in the dictionary, add it
        if tag not in lendings_dict:
            lendings_dict[tag] = amount

        else:
            lendings_dict[tag] += amount

    return lendings_dict, total_lendings

#------------------------------

def my_lendings_and_recollections(in_main_df):
    """
    ERROR: DO NOT USE THIS METHOD; IT IS NOT WORKING PROPERLY

    DESCRIPTION:
        Loop through the main dataframe and return how much do everyone still owes you
        (a bit complicated to write a function that tally who owes me what, so I'll tackle it later)

        If the returned value is negative, then there are debts to be recollected
    """
    my_lendings = 0 # will always be negative
    my_collections = 0 # will always be positive

    # loop through the main dataframe
    for i in range(len(in_main_df)):

        # if the transaction is a lending
        if in_main_df.at[i, "Category"] == "Lending":

            # add the transaction to the total
            my_lendings += in_main_df.at[i, "Amount"] # the value of the transaction will be negative

        # if the transaction is a collection
        elif (in_main_df.at[i, "Category"] == "Reimbursement") or (in_main_df.at[i, "Category"] == "Debt Collection"):

            # add the transaction to the total
            my_collections += in_main_df.at[i, "Amount"] # the value of the transaction will be positive

    return (my_lendings + my_collections)

#------------------------------

def get_all_account_dfs(account_names):
    """
    DESCRIPTION:
        Return a Pandas Dataframe containing each account and its overview information as a line

    INPUT SIGNATURE:
        1. account_names (list): a list of account names

    SOURCE:
        https://softhints.com/how-to-merge-multiple-csv-files-with-python/
    """

    # clean up the accounts not in use from the directory
    clean_up_accounts_data(account_names)

    path = "Data/Accounts"

    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index=True)

    # drop the column Account
    df_merged.drop(columns=['Account'], inplace = True)

    # sort the dataframe by the column Account Type
    df_merged.sort_values(by = ['Account Type', 'Display Name'], inplace = True)

    # set the column Unique ID to be the index
    df_merged.set_index("Unique ID", inplace=True)

    # rename the column Value to be Cash Equivalent
    df_merged.rename(columns={"Value": "Available Cash Equivalents"}, inplace=True)

    # add a column "Net Value" = the total of "Value" and "Asset" next to the column "Asset"
    df_merged.insert(3, "Net Value", df_merged["Available Cash Equivalents"] + df_merged["Asset"])

    return df_merged

#------------------------------

def clean_up_accounts_data (account_names):
    """
    DESCRIPTION:
        Given a list of account names, delete all .csv files within Data/Accounts that are not in the list
    """

    path = "Data/Accounts/"

    using_files = []

    for account in account_names:
        using_files.append(path + account + ".csv")

    all_files = os.listdir(path)

    for file in all_files:

        full_file_path = path + file

        if full_file_path not in using_files:
            os.remove(full_file_path)

#------------------------------

def clean_up_all_but (folder, starts_with, not_delete_id, ends_with):
    """
    DESCRIPTION:
        look into a folder, delete all files that starts with a certain name that does not have the "not-delete id"

    EXAMPLE:
        for the not-delete-file: "overall_graph_146143154145.csv"
        starts_with is: "overall_graph_"
        not_delete_id is: "146143154145"
        ends_with is: ".csv"
    """

    # not_delete_file = folder + starts_with + not_delete_id + ends_with

    all_files_name = os.listdir(folder)

    all_files_path = [] 
    for file_name in all_files_name:
        file_path = folder + file_name
        all_files_path.append(file_path)

    for file in all_files_path:

        if starts_with in file:

            if not_delete_id not in file:
                os.remove(file)

#------------------------------

def back_up_original_df ():
    """
    DESCRIPTION:
        make a copy of the mint_processed.csv file
    """

    # read the mint_processed.csv file
    df = pd.read_csv("Data/mint.csv")

    # export with a different name
    df.to_csv("Data/mint_backup.csv", index = False)

#------------------------------

def find_entries_in_only_one_of_two_dfs(df1, df2):
    """
    DESCRIPTION:
        given 2 dataframes, return

    OUTPUT SIGNATURE:
        df1_n2 (dataframe): a dataframe containing all the entries in df1 that are not in df2
        df2_n1 (dataframe): a dataframe containing all the entries in df2 that are not in df1
    """

    # get the columns in df1 as a list
    df1_columns = df1.columns.tolist()

    # get the columns in df2 as a list
    df2_columns = df2.columns.tolist()

    # check if the columns are the same
    if df1_columns != df2_columns:
        raise Exception("ERROR in find_entries_in_only_one_of_two_dfs: the 2 dataframes do not have the same columns or columns order")

    else:

        df1.to_csv("Data/df1.csv", index = False)
        df2.to_csv("Data/df2.csv", index = False)
        df2.drop_duplicates().to_csv("Data/df2_drop_duplicates.csv", index = False)

        # merge two DataFrames and create indicator column of rows that exists in df1 only
        df1_n2 = df1.merge(df2.drop_duplicates(), on = df1_columns, how = 'left', indicator=True)
        df2_n1 = df2.merge(df1.drop_duplicates(), on = df1_columns, how = 'left', indicator=True)

        #create DataFrame with rows that exist in first DataFrame only
        df1_n2 = df1_n2[df1_n2['_merge'] == 'left_only']
        df2_n1 = df2_n1[df2_n1['_merge'] == 'left_only']

        # drop the column _merge
        df1_n2.drop(columns=['_merge'], inplace = True)
        df2_n1.drop(columns=['_merge'], inplace = True)

        # write and re-read the dataframes to make sure the index is correct
        df1_n2.to_csv("Data/df1_n2.csv", index = False)
        df2_n1.to_csv("Data/df2_n1.csv", index = False)

        df1_n2_out = pd.read_csv("Data/df1_n2.csv")
        df2_n1_out = pd.read_csv("Data/df2_n1.csv")

        return df1_n2_out, df2_n1_out

#------------------------------