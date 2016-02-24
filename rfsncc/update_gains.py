import sys
import re
import os
import glob
GAINKEY = "--gain="
PATHKEY = "--path="
EXITCODE = -392

def print_help():
    print("-----------update_gains.py-------------")
    print("   - Looks for epoch*.sh files and changes the gain value within.")
    print("   - Give a parameter of '--gain=##' to specify the new gain.")
    print("   - Parameter '--path=/AAA/BBB/' to specify absolute path.")
    print("---------------------------------------")

def process_parameters():
    gain=EXITCODE
    path=""
    try:
        for parameter in sys.argv:
            if GAINKEY in parameter:
                should_be_gain = parameter.split('=')[1]
                if should_be_gain.isdigit():
                    gain = int(should_be_gain)
                else:
                    return EXITCODE 
            if PATHKEY in parameter:
                should_be_path = parameter.split('=')[1]
                if is_valid_path(should_be_path):
                    path = should_be_path
                else:
                    return EXITCODE
    except:
        return EXITCODE
    return (gain, path)

def is_valid_path(string):
    return string.startswith('/') and string.endswith('/')

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
            out_file.write(re.sub(r'--gain=\d+\b', "--gain="
                + str(new_gain), launch_script))

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
    gain, path = process_parameters()
    if gain == EXITCODE:
        print_help()
        return
    list_of_files = glob.glob(path + "epoch*.sh")
    if len(list_of_files) == 0:
        if path == "":
            print("No epoch*.sh files found in current folder.")
        else:
            print("No epoch*.sh files found in " + path)
        return
    process_files(list_of_files, gain)
    

#Modularization??
if __name__ == "__main__":
    sys.argv[0]

main()
