import sys
import re
import os
import glob
GAINKEY = "--gain="
EXITCODE = -392
def print_help():
    print("-----------update_gains.py-------------")
    print("   - Looks for epoch*.sh files and changes the gain value within.")
    print("   - Give a parameter of '--gain=##' to specify the new gain.")
    print("---------------------------------------")

def process_parameters():
    try:
        first_parameter = sys.argv[1]   
        if GAINKEY in first_parameter:
            split_parameter = first_parameter.split('=')    
            should_be_gain = split_parameter[1]
            if should_be_gain.isdigit():
                return int(should_be_gain)
            else:
                return EXITCODE 
        # If we've made it this far without returning or exiting
        # The gain parameter doesn't fit the format asked for.
        return EXITCODE

    except: # No parameters were given
        return EXITCODE

def process_files(list_of_files, new_gain):
    try:
        print("-------------------------")
        print("-----files processed-----")
        print("-------------------------")
        for filename in list_of_files:
            print(filename)
            in_file = open(filename, 'r')
            launch_script = in_file.read()

            out_file = open(filename + ".tmp", 'w')
            out_file.write(re.sub(r'--gain=\d+\b', "--gain=" + str(new_gain), launch_script))

            out_file.close()
            in_file.close()

            os.remove(filename)
            os.rename(filename + ".tmp", filename)

        print("--------------------------")
        print("Files Edited: " + str(len(list_of_files)))
        print("New Gain: " + str(new_gain))
        print("--------------------------")

    except IOError as e:
        print(e)
        print("Error during file reading/writing.")

def main():
    new_gain = process_parameters()
    if new_gain == EXITCODE:
        print_help()
        return
    else: 
        list_of_files = glob.glob("epoch*.sh")
        if len(list_of_files) == 0:
            print("No epoch*.sh files found in this folder.")
        else:
            process_files(list_of_files, new_gain)

main()
