# Set of modules to be systematically imported
# for all Python scripts

# ---------------------------------------
# Headers, modules imported, etc.
# ---------------------------------------
# Regular Python modules
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib
matplotlib.use('Agg') # avoids tKinter error
import matplotlib.dates as mdates

import numpy as np
import sys
import datetime

from netCDF4 import Dataset
from matplotlib.gridspec import GridSpec

import os

# Change font globally
# --------------------
font_dirs  = [u'./fonts/', ]
font_files = font_manager.findSystemFonts(fontpaths = font_dirs)
font_list  = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
matplotlib.rcParams['font.family'] = 'Acephimere'

plt.close("all")                   # Close all figures

