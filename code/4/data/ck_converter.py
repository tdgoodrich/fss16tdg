"""
Takes a csv from the CK datasets in the PROMISE repository
(http://openscience.us/repo/defect/ck/) and converts it to an arff.
Also removes the first three features (dataset name, version number,
and project name)
Also converts the outcome from number of bugs to "Has bugs?" {false, true}.

Usage: $ python data_converter.py [filename].csv
Output: A file named "bool_[filename].arff" in the current directory, for a
dataset [filename].
"""

import sys

def convert_file(filename):
    with open(filename, "r") as infile, open("bool_" + filename.replace(".csv",
      ".arff"), "w") as outfile:

        # Write arff header
        outfile.write("@RELATION " + filename + "\n\n")
        header = infile.readline().split(",")
        for attribute in header[3:-1]:
            outfile.write("@attribute %s numeric\n" % attribute)
        outfile.write("@attribute %s {false,true}\n\n" % \
          header[-1].replace("\r\n", ""))
        outfile.write("@DATA\n")

        # Write the data
        for line in infile.readlines():
            row = line.split(",")[3:]
            row[-1] = str(int(row[-1]) > 0).lower() + "\n"
            outfile.write(",".join(row))

if __name__ == "__main__":
    convert_file(sys.argv[1])
