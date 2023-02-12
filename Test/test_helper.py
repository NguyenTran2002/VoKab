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

class test_get_study_sets(unittest.TestCase):
      
    def setUp(self):
        
        # test user
        self.user = "sample_user_1"

        # the expected sets to be returned from test user
        self.expected_sets = ["Food", "French Elementary", "Simple English", "Weather"]

        # sort the list in the default order of sort() function
        self.expected_sets.sort()

    def test_get_study_sets(self):

        # get the output from the function we're testing
        found_sets = helper.get_study_sets(self.user)

        # sort the list in the default order of sort() function
        found_sets.sort()

        # check if the produced dataframe and the processed dataframe are the same
        self.assertEqual(found_sets, self.expected_sets)

#------------------------------

if __name__ == '__main__':
    unittest.main()