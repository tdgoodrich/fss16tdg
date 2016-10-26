"""
Table.py : A table class for reading in datasets (CSV and arff supported).
Limitations and assumptions:
- Assumes that the last column from input is the outcome, and the rest are features. To change this, we'd need to update the input readers; internally, features and outcomes are separated.
- Currently assumes a complete dataset (i.e. no missing values). If this needs
  to change then the distance methods need to be updated.
- Assumes that the dataset file comes with an appropriate header:
  CSV : top row
  arff: @attribute labels
"""

import argparse, itertools, math, re, sys

# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw2.md
# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw3.md
class Num:
    def __init__(self, first_item, col_name):
        self.mu = 0
        self.n = 0
        self.m2 = 0
        self.up = float("-inf")
        self.lo = float("inf")
        self.name = col_name
        self.add(first_item)
        self.type="Num"

    def add(self,x):
        self.n += 1
        x = float(x)
        if x > self.up: self.up=x
        if x < self.lo: self.lo=x
        delta = x - self.mu
        self.mu += delta/self.n
        self.m2 += delta*(x - self.mu)
        return x

    def subtract(self,x):
        self.n   = max(0,self.n - 1)
        delta = x - self.mu
        self.mu  = max(0,self.mu - delta/self.n)
        self.m2  = max(0,self.m2 - delta*(x - self.mu))

    def standard_deviation(self):
        return 0 if self.n <= 2 else (self.m2/(self.n - 1))**0.5

    def show(self):
        return "type: numeric, mean: %f, standard deviation: %f" % (self.mu,
          self.standard_deviation())

    def norm(self, x):
        tmp= (x - self.lo) / (self.up - self.lo + sys.float_info.epsilon)
        if tmp > 1: return 1
        elif tmp < 0: return 0
        else: return tmp

    def distance(self, x, y):
        return self.norm(x) - self.norm(y)

    def furthest(self, x) :
        return self.up if x < (self.up-self.lo)/2 else self.lo

# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw2.md
# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw3.md
class Sym:
    def __init__(self, first_item, col_name):
        self.counts = {}
        self.most = 0
        self.mode = None
        self.n = 0
        self.name = col_name
        self.add(first_item)
        self.type="Sym"

    def add(self,x):
        self.n += 1
        new = self.counts[x] = self.counts.get(x,0) + 1
        if new > self.most:
            self.most, self.mode = new,x
        return x

    def subtract(self,x):
        self.n -= 1
        self.counts[x] -= 1
        if x == self.mode:
            self.most, self.mode = None,None

    def entropy(self):
        tmp = 0
        for val in self.counts.values():
            p = float(val)/self.n
            if p:
                tmp -= p*math.log(p,2)
        return tmp

    def show(self):
        return "type: symbolic, mode: %s, entropy: %f" % (self.mode,
          self.entropy())

    def norm(self, x):
        return x

    def distance(self, x, y):
        return 0 if x==y else 1

    def furthest(self, x):
        return None

class Row:
    def __init__(self, features, outcomes):
        self.features = features
        self.outcomes = outcomes

    def __iter__(self):
        for item in self.features:
            yield item
        for item in self.outcomes:
            yield item

class Table:
    # Constructor
    def __init__(self, filename=None):
        """
        Initialize the Table object with
        - rows: The rows of data
        - cols: Some statistics we keep for each column
        """
        self.rows = []
        self.cols = None
        if filename != None:
            if filename.split(".")[-1] == "csv":
                self.populate(Table.csv(filename))
            elif filename.split(".")[-1] == "arff":
                self.populate(Table.arff(filename))

    def populate(self, file_reader):
        """
        Populate this Table object with the data in filename.
        Hard coded choice that features are the first n-1 items.
        """

        # Initialize first data row and the column statistics row
        header = file_reader.next()
        row = file_reader.next()
        features = row[:-1]
        outcomes = row[-1:]
        self.rows.append(Row(features, outcomes))
        col_features = map(Table.construct_column, zip(features, header[:-1]))
        col_outcomes = map(Table.construct_column, zip(outcomes, header[-1:]))
        self.cols = Row(col_features, col_outcomes)

        # Read in the rest
        for row in file_reader:
            self.rows.append(Row(features=row[:-1], outcomes=row[-1:]))
            for item, col in zip(row, self.cols):
                col.add(item)

    def add_row(self, row):
        """
        Add a single row. Populate self.cols if not already populated
        """
        self.rows.append(row)
        if self.cols is None:
            col_features = map(Table.construct_column,
              itertools.izip_longest(row.features, []))
            col_outcomes = map(Table.construct_column,
              itertools.izip_longest(row.outcomes, []))
            self.cols = Row(col_features, col_outcomes)
        else:
            for item, col in zip(row, self.cols):
                col.add(item)

    @staticmethod
    def construct_column((item, name)):
        """
        Takes an item and constructs the appropriate column type.
        """
        try:
            col = Num(item, name)
        except:
            col = Sym(item, name)
        return col

    # Adapted from timm's https://github.com/txt/fss16/blob/master/src/rows.py
    @staticmethod
    def parse_rows(file,prep = None, whitespace = '[\n\r\t]', comments = '#.*',
      sep = ","):
      """
      Walk down comma seperated values,
      skipping bad white space and blank lines
      """
      doomed = re.compile('(' + whitespace + '|' +  comments + ')')
      with open(file) as fs:
          for line in fs:
              line = re.sub(doomed, "", line)
              if line:
                  row = map(lambda z:z.strip(), line.split(sep))
                  if len(row)> 0:
                      yield prep(row) if prep else row

    # Adapted from timm's https://github.com/txt/fss16/blob/master/src/rows.py
    @staticmethod
    def csv(file):
        """
        Convert rows of strings to ints, floats, or strings as appropriate
        (assuming a .csv file.
        First yielded row is the header.
        """
        def atoms(lst):
            return map(atom,lst)
        def atom(x)  :
            try: return int(x)
            except:
                try: return float(x)
                except ValueError: return x
        for row in Table.parse_rows(file, prep=atoms):
            yield row

    @staticmethod
    def arff(file):
        """
        Convert rows of strings to int, floats, or strings as appropriate
        (assuming an .arff file).
        First yielded row is the header.
        """
        def atoms(lst):
            return map(atom,lst)
        def atom(x)  :
            try: return int(x)
            except:
                try: return float(x)
                except ValueError: return x
        header = []

        row_generator = Table.parse_rows(file, prep=atoms)
        row = row_generator.next()
        while "@data" not in row[0].lower():
            if "@attribute" in row[0].lower():
                header.append(row[0].split(" ")[1])
            row = row_generator.next()
        yield header
        for row in row_generator:
            yield row

    # Gets
    def iterate_rows(self, features_only=True):
        if features_only:
            for row in self.rows:
                yield row.features
        else:
            for row in self.rows:
                yield row

    def iterate_cols(self, features_only=True):
        if features_only:
            for col in self.cols.features:
                yield col
        else:
            for col in self.cols.features + self.cols.outcomes:
                yield col

    # Prints
    def print_statistics(self):
        """
        Print the Table's statistics.
        """
        COL_SIZE = 20
        print "Column Name".ljust(COL_SIZE) + "Statistics"
        for col in self.cols:
            print col.name.ljust(COL_SIZE) + col.show()

    # Internal methods

    # Adapted from Aha's algorithm: http://goo.gl/ZspOeL
    def row_distance(self, row1, row2):
        """
        Compute the distance of row1 from row2 in Table.
        Assumes that row1, row2, and self.cols are the full Row object,
        so we can pull out the features.
        Assumes len(row1) == len(row2) == len(self.cols).
        """
        return math.sqrt(sum([col.distance(item1, item2)**2 for col, item1,
          item2 in zip(self.cols.features, row1.features, row2.features)]))

    def row_distances(self, new_row):
        """
        Generates the distance of new_row from each row in the table.
        """
        class DistanceItem():
            def __init__(self, row, distance):
                self.row = row
                self.distance = distance

        for row in self.rows:
            yield DistanceItem(distance=self.row_distance(new_row, row),
              row=row)

    def closest(self, new_row):
        """
        Returns the closest Row object in the Table.
        """
        distances = list(self.row_distances(new_row))
        return min(distances, key=lambda item: item.distance).row

    def size(self):
        """
        Returns the table size.
        """
        return len(self.rows)

if __name__ == "__main__":
    pass
