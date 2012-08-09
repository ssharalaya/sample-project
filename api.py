#######################################################################################################################
# Dummy Disclaimer - Production code
#
# Copyright (c) 2012 
#
# This is company property. So, do not distribute. If you go ahead and distribute, you will NOT get to meet "the most
# interesting man in the world", whose achievements are not limited to :
#
# 1. He once taught a German shepherd to bark in Spanish.
# 2. He is left-handed. And right-handed.
# 3. He Doesn't Always Test His Code, but when He Does, He Does It in Production
# 4. Respected archaeologists fight over his discarded apple cores.
# 5. His organ donation card also lists his beard.

#######################################################################################################################

"""
This module contains the main API requested in the requirements.
"""

import logging
import pdb
import os

from exception_messages import (MerchantNameNotFoundError, MerchantIdNotFoundError, CsvFileNotFoundError,\
                                    CsvFileRelatedError, InvalidRequiredFieldError, NotUniqueError)

class CsvFileReader (object):
    """
    This class handles the reading of the data from the CSV file in to the desired data structure. It
    contains reusable methods for future operations on a csv file. Also, we are assuming that there is
    only one csv file in the chosen directory / filepath.
    """

    def populate_methods (self):

        self.filename = self.check_if_file_exists (self.filepath)

        # Now constucting the full path to tht csv file. Useful for future operations
        if self.filename:
            self.full_filepath = os.path.join(os.path.abspath(self.filepath), self.filename)
        
        # Let us assume that the csv file has no bad data in it, i.e no unicode, no bad formatting etc. Ideally, we
        # should be checking for corrupt data and writing tests for the same. 

        self.read_csv_into_dict (self.full_filepath)
 
    
    def check_if_file_exists (self, name_of_directory):
        """
        Check if there are files in the directory specified.
        @ returns - name of the csv file if found
        """
        if os.path.isdir (name_of_directory):
            csv_file = os.listdir (name_of_directory)
            if csv_file:
                for filename in csv_file:
                    if not filename.endswith('.csv'):
                        msg = 'No csv file found in the directory named "%s"' %(name_of_directory)
                        raise CsvFileNotFoundError, msg
                    else:
                        name_of_csv_file = filename
                        return name_of_csv_file
            else:
                msg = 'No files exist in the directory "%s". Aborting process. ' % name_of_directory
                raise CsvFileNotFoundError, msg
        else:
            msg = 'No such directory "%s" found' % name_of_directory
            raise CsvFileNotFoundError, msg


    def read_csv_into_dict (self, csv_file):
        """
        Read contents of the csv file and arrange data in to Dictionaries, i.e key-value pairs (hashing). Dictionaries
        are chosen as it can be easier to operate on key-value pairs as the data set increases. For example, if we have
        the consider only the first two lines in our csv file, we'd get a data mapping (say 'datadict') like this:

        {'1': [Purple Cow,2001,206-339-8960,Nico Robin],'2': [Panera Bread,1002,(555)232-3422,Mario Andretti]} 

        We can then perform operations like these on datadict:
        datadict['0'][1] = '2001'
        datadict['1'][0] = 'Panera Bread'

        where the first index in the value list (i.e '0') corresponds to 'merchant name', the second index corresponds
         to 'merchant ID' and so on.
        
        """
        csvfile = open(csv_file, 'r')
        self.data_list = []
        csvcontent = csvfile.readlines()
        csvfile.close()

        for csvdata in csvcontent:
            self.data_list.append((csvdata.strip()).split(',')) 

        row_numbering = []

        for row_num in range(len(self.data_list)):
            row_numbering.append(str(row_num+1))

        ldict = zip(row_numbering, self.data_list) # This returns a tuple
        self.datadict = dict(ldict) # Typecasting the tuple in to a dictionary


class CsvOperations (CsvFileReader):
    """
    Child class to add operations on the data set processed in the parent class
    """
    def __init__ (self, directory_path, merch_name=None, merch_id=None, upsert_merch=None, persist=False):
        """
        Assuming the data comes in the following format, each column can be represented as a constant (number). this is for aesthetics only :)

        <merchant name>,<merchant ID>,<phone number>,<merchant contact>
               0               1            2               3

        This init will also initialize methods representing operations of the data set after initializing thr base class itself
        """

        self.filepath = directory_path
        self.populate_methods()
        self.merchant_name = 0
        self.merchant_id = 1
        self.phone_numbr = 2
        self.merchant_contact = 3
        self.listing = []
        self.found_merchant_by_name = []
        self.found_merchant_by_id = []
        self.persist_data = {}

        if merch_name is not None:
            found_merch_name = self.lookup_info_by_name(merch_name)

        if merch_id is not None:
            found_merch_id = self.lookup_info_by_id (merch_id)

        if upsert_merch is not None:
            self.persist_data = self.upsert_merch_info (upsert_merch)
       
        if persist == True:
            self.persist_changes (self.persist_data)

    def lookup_info_by_name (self, merch_name):
        """
        Method to lookup all info using merchant name
        @ merch_name = name of merchant
        @ returns = return the entire row of data for that merchant
        """
        for key,value in self.datadict.iteritems():
            if value[self.merchant_name] == merch_name:
                self.listing.append(key)

        # self.listing will have the key which can be used to refer and print the entire row(s) of data pertaining
        # to that particular merchant. For example, if the key is '2', we can print details of the second merchant.
        
        if len(self.listing) == 0:
             msg = 'Merchant name %s not found in the csv file.' % merch_name
             raise MerchantNameNotFoundError, msg
        else:
             for merchants in self.listing:
                 self.found_merchant_by_name.append(self.datadict[merchants])
        
        for details in self.found_merchant_by_name:
             print details # This returns all details for the chosen row(s) in the csv file  

        return self.found_merchant_by_name


    def lookup_info_by_id (self, merch_id):
        """
        Almost exactly same as the the lookup_info_by_name() method. This method looks up all info using the merchant id
        @ params merch_id = name of merchant
        @ returns = return the entire row of data for that merchant
        """
        for key,value in self.datadict.iteritems():
            if value[self.merchant_id] == merch_id:
                self.listing.append(key)

        # self.listing will have the key which can be used to refer and print the entire row(s) of data pertaining
        # to that particular merchant. For example, if the key is '2', we can print details of the second merchant.

        if len(self.listing) == 0:
             msg = 'Merchant id %s not found in the csv file.' % merch_id
             raise MerchantNameNotFoundError, msg
        else:
             for merchants in self.listing:
                 self.found_merchant_by_name.append(self.datadict[merchants])

        for details in self.found_merchant_by_name:
             print details # This returns all details for the chosen row(s) in the csv file
       
        return self.found_merchant_by_name


    def upsert_merch_info (self, upsert_info):
        """
        This method will determine whether the data has to be updated or inserted. The merchant ID will be used as the 
        tiebreaker to decide whether it is an insert or an update.

        @ params upsert_info - Row of datai (string) to be upserted (upsert is 'update or insert' in short)
        """
        self.upsert_info = upsert_info
        self.save_mode = ''
        
        # Convert the string to a comma separated list
        upsert_list = self.upsert_info.split(',')
        upsert_merch_id = upsert_list[self.merchant_id]
        
        # Now that we have the merch_id, search if record already exists for that merch_id. If there's no data,
        # then we insert. Otherwise, update the datastructure. Reusing the lookup method.
        try: 
            decision = self.lookup_info_by_id (upsert_merch_id)
            self.save_mode = 'UPDATEMODE'
        except MerchantNameNotFoundError:
            self.save_mode = 'INSERTMODE' # which means that we have to insert this data at the end of the csv file

        # If it's an update, then find out the key of the dictionary which holds this upsert_info, so that
        # the key value pair is updated in the dictionary. So,

        if self.save_mode == 'UPDATEMODE':
            if len(self.listing) > 1:
                msg = 'The merchant id %s has yielded more than one match in the csv file. Aborting\n' %upsert_merch_id
                raise NotUniqueError, msg
            else:
                key = self.listing[0]
                self.datadict[key] = upsert_list # Overwrite the data at that particular position
                return self.datadict

        if self.save_mode == 'INSERTMODE':
            key = str(len(self.datadict) + 1) # We are trying to add a new dict at the end of the datastructure
            self.datadict[key] = upsert_list
            return self.datadict
            
    def persist_changes (self, data_to_persist):
        """
        Method to persist changes to the file for both update and insert modes. 
        """
        # Convert data from dict format to list format in preparation for persisting changes
        # i.e convert {'1': ['Purple Cow', '1001', '206-339-8960', 'Nico Robin']} in the dict to
        # something like ['Purple Cow', '1001', '206-339-8960', 'Nico Robin'] so that it easy to write to file
        
        temp_str = ''; iterator = []; dlist = [] 

        for index in range(len(data_to_persist)):
            value = data_to_persist[str(index+1)]
            for iterator in value:
                temp_str += iterator + ',' # string needs to be comma separated
            dlist.append(temp_str[:-1]) # we need to avoid adding  the last trailing comma to the text
            temp_str = ''
        
        try:
            os.remove(self.full_filepath)
        except OSError:
            msg = "Unable to persist changes as csv file cannot be deleted. Aborting"
            raise OSError, msg
        
        full_filename = self.full_filepath
        thefile = open(full_filename, 'wb')
        for stuff in dlist:
            thefile.write("%s\n" % stuff)


if __name__ == '__main__':
    CsvOperations(directory_path= 'dump', merch_name='Purple Cow')
    CsvOperations(directory_path= 'dump', merch_name='Panera Bread') # both Panera Bread  listings are displayed
    CsvOperations('dump', merch_id='1004')
    CsvOperations('dump', upsert_merch='Paneraaaaa Bread,1005,211-211-2333,Steve Wozniak')
    CsvOperations('dump', upsert_merch='Java Coffee,112308,211-211-2333,Billy Wozniak', persist=True)
    CsvOperations('dump', upsert_merch='Java Coffee,112i2308,211-211-2333,Ricardo Wozniak', persist=True)
