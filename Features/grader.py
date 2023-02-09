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

    # get lower case of user_answer
    user_answer_lower = user_answer.lower()

    # get lower case of correct_answer
    correct_answer_lower = correct_answer.lower()

    # compare the two answers
    if user_answer_lower == correct_answer_lower:
        return True
    else:
        return correct_answer
    
#------------------------------