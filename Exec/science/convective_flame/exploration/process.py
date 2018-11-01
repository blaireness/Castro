# After running the problem code in each directory, this code loops over the 
# resulting plotfiles and generates .png images of the plots at specific times.
# 
# The code also reads in a html template file and writes the html for a webpage
# displaying the high, reference, and low plots side by side to be compared
# qualitatively.
#
# The latest version of the webpage generated by this code can be found at:
#    http://bender.astro.sunysb.edu/blaire/
#
# Written by Blaire Ness and Michael Zingale
#
# Last updated 9/24/18

from __future__ import print_function

import os
import shlex
import subprocess

# read in html template
html_template = "index_temp.html"

# define function for writing the html
def write_html(file_names, target_dir, var_name):
    # read in index.html
    html_mod = open("{}/index{}.html".format(target_dir, var_name), "w")
    for line in html_lines:
        for key in file_names:
            line = line.replace("@@{}@@".format(key), ".{}".format(file_names[key]))
        html_mod.write(line)
    html_mod.close()

# open the html template
with open(html_template, "r") as html_temp:
    html_lines = html_temp.readlines()

# define plotfile class
class PlotFile:
    def __init__(self, run, value, plotfile, full_path=""):
        self.run = run                 # variable being altered
        self.value = value             # low, high
        self.plotfile = plotfile
        self.full_path = full_path     # path to file
        self.find_time = -1            # time of file

# define function for running shell commands
def run(string):

    # shlex.split will preserve inner quotes
    prog = shlex.split(string)
    p0 = subprocess.Popen(prog, stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)

    stdout0, stderr0 = p0.communicate()
    rc = p0.returncode
    p0.stdout.close()
    p0.stderr.close()

    return stdout0, stderr0, rc

# define function for finding the time value of a plotfile
def find_time(pf):
    stdout, _, _ = run("ftime.Linux.gfortran.exe {}".format(pf))
    return float(stdout.split()[-1])

# this is the heart of the code: here we loop over the directories,
# generate the .png images, and add them to the html
def process(top_dir=".", prefix="plt"):

    # find directories with runs

    current_run = None
    current_value = None

    all_plot_files = []

    # loop through directories looking for plotfiles
    for root, dirs, files in os.walk(top_dir):
        for d in dirs:
            if prefix in d:
                path = root.split("/")
                if path[-1] == "reference":
                    current_run = "reference"
                    current_value = None
                else:
                    if path[-1] == "low":
                        current_value = "low"
                        current_run = path[-2]
                    elif path[-1] == "high":
                        current_value = "high"
                        current_run = path[-2]
                                
                all_plot_files.append(PlotFile(current_run, current_value, d, full_path=os.path.join(root, d)))

    # find all the unique runs
    runs = set([pf.run for pf in all_plot_files])    
    print('runs = ', runs)

    # find files and their output times
    for pf in all_plot_files:
        if pf.run == "PERT_WIDTH": continue
        if pf.run == "PERT_FACTOR": continue
        pf.time = find_time(pf.full_path)
        
    print("times found")

    ref = [pf for pf in all_plot_files if pf.run == "reference"]

    # loop over runs and write html
    top_dir = os.getcwd()

    # process reference here
    for pf in ref:
        temp_command = "plotsinglevar.py -m 0.0 -M 50.0 %s Temp" % pf.full_path
        omega_ash_command = "plotsinglevar.py %s omegadot_ash" % pf.full_path
        omega_fuel_command = "plotsinglevar.py %s omegadot_fuel" % pf.full_path
        if (pf.time == 0.0):
            run(temp_command)
            run(omega_ash_command)
            run(omega_fuel_command)
            ref1_temp = "%s_Temp.png" % pf.full_path
            ref1_ash = "%s_omegadot_ash.png" % pf.full_path
            ref1_fuel = "%s_omegadot_fuel.png" % pf.full_path
        elif (0.000095 < pf.time < 0.000105):
            run(temp_command)
            run(omega_ash_command)
            run(omega_fuel_command)
            ref2_temp = "%s_Temp.png" % pf.full_path
            ref2_ash = "%s_omegadot_ash.png" % pf.full_path
            ref2_fuel = "%s_omegadot_fuel.png" % pf.full_path
        elif (0.000195 < pf.time < 0.000205):
            run(temp_command)
            run(omega_ash_command)
            run(omega_fuel_command)
            ref3_temp = "%s_Temp.png" % pf.full_path
            ref3_ash = "%s_omegadot_ash.png" % pf.full_path
            ref3_fuel = "%s_omegadot_fuel.png" % pf.full_path
        elif (0.000295 < pf.time < 0.000305):
            run(temp_command)
            run(omega_ash_command)
            run(omega_fuel_command)
            ref4_temp = "%s_Temp.png" % pf.full_path
            ref4_ash = "%s_omegadot_ash.png" % pf.full_path
            ref4_fuel = "%s_omegadot_fuel.png" % pf.full_path

    # assign .png images to placeholder keywords in html template
    ref_files_temp = {"row1column2":ref1_temp,
                      "row2column2":ref2_temp,
                      "row3column2":ref3_temp,
                      "row4column2":ref4_temp}
    ref_files_ash = {"row1column2":ref1_ash,
                      "row2column2":ref2_ash,
                      "row3column2":ref3_ash,
                      "row4column2":ref4_ash}
    ref_files_fuel = {"row1column2":ref1_fuel,
                      "row2column2":ref2_fuel,
                      "row3column2":ref3_fuel,
                      "row4column2":ref4_fuel}

    # loop over the different runs other than reference
    for r in runs:
        
        # find "low" and "high" files for this run
        low = [pf for pf in all_plot_files if pf.run == r and pf.value == "low"]
    
        for pf in low:
            temp_command = "plotsinglevar.py -m 0.0 -M 50.0 %s Temp" % pf.full_path
            ash_command = "plotsinglevar.py %s omegadot_ash" % pf.full_path
            fuel_command = "plotsinglevar.py %s omegadot_fuel" % pf.full_path
            if (pf.time == 0.0):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                low1_temp = "%s_Temp.png" % pf.full_path
                low1_ash = "%s_omegadot_ash.png" % pf.full_path
                low1_fuel = "%s_omegadot_fuel.png" % pf.full_path
            elif (0.000095 < pf.time < 0.000105):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                low2_temp = "%s_Temp.png" % pf.full_path
                low2_ash = "%s_omegadot_ash.png" % pf.full_path
                low2_fuel = "%s_omegadot_fuel.png" % pf.full_path
            elif (0.000195 < pf.time < 0.000205):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                low3_temp = "%s_Temp.png" % pf.full_path
                low3_ash = "%s_omegadot_ash.png" % pf.full_path
                low3_fuel = "%s_omegadot_fuel.png" % pf.full_path
            elif (0.000295 < pf.time < 0.000305):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                low4_temp = "%s_Temp.png" % pf.full_path
                low4_ash = "%s_omegadot_ash.png" % pf.full_path
                low4_fuel = "%s_omegadot_fuel.png" % pf.full_path
        low_files_temp = {"row1column3":low1_temp,
                          "row2column3":low2_temp,
                          "row3column3":low3_temp,
                          "row4column3":low4_temp}
        low_files_ash = {"row1column3":low1_ash,
                         "row2column3":low2_ash,
                         "row3column3":low3_ash,
                         "row4column3":low4_ash}
        low_files_fuel = {"row1column3":low1_fuel,
                          "row2column3":low2_fuel,
                          "row3column3":low3_fuel,
                          "row4column3":low4_fuel}

        high = [pf for pf in all_plot_files if pf.run == r and pf.value == "high"]

        for pf in high:
            temp_command = "plotsinglevar.py -m 0.0 -M 50.0 %s Temp" % pf.full_path
            ash_command = "plotsinglevar.py %s omegadot_ash" % pf.full_path
            fuel_command = "plotsinglevar.py %s omegadot_fuel" % pf.full_path
            if (pf.time == 0.0):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                high1_temp = "%s_Temp.png" % pf.full_path
                high1_ash = "%s_omegadot_ash.png" % pf.full_path
                high1_fuel = "%s_omegadot_fuel.png" % pf.full_path
            elif (0.000095 < pf.time < 0.000105):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                high2_temp = "%s_Temp.png" % pf.full_path
                high2_ash = "%s_omegadot_ash.png" % pf.full_path
                high2_fuel = "%s_omegadot_fuel.png" % pf.full_path
            elif (0.000195 < pf.time < 0.000205):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                high3_temp = "%s_Temp.png" % pf.full_path
                high3_ash = "%s_omegadot_ash.png" % pf.full_path
                high3_fuel = "%s_omegadot_fuel.png" % pf.full_path
            elif (0.000295 < pf.time < 0.000305):
                run(temp_command)
                run(ash_command)
                run(fuel_command)
                high4_temp = "%s_Temp.png" % pf.full_path
                high4_ash = "%s_omegadot_ash.png" % pf.full_path
                high4_fuel = "%s_omegadot_fuel.png" % pf.full_path                
        print("current_run = ", r)
        high_files_temp = {"row1column1":high1_temp,
                           "row2column1":high2_temp,
                           "row3column1":high3_temp,
                           "row4column1":high4_temp}
        high_files_fuel = {"row1column1":high1_fuel,
                           "row2column1":high2_fuel,
                           "row3column1":high3_fuel,
                           "row4column1":high4_fuel}
        high_files_ash = {"row1column1":high1_ash,
                          "row2column1":high2_ash,
                          "row3column1":high3_ash,
                          "row4column1":high4_ash}
        file_names_temp = ref_files_temp.copy()
        file_names_temp.update(high_files_temp)
        file_names_temp.update(low_files_temp)

        file_names_fuel = ref_files_fuel.copy()
        file_names_fuel.update(high_files_fuel)
        file_names_fuel.update(low_files_fuel)

        file_names_ash = ref_files_ash.copy()
        file_names_ash.update(high_files_ash)
        file_names_ash.update(low_files_ash)

        print(r, file_names_temp, file_names_fuel, file_names_ash)
        write_html(file_names_temp, r, "temperature")
        write_html(file_names_fuel, r, "fuel")
        write_html(file_names_ash, r, "ash")

if __name__ == "__main__":
    process()

print("FINISHED")
