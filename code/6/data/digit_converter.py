"""
Takes the Semeion handwritten digit data
(https://archive.ics.uci.edu/ml/datasets/Semeion+Handwritten+Digit)
and converts it to an arff of our format

Usage: $ python digit_converter.py
Output: A file named "digit.arff" in the current directory.
"""

import sys

digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven",
               "eight", "nine"]

def convert_file(filename):
    with open(filename, "r") as infile, open("digits.arff", "w") as outfile:

        # Write arff header
        outfile.write("@RELATION " + filename + "\n\n")
        for i in xrange(256):
            outfile.write("@attribute pixel%d boolean\n" % i)
        outfile.write("@attribute digit {")
        for i in xrange(9):
            outfile.write(digit_names[i] + ", ")
        outfile.write(digit_names[9] + "}\n\n")
        outfile.write("@DATA\n")

        # Write the data
        for line in infile.readlines():
            row = line.replace("1.0000", "TRUE").replace("0.0000", "FALSE").split()
            features, outcome = row[:256], row[256:]
            outcome = [digit_names[x] for x in xrange(len(outcome)) if outcome[x] == "1"]
            row = features + outcome
            outfile.write(",".join(row) + "\n")

if __name__ == "__main__":
    convert_file("semeion.data")
