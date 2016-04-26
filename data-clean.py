"""
data-clean.py

Author: Jonathan Whitaker
Email: jon.b.whitaker@gmail.com
Date: April 21, 2016

data-clean.py is an integral part of the AirU toolchain, serving as 
the script which purges residual data that has already been uploaded. 
This script is designed to run using an Anacron task with long period
(every 6 months - 1 year). 
"""
from lib.airu.dbmodels import *

if __name__ == '__main__':
    
    # TODO: Add logging
    
    # Get all samples that have been uploaded and execute a delete query
    query = AirMeasurement.delete().where(AirMeasurement.uploaded == True)
    query.execute()