import unittest

# navigate to the Features folder
import sys
sys.path.append(sys.path[0]+'/../Features')

# UNIVERSAL IMPORT
from universal_imports import *

# import other features
import helper

# Import testing specific libraries
from pandas.testing import assert_frame_equal

#------------------------------

class test_reformat_main_df(unittest.TestCase):
      
    def setUp(self):
        
        # read in mint.csv data
        self.input_df = pd.read_csv('Data/Test Data/reformat_main_df/mint_test.csv')

        # read in the expected output
        self.expected_df = pd.read_csv('Data/Test Data/reformat_main_df/mint_processed_test.csv')

        # convert the date column to datetime
        self.expected_df["Date"] = pd.to_datetime(self.expected_df["Date"])

        # export the expected output to csv
        self.expected_df.to_csv("Data/Test Data/reformat_main_df/mint_processed_test.csv", index=False)

        # re_read in the expected output
        self.expected_df = pd.read_csv('Data/Test Data/reformat_main_df/mint_processed_test.csv')

    def test_reformat_main_df(self):

        result = helper.reformat_main_df(self.input_df)

        # export result to csv
        result.to_csv("Data/Test Data/reformat_main_df/result_test.csv", index=False)

        # read in the result
        result_re = pd.read_csv("Data/Test Data/reformat_main_df/result_test.csv")

        # check if the produced dataframe and the processed dataframe are the same
        assert_frame_equal(result_re, self.expected_df, check_dtype=False)

#------------------------------

if __name__ == '__main__':
    unittest.main()