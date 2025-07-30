# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                               Displam                          #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Command line interface for Displam as a standalone python package.
 
@note: Displam
Created on 05.12.2023

@version: 1.0
----------------------------------------------------------------------------------------------
@requires:
       - 

@change: 
       -    
                           
@author: garb_ma                                                     [DLR-FA,STM Braunschweig]
----------------------------------------------------------------------------------------------
"""

## @package Displam
# Command line interface for Displam as a standalone python package.
## @authors 
# Jens Baaran,
# Marc Garbade
## @date
# 05.12.2023
## @par Notes/Changes
# - Added documentation // mg 05.12.2023

import os,sys,subprocess

## Add additional path to environment variable
if os.path.exists(os.path.join(sys.prefix,"conda-meta")):
    os.environ["PATH"] = os.pathsep.join([os.path.join(sys.prefix,"Library","bin"),os.getenv("PATH","")])

def main():
    """
    Run DaMapper from a python console.
    """
    subprocess.call([os.path.join(os.path.dirname(os.path.abspath(__file__)),"bin","displam")] + sys.argv[1:])

if __name__ == '__main__':
    main(); sys.exit()
    pass