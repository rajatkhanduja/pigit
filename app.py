#!/usr/bin/env python

from pigit import PigitCommandWrapper, PigitException
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


try:
    pigit = PigitCommandWrapper(os.curdir)
    pigit.execute_command(sys.argv[1:])
except PigitException as e:
    print(e.message)