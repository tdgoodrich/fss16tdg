"""
Converts a bug count outcome to a boolean "Has bugs?" outcome.
Assumes a csv input.
Tested with files from the CK dataset in the PROMISE repository.
Usage: $ python data_converter.py [filename]
Output: A file named "boolean_[filename]" in the current directory, for a dataset [filename]   
"""

import sys

def convert_file(filename):
    with open(filename, "r") as infile, open("boolean_" + filename, "w") as outfile:
            outfile.write(infile.readline())
            for line in infile.readlines():
                split_line = line.split(",")
                split_line[-1] = str(int(split_line[-1]) > 0) + "\n"
                outfile.write(",".join(split_line))

if __name__ == "__main__":
    convert_file(sys.argv[1])
