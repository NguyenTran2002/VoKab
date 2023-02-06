# universal import
from universal_imports import *

# import features
import helper

#------------------------------

def check_answer(user_answer, df, current_index):
    """
    DESCRIPTION
        Return True if the answer is correct
        Return the correct answer if the answer is false
    """

    # get the correct answer
    correct_answer = df.at[current_index, "Word"]

    # compare the two answers
    if user_answer == correct_answer:
        return True
    else:
        return correct_answer
    
#------------------------------