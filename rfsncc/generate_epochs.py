import os
import sys
import datetime

def create_needed_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return

def read_csv_from_parameters():
    infile = open(sys.argv[1], 'r')
    path = sys.argv[2]

    create_needed_directory(path)
    # Try to fix the path incase user didn't put the /.
    if not path.endswith("/"):
        path = path + "/"

    path_for_log_file = path + "recordings"
    create_needed_directory(path_for_log_file)
    # Create the atqCmd file that will need to be ran later to schedule the
    # records
    atqCmd = open(path + "atqCmd.sh", "w")
    atqCmd.write("#!/bin/bash\n")

    successfully_written = 0
    for line in infile:
        # Mindless parsing...
        items = line.split(',')
        time = items[0]
        filename_extension = items[1]
        frequency = items[2]
        length_of_epochs = items[3].strip() # Only necessary here beacuse this
        # this item contains a newline as it's the last one on the line

        # This is the filename for this specific shell script.
        filename = "epoch" + filename_extension + ".sh"
        #And this is how we know where to write it to
        filename_with_path = path + filename

        epoch_file = open(filename_with_path, 'w')
        epoch_file.write("#!/bin/bash\n")
        epoch_file.write('echo "' + filename + '" >> ' + path_for_log_file
                + '\n')

        filename_for_specrec = (path + "recordings/epoch" + filename_extension
        + ".sc16")

        write_string = ('specrec --args=master_clock_rate=25e6 --rate=25e6'
        ' --ant=RX2 --time=' + str(length_of_epochs) + ' --freq=' + frequency
        + ' --gain=50 --ref=gpsdo --metadata=true --segsize=24999936 --file='
        + filename_for_specrec + ' --starttime="' + time + '" >> '
        + path_for_log_file + ' 2>&1')

        epoch_file.write(write_string)
        epoch_file.close()

        print("Wrote epoch" + filename_extension + ".sh for starting time "
                + time)

        # Parse the specrec datetime into a datetime object
        twoitems = time.split(' ')
        dateinfo = twoitems[0].split('-')
        timeinfo = twoitems[1].split(':')
        datetime_object = datetime.datetime(int(dateinfo[0]), int(dateinfo[1]),
            int(dateinfo[2]), int(timeinfo[0]), int(timeinfo[1]),
            int(timeinfo[2]))

        # Schedule the epoch about a minute early with put_epoch_in_schedule()
        put_epoch_in_schedule(filename_with_path, datetime_object, atqCmd)

        successfully_written += 1

def main():
    if len(sys.argv) > 1:
        read_csv_from_parameters()
    else:
        # No args run
        display_help()

def display_help():
    print("-------generate_epochs.py Information--------")
    print("Takes a CSV file of start times, filename extensions,"
    + " and frequencies.")
    print("Give it a CSV file path and a path to write files to.")
    print("Generates shell scripts for launching specrec according to CSV file")
    print("")
    print("Needed parameters: [CSV filename] [path to write to]")
    print("Example run: python generate_epochs.py /opt/fall15alcornstate/schedule.csv /opt/fall15alcornstate/")
    print("CSV Format: [specrec time string],[extension to epoch],[frequency],[timeForEpoch]")
    print("For example: [2015-10-15 08:00:00,0,2406] would result in an epoch0.sh file")
    print("that would tell specrec to start recording at 2015-10-15 08:00:00")
    print("at frequency 2406.")
    print("")
    print("Default arguments passed to specrec:")
    print("master_clock_rate = 25e6, rate=25e6, ant=RX2, gain=50, ref=gpsdo")
    print("metadata=true, segsize=24999936")
    print("")
    print("Logs are written to [path to write to]/recordings/logs.txt")

def fix_one_digit(string):
    if len(string) == 1:
        return "0" + string
    return string

def put_epoch_in_schedule(filename, timeobject, atqCmd):
    timeobject = timeobject - datetime.timedelta(seconds=40)

    atq_timedate_string = (fix_one_digit(str(timeobject.hour)) + ":"
            + fix_one_digit(str(timeobject.minute)) + " "
            + fix_one_digit(str(timeobject.month)) + "/"
            + fix_one_digit(str(timeobject.day)) + "/" + str(timeobject.year))

    atqCmd.write('at ' + atq_timedate_string + ' -f ' + filename + '\n')

if __name__ == "__main__":
    main()
