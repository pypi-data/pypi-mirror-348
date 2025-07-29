"""
Import this module to add gmcommon in Python paths
"""

import sys
from os.path import dirname, join, pardir

this_dir = dirname(__file__)
common_dir = join(this_dir, pardir, "libs", "common")
sys.path.append(common_dir)
