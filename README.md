sample-project
==============

This is a sample project that I started recently. Just wanted to play around a bit and practice some Python :)

PROJECT STATEMENT
__________________

To write a small API that can be used to look up information about merchants in a directory that is stored as a
csv file. The comma separated values are:

<merchant name>,<merchant ID>,<phone number>,<merchant contact>

An example CSV file (in a simple directory) would look like this:

Purple Cow,2001,206-339-8960,Nico Robin
Panera Bread,1002,(555)232-3422,Mario Andretti
Panchos Tacos,2003,343 222 3322 ext. 342,Michael Johnson
Curry Pot,1004,+44 232 3222 3322,Susan Vettel
Panera Bread,2005,211-211-2333,David Beckham


Panera Bread (second line) and Panera Bread (last line) are not the same merchants.

The aim is to write a library that will enable the following operations:
* Do a look up of all of any merchant's information by name.
* Do a look up of all of any merchant's information by ID.
* Add the information of a merchant
* Update the information of a merchant
* Persist changes back to the csv file


HOW TO RUN THE SCRIPT (API)
____________________________

* Clone this repository
* Assuming python is already installed run 'python api.py'
* Here are a few ways one can invoke the API in the api.py file

    CsvOperations(directory_path= 'dump', merch_name='Purple Cow')

    CsvOperations(directory_path= 'dump', merch_name='Panera Bread') # both Panera Bread listings are displayed

    CsvOperations('dump', merch_id='1004')

    CsvOperations('dump', upsert_merch='Paneraaaaa Bread,1005,211-211-2333,Steve Wozniak')

    CsvOperations('dump', upsert_merch='Java Coffee,112308,211-211-2333, Billy Wozniak', persist=True)

    CsvOperations('dump', upsert_merch='Java Coffee,112i2308,211-211-2333, Ricardo Wozniak', persist=True)

