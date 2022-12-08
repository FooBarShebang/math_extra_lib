#usr/bin/python3
"""
Module math_extra_lib.Tests.DT002_special_functions

Implements demonstration testing of the module math_extra_lib.special_functions
- specifically the exceptions generation, which are auxilary to the functional
unit tests see TE00 and TE002 documents.
"""

__version__ = "1.0.0.0"
__date__ = "08-12-2022"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.special_functions as testmodule

#helper functions

def PrintError(Error: Exception) -> None:
    print(Error.__class__.__name__, ':', Error)
    print(Error.Traceback.Info)

#test area

if __name__=='__main__':
    try:
        testmodule.permutation(-1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.permutation(10, 2.0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta(-1, 2.0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta(1, '2.0')
    except Exception as err:
        PrintError(err)
    input('Press Enter')