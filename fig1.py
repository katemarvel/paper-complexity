#!/usr/bin/python
#
# Script to make Fig. ED4 of the proces paper
# intended to highlight the absence of link
# between model physics and process strength
#
# Author: F. Massonnet, September 2017
#         francois.massonnet@uclouvain.be

# Load standard modules, fonts, etc.
execfile("./config.py") 


# Start the script
diag = "siextent" # siextent, sivol or siarea
domain = "Antarctic" # Domain under consideration 
dirin = "./netcdfs/"   # where the pre-processed NetCDF data of volume and area are

month = 9 # Month to plot (Standard convention): September = 9

colors_complexity = [[1.0, 0.0, 0.0], [1.0, 0.5, 0.0], [1.0, 1.0, 0.0], [0.0, 0.8, 0.0]]  # For plotting model complexity as color
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
# Read CMIP5 namelist (in another file since this namelist is used by different scripts)
execfile("./cmip5_namelist.py")

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
    
    data[j_models].append([complexity, mean, trend])


# Graphs
fig = plt.figure("fig", figsize = (5, 7))

# 1. MEAN STATE
plt.subplot(2, 1, 1)
# List of pairs "complexity, value"
tmp = [[y[0], y[1]] for x in data for y in x]
# Sort by ascending value
tmp.sort(key = lambda x : x[1])

has_plotted_legend = [False, False, False, False]
for j in range(len(tmp)):
    if has_plotted_legend[tmp[j][0] - 1]:
        label = None
    else:
        label = complexity_names[tmp[j][0] - 1]
        has_plotted_legend[tmp[j][0] - 1] = True
        
    plt.fill((j, j + 1, j + 1, j), (0.0, 0.0, tmp[j][1], tmp[j][1]), 
         facecolor = colors_complexity[tmp[j][0] - 1],
         edgecolor = None,
         alpha = 0.5, label = label)

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
for j in range(len(tmp)):
    if has_plotted_legend[tmp[j][0] - 1]:
        label = None
    else:
        label = complexity_names[tmp[j][0] - 1]
        has_plotted_legend[tmp[j][0] - 1] = True
        
    plt.fill((j, j + 1, j + 1, j), (0.0, 0.0, tmp[j][1], tmp[j][1]), 
         facecolor = colors_complexity[tmp[j][0] - 1],
         edgecolor = None,
         alpha = 0.5, label = label)
    
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
