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
Module listing simple reusable exception classes

"""

import pdb
import exceptions

class MerchantNameNotFoundError (LookupError):
    """
    Custom exception when there is no merchant name in the datastructure
    """
    pass

class MerchantIdNotFoundError (LookupError):
    """
    Custom exception when there is no merchant ID in the datastructure
    """
    pass

class CsvFileNotFoundError (OSError):
    """
    Custom exception when there is no csv file in the directory specified
    """
    pass

class CsvFileRelatedError (OSError):
    """
    Custom exception for all other csv file related error
    """
    pass

class InvalidRequiredFieldError (ValueError):
    """
    Custom exception for invalid data found for required fields
    """
    pass

class NotUniqueError (LookupError):
    """
    Custom exception for indicating non-unique data
    """
    pass
