#!/usr/bin/python3 

import logging
import sys
import os



logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/APC/')


from run import app as application

