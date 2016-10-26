"""
Takes the Semeion handwritten digit data
(https://archive.ics.uci.edu/ml/datasets/Semeion+Handwritten+Digit)
and converts it to an arff of our format

Usage: $ python digit_converter.py
Output: A file named "digit.arff" in the current directory.
"""

import sys

wine_names = ["", "wine1", "wine2", "wine3"]

def convert_file(filename):
    with open(filename, "r") as infile, open("wine.arff", "w") as outfile:

        # Write arff header
        outfile.write("@RELATION " + filename + "\n\n")
        for i in xrange(13):
            outfile.write("@attribute ignore%d numeric \n" % i)
        outfile.write("@attribute wine {")
        for i in xrange(1, len(wine_names)):
            outfile.write(wine_names[i] + ", ")
        outfile.write(wine_names[-1] + "}\n\n")
        outfile.write("@DATA\n")

        # Write the data
        for line in infile.readlines():
            row = line.replace("\n", "").split(",")
            features, outcomes = row[1:], row[:1]
            outcomes = [wine_names[int(x)] for x in outcomes]
            row = features + outcomes
            outfile.write(",".join(row) + "\n")

if __name__ == "__main__":
    convert_file(filename="wine.data")
