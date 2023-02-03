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

class test_check_person(unittest.TestCase):
      
    def setUp(self):
        pass

    def test_check_person(self):

        # list of inputs
        given = ['duy_nguyen', 'nhim',\
            'minh_tran', 'zhihan',\
            'antonio', 'huong_trinh', 'ori', 'grandparents',\
            'john_win', 'Friends', 'rachel_blossom',\
            'mikey tike', 'jonny won']

        # list of corresponding expected output
        expected = ['Duy Nguyen', 'Nhim',\
            'Minh Tran', 'Zhihan',\
            'Antonio', 'Huong Trinh', 'Ori', 'Grandparents',\
            'John Win', 'Friends', 'Rachel Blossom',\
            False, False]

        # get the output
        output = []
        for i in range(len(given)):
            output.append(helper.check_person(given[i]))
        
        # loop through the list of given and expected outcome and compare multiple cases
        for i in range(len(given)):
            self.assertEqual(expected[i], output[i])

#------------------------------

class test_single_account_transactions(unittest.TestCase):
      
    def setUp(self):
        pass

    def test_check_person(self):

        # list of inputs
        given = ['duy_nguyen', 'nhim',\
            'minh_tran', 'zhihan',\
            'antonio', 'huong_trinh', 'ori', 'grandparents',\
            'john_win', 'Friends', 'rachel_blossom',\
            'mikey tike', 'jonny won']

        # list of corresponding expected output
        expected = ['Duy Nguyen', 'Nhim',\
            'Minh Tran', 'Zhihan',\
            'Antonio', 'Huong Trinh', 'Ori', 'Grandparents',\
            'John Win', 'Friends', 'Rachel Blossom',\
            False, False]

        # get the output
        output = []
        for i in range(len(given)):
            output.append(helper.check_person(given[i]))
        
        # loop through the list of given and expected outcome and compare multiple cases
        for i in range(len(given)):
            self.assertEqual(expected[i], output[i])

#------------------------------

class test_sum_lendings(unittest.TestCase):

    def setUp(self):

        # read in the data from the test data folder
        path = "Data/Test Data/sum_lendings/testData_lendings_tracker.csv"
        self.lendings_df = pd.read_csv(path)

    def test_sum_lendings(self):

        # the expected dictionary output
        expected_dict = {\
            "baka_kuta" : 2139.24,\
            "levi_ackerman" : 65.77,\
            "eren_yeager" : 209.27,\
            "reiner_braun" : 295.67,\
            "mikasa_ackerman" : 187.04}

        expected_total = 2896.99

        # get the output
        output_dict, output_total = helper.sum_lendings(self.lendings_df)

        self.assertEqual(expected_dict, output_dict)
        self.assertEqual(expected_total, output_total)

#------------------------------

class test_find_entries_in_only_one_of_two_dfs(unittest.TestCase):

    def setUp(self):

        # read in all relevant dataframes
        self.df1 = pd.read_csv("Data/Test Data/find_entries_in_only_one_of_two_dfs/df_1.csv")
        self.df2 = pd.read_csv("Data/Test Data/find_entries_in_only_one_of_two_dfs/df_2.csv")
        self.df1_n2 = pd.read_csv("Data/Test Data/find_entries_in_only_one_of_two_dfs/df1_n2.csv")
        self.df2_n1 = pd.read_csv("Data/Test Data/find_entries_in_only_one_of_two_dfs/df2_n1.csv")

        self.df3 = pd.read_csv("Data/Test Data/find_entries_in_only_one_of_two_dfs/df_3.csv")
        # df3 is for the raise exception test case

    def test_find_entries_in_only_one_of_two_dfs(self):

        # get the output for normal cases
        out_df1_n2, out_df2_n1 = helper.find_entries_in_only_one_of_two_dfs(self.df1, self.df2)

        # reset all indexes
        out_df1_n2.reset_index(inplace=True)
        out_df2_n1.reset_index(inplace=True)
        self.df1_n2.reset_index(inplace=True)
        self.df2_n1.reset_index(inplace=True)

        # drop the column named "index"
        out_df1_n2.drop(columns=["index"], inplace=True)
        out_df2_n1.drop(columns=["index"], inplace=True)
        self.df1_n2.drop(columns=["index"], inplace=True)
        self.df2_n1.drop(columns=["index"], inplace=True)

        print(out_df1_n2.to_string())
        print(self.df1_n2.to_string())

        result_1 = out_df1_n2.equals(self.df1_n2)
        result_2 = out_df2_n1.equals(self.df2_n1)

        # compare the output with the expected output
        self.assertEqual(result_1, True)
        self.assertEqual(result_2, True)

        # get the output for exception case
        with self.assertRaises(Exception) as exc:
            out_df3 = helper.find_entries_in_only_one_of_two_dfs(self.df1, self.df3)
        self.assertEquals(str(exc.exception), "ERROR in find_entries_in_only_one_of_two_dfs: the 2 dataframes do not have the same columns or columns order")

#------------------------------

if __name__ == '__main__':
    unittest.main()