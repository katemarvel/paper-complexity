#!/usr/bin/python
#
# Script for the BAMS paper on model complexity 
# (Notz, Hunke, Massonnet, Vancoppenolle)

# Author: F. Massonnet, Jan 2019 - April 2019
# francois.massonnet@uclouvain.be

# Load standard modules, fonts, etc.
import sys

# Python 2 or 3 call to config and namelist files
if sys.version_info.major == 3:
    # Read configuration file (fonts, imports, etc.)
    exec(open("./config.py").read())
    # Read CMIP5 namelist (in another file since this namelist is used by different scripts)
    exec(open("./cmip5_namelist.py").read())
else:
    # Read configuration file (fonts, imports, etc.)
    execfile("./config.py")
    # Read CMIP5 namelist (in another file since this namelist is used by different scripts)
    execfile("./cmip5_namelist.py")


# Start the script
diag = "sivol" # siextent, sivol or siarea
domain = "Arctic" # Domain under consideration 
dirin = "./netcdfs/"   # where the pre-processed NetCDF data of volume and area are

month = 3 # Month to plot (Standard convention): September = 9

colors_complexity = ["#c7e9c0", "#74c476", "#31a354", [0.0, 0.2, 0.08]]  # For plotting model complexity as color
complexity_names  = ["Very simple", "Simple", "Intermediate", "Complex"]
# Start the script
# ----------------

if diag == "siextent":
    units = "10$^6$ km$^2$"
    diag_name = domain + " sea ice extent"
elif diag == "siarea":
    units = "10$^6$ km$^2$"
    diag_name = domain + " sea ice area"
elif diag == "sivol":
    units = "10$^3$ km$^3$"
    diag_name = domain + " sea ice volume"
else:
    sys.exit("Diag unknown")

month_name = datetime.date(2000, month, 1).strftime('%B')

# Load and analyse CMIP5 data
# ------------------------------------
# Years defining the period to showcase (must be within the availability of data)
yearb = 1979
yeare = 2004

years = np.arange(yearb, yeare + 1)

n_models = len(info)
n_years = yeare - yearb + 1

# Load the data and compute the diagnostics
data = list() # Will contain as many items as there are models
              # Each item will contain as many sub-items as there are members
              
nt = (yeare - yearb) * 12 + 1 # Number of time steps (months) in the analysis

for j_models in range(n_models):
  # 1. Get information about the model
  model = info[j_models][0]
  # Start and End years of that model
  yb    = info[j_models][5]
  ye    = info[j_models][6]

  complexity = info[j_models][9]
  # List of ensemble members
  members = info[j_models][7]
  n_members = len(members)

  print("Loading " + model + "(" + str(n_members) + " members)")

  data.append(list()) # One per member
  for j_members in range(n_members):
    # 2. Read volume, area and temperature
    filein = dirin + "/seaice_" + model + "_historical_r" + \
           str(members[j_members]) + "i1p1_" + str(yb) +  \
           "01-" + str(ye) + "12.nc"
           
    f = Dataset(filein, mode = "r")
    series = f.variables[diag + "_"  + domain][(yearb - yb)   * 12:(yeare - yb) * 12 + 12]
    f.close()

    # Mean state
    mean = np.mean(series[month::12])

    # Trend
    trend = np.polyfit(years, series[month::12], 1)[0] * 10.0 # per decade
    
    data[j_models].append([complexity, mean, trend, series])

# Series
tmp = [[y[0], y[3]] for x in data for y in x]    
has_plotted_legend = [False, False, False, False]
order = 1
fig = plt.figure("series")
counter=0
for d in data:
    for m in d:
        series = m[3][month::12]
        color = colors_complexity[m[0] - 1]
   
        plt.plot(years, series, color = color, alpha = 0.8)
        
plt.ylabel(units)
plt.title(month_name + " " + diag_name)
plt.grid()
plt.gca().set_axisbelow(True)
plt.legend()
plt.tight_layout()
plt.savefig("./" + diag + "-" + domain + "-" + month_name + "-" + str(yearb) + "-" + str(yeare) + ".png", dpi = 500)
plt.savefig("./" + diag + "-" + domain + "-" + month_name + "-" + str(yearb) + "-" + str(yeare) + ".pdf"           )



# 1. MEAN STATE
fig = plt.figure("fig", figsize = (5, 7))
plt.subplot(2, 1, 1)
# List of pairs "complexity, value"
tmp = [[y[0], y[1]] for x in data for y in x]
# Sort by ascending value
tmp.sort(key = lambda x : x[1])

has_plotted_legend = [False, False, False, False]
order = 1 # To freeze the order of legend
for j in range(len(tmp)):
    if not has_plotted_legend[tmp[j][0] - 1] and  tmp[j][0] == order:
        label = complexity_names[tmp[j][0] - 1]
        has_plotted_legend[tmp[j][0] - 1] = True
        order += 1
    else:
        label = None
        
    plt.fill((j, j + 1, j + 1, j), (0.0, 0.0, tmp[j][1], tmp[j][1]), 
         facecolor = colors_complexity[tmp[j][0] - 1],
         edgecolor = None,
         alpha = 0.8, label = label)

plt.title(str(yearb) + "-" + str(yeare) + " mean " + month_name + "\n" + diag_name)
plt.ylabel(units)
plt.grid()
plt.gca().set_axisbelow(True)
plt.legend()
plt.gca().xaxis.grid(False)
plt.tight_layout()

# 2. TREND
plt.subplot(2, 1, 2)
# List of pairs "complexity, value"
tmp = [[y[0], y[2]] for x in data for y in x]
# Sort by ascending value
tmp.sort(key = lambda x : x[1])

has_plotted_legend = [False, False, False, False]
order = 1
for j in range(len(tmp)):
    if not has_plotted_legend[tmp[j][0] - 1] and  tmp[j][0] == order:
        label = complexity_names[tmp[j][0] - 1]
        has_plotted_legend[tmp[j][0] - 1] = True
        order += 1
    else:
        label = None

        
    plt.fill((j, j + 1, j + 1, j), (0.0, 0.0, tmp[j][1], tmp[j][1]), 
         facecolor = colors_complexity[tmp[j][0] - 1],
         edgecolor = None,
         alpha = 0.8, label = label)
    
plt.title(str(yearb) + "-" + str(yeare) + " trend " + month_name + "\n" + diag_name)
plt.xlabel("CMIP5 ensemble member #")
plt.ylabel(units + "/ decade")
plt.grid()
plt.gca().set_axisbelow(True)
plt.gca().xaxis.grid(False)
plt.legend()
plt.tight_layout()


plt.savefig("./" + domain + "-" + month_name + "-" + diag + "-" + str(yearb) + "-" + str(yeare) + ".png", dpi = 500)
plt.savefig("./" + domain + "-" + month_name + "-" + diag + "-" + str(yearb) + "-" + str(yeare) + ".pdf")



