#usr/bin/python3
"""
Module math_extra_lib.Tests.UT001_polynomial

Implements demonstration testing of the module math_extra_lib.polynomial, which
are auxilary to the functional unit tests see TE00 and TE001 documents.

Aim is to show the str and repr representation of the objects, and to
demonstrate the exceptions' descriptions.
"""

__version__ = "1.0.0.0"
__date__ = "05-12-2022"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.polynomial as testmodule

#test area

if __name__=='__main__':
    TestObject = testmodule.Polynomial(-2, 1, 0, -3.2, 2.0)