import sys,os

def recording_information():
    filename_extension_list = []
    sample_rate_list = []
    duration_list = []
    csv = open(sys.argv[1])
    lines = csv.readlines()
    for line in lines:
        items = line.split(" ", ",")
        sample_rate_list.append(items[3])
        duration_list.append(items[4])
        filename_extension_list.append(items[2])
    return sample_rate_list, duration_list, filename_extension_list


def epoch_path(filename_extension_list):
    epoch_path_list = []
    for i in filename_extension_list:
        epochPath = "~node_infrastructure-operations/rfsncc/recordings/"+ i + ".sc16"
        epoch_path_list.append(epochPath)
    return epoch_path_list


def actual_size(epoch_path_list):
    size_list = []
    for i in epoch_path_list:
        size = os.path.getsize(i)
        size_list.append(size)
    return size_list

def expected_size(duration_list, sample_rate_list):
    expected_size_list = []
    for i in range(len(duration_list)):
        expectedSize = 4 * duration_list[i] * sample_rate_list[i]
        expected_size_list.append(expectedSize)
    return expected_size_list

def compare_size(size_list, expected_size_list):
    for i in range(len(size_list)):
        if (abs(size_list[i] - expected_size_list[i]) < 50000):
            print(filename_extension_list + " is a valid recording")
        else:
            print(filename_extension_list + "is not a valid recording")

def main():
    sampleRate, duration, filenameExtension = recording_information()
    epochPath = epoch_path(filenameExtension)
    actualSize = actual_size(epochPath)
    expectedSize = expected_size(duration, sampleRate)
    compare_size(actualSize, expectedSize)

if __name__ == "__main__":
    main()
    
    
    
        
        
