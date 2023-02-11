# universal import
from universal_imports import *

# import features
import helper

#------------------------------

def get_study_order(in_df):
    """
    DESCRIPTION
        Given a study set, return a study order with the following characteristics:
            1. Contains no mastered word (mastery = 3)
            2. Words with the highest mastery are placed first
            3. Words with the same mastery are placed randomly
    """

    # make a copy of the dataframe
    df = in_df.copy()

    # filter the dataframe with different mastery levels
    df_2 = df[df["Mastery"] == 2]
    df_1 = df[df["Mastery"] == 1]
    df_0 = df[df["Mastery"] == 0]

    # get the indicies of each mastery level
    indices_2 = list(df_2.index.values)
    indices_1 = list(df_1.index.values)
    indices_0 = list(df_0.index.values)

    # shuffle the indices
    random.shuffle(indices_2)
    random.shuffle(indices_1)
    random.shuffle(indices_0)

    # concatenate the indices into the final study order
    study_indices = indices_2 + indices_1 + indices_0

    # return the study order
    return study_indices
    
#------------------------------