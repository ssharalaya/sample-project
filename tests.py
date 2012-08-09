#######################################################################################################################
# Disclaimer - Production code
#
# Copyright (c) 2012 
#
# This is company property. So, do not distribute. If you go ahead and distribute, you will NOT get to meet the most
# interesting man in the world, whose achievements are not limited to :
#
# 1. He once taught a German shepherd to bark in Spanish.
# 2. He is left-handed. And right-handed.
# 3. He Doesn't Always Test His Code, but when He Does, He Does It in Production
# 4. Respected archaeologists fight over his discarded apple cores.
# 5. His organ donation card also lists his beard.
#
#######################################################################################################################

"""
This is a module to maintain simple unit test cases keeping in mind the operations in the main API. This can be 
run with the nose module
"""

import logging
import pdb
import os
import nose
import shutil
from nose.tools import raises, assert_raises, assert_equal, assert_not_equal

from .exception_messages import (MerchantNameNotFoundError, MerchantIdNotFoundError, CsvFileNotFoundError,\
                                    CsvFileRelatedError, InvalidRequiredFieldError, NotUniqueError)
from .api import CsvFileReader, CsvOperations


class TestInputFile (object):
    """
    A few basic sanity checks for the csv file and its contents
    """
    def setUp (self):
        """
        Initializing the test by creating directory and test csv file for the positive and the negative tests
        """
        if 'dummy_dir' not in os.listdir(os.path.abspath(os.getcwd())):
           os.mkdir('dummy_dir')

        if 'test_dir' not in os.listdir(os.path.abspath(os.getcwd())):
            os.mkdir('test_dir')

        if 'wrong_dir' not in os.listdir(os.path.abspath(os.getcwd())):
            os.mkdir('wrong_dir')

        # Creating two new directories for testing purposes. Only one of the directories will have a test csv file.
        current_working_directory = os.getcwd()

        # Change current working  directory to 'test_dir' and creating a test csv file with test data
        os.chdir('test_dir')
        testfilename = 'test_file.csv'
        file_handle = open(testfilename, 'w')
        csv_text =\
        """\
Purple Cow,2001,206-339-8960,Nico Robin
Panera Bread,1002,(555)232-3422,Mario Andretti
Panchos Tacos,2003,343 222 3322 ext. 342,Michael Johnson
Curry Pot,1004,+44 232 3222 3322,Susan Vettel
Panera Bread,2005,211-211-2333,David Beckham"""

        file_handle.writelines(csv_text)
        file_handle.close()

        # Restore working directory to the previous one
        os.chdir(current_working_directory)

        # Change working directory to 'wrong_dir' directory
        os.chdir('wrong_dir')
        wrong_filename = 'test_file.csssssssv'
        filehandle = open(wrong_filename, 'w')
        filehandle.close()

        os.chdir(current_working_directory)
 
    @raises (CsvFileNotFoundError)
    def test_for_csv_file_presence (self):
        """
        Check if there is a csv file in the location specified.
        """
        # Do a negative test.
        # Assert if CsvFileNotFoundError is raised by our API if incorrect directory name is fed or if the directory
        # has no csv files in it.
        
        a = CsvOperations('unknown_dir') # No such directory exists, should raise error

        # Now that a test file has been created, ensuring the error is raised for incorrect file extension
        b = CsvOperations('wrong_dir')


    def test_read_csv_into_dict (self):
        """
        Check if the csv file has been correctly parsed in to a dictionary format
        """
        a = CsvOperations ('test_dir')
        a.read_csv_into_dict('test_dir/test_file.csv')
        assert (a.datadict['1'][0] == 'Purple Cow')
        assert not (a.datadict['3'][1] == 'Purple Cow') 
                      

    def test_lookup_info_by_name (self):
        """
        Check if the lookup method in our api and exception handling works as expected
        """
        b = CsvOperations ('test_dir')
       
        # Check to see if the exception message is raised when we send wrong data
        assert_raises (MerchantNameNotFoundError, b.lookup_info_by_name, 'Tacson Del Mar')

        c = CsvOperations ('test_dir', merch_name='Panera Bread')
        for name in b.found_merchant_by_name:
            assert name[0] == 'Panera Bread'


    def test_lookup_info_by_id (self):
        """
        Check if the merch_id lookup method in our api and exception handling works as expected
        """
        x = CsvOperations ('test_dir')

        # Check to see if exception is being raised in the event of errorneou data
        assert_raises (MerchantNameNotFoundError, x.lookup_info_by_id, '1234567!@#')

        z = CsvOperations ('test_dir', merch_id='1004')
        for name in z.found_merchant_by_name:
            assert name[3] == 'Susan Vettel'

    def test_upsert_merch_info (self):
        """
        Check if new data is considered for insert or update correctly based on the merchant id
        """
        w = CsvOperations ('test_dir', upsert_merch='Starbuckszzzzz Coffeezzzzz,2005,211-211-2333,David Beckham')
        # That data should be 'updated' as we will get a positive search for the merchant id

        assert w.datadict['5'][3] == 'David Beckham'
        assert not w.datadict['2'][3] == 'David Beckham' 

        # Now for 'insert' tests. Note the change in the merchant id. This should add a new column 
        # in our datastructure. 

        k = CsvOperations ('test_dir', upsert_merch='Starbuckszzzzz Coffeezzzzz,2005123,211-211-2333,David Beckham')
        assert k.datadict['6'][3] == 'David Beckham'
        assert k.datadict['6'][1] == '2005123'


    def test_persist_changes (self):
        """
        Test to check whether the newly updated or inserted data is available in the csv file or not
        """
        u = CsvOperations('test_dir', upsert_merch='Starbucksooo Coffee,2005,211-211-2333,David Beckham', persist=True) # for updatemode
        # Actually, verify data with the data set which is about to be written to a new csv file. Expected to be a dict
        persistence_data = u.persist_data
        for key,value in persistence_data.iteritems():
            if value[1] == '2005':
                assert value[0] == 'Starbucksooo Coffee'
                assert not value[1] == '200555'
        
        v = CsvOperations('test_dir', upsert_merch='Java City Coffee,12005,211-211-2333,Peter Wozniak', persist=True) # for insertmode
        pdata = {}
        for key,value in pdata.iteritems():
            if value[1] == 'i12005':
                assert value[0] == 'Java City Coffee'
                assert not value[1] == '200555'
                assert value[3] == 'Peter Wozniaky'


    def tearDown(self):
        """
        Delete all directories that were used for testing
        """
        if 'dummy_dir' in os.listdir(os.path.abspath(os.getcwd())):
            shutil.rmtree('dummy_dir')
        if 'test_dir'  in os.listdir(os.path.abspath(os.getcwd())):
            shutil.rmtree('test_dir')
        if 'wrong_dir'  in os.listdir(os.path.abspath(os.getcwd())):
            shutil.rmtree('wrong_dir')
