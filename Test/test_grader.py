import unittest

# navigate to the Features folder
import sys
sys.path.append(sys.path[0]+'/../Features')

# UNIVERSAL IMPORT
from universal_imports import *

# import other features
import helper
import grader

# Import testing specific libraries
from pandas.testing import assert_frame_equal

#------------------------------

class test_compare_2_words(unittest.TestCase):
      
    def setUp(self):

        # correct words
        self.main_df = pd.read_csv('Data/Test Data/reformat_main_df/mint_processed_test.csv')

        # convert the date column to datetime
        self.main_df["Date"] = pd.to_datetime(self.main_df["Date"])

    def test_categorize(self):

        # the expected output
        expected = {}
        expected["Food Delivery"] = -16.19
        expected["Electronics & Software"] = -8.32
        expected["Food & Dining"] = -20.36
        expected["Pharmacy"] = - 6.88

        # get the function's output
        output = categorical_spend.categorize(self.main_df)

        # equality test
        self.assertDictEqual(expected, output)

#------------------------------

if __name__ == '__main__':
    unittest.main()