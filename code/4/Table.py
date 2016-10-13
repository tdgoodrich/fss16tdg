"""
Table.py : A table class for reading in datasets (CSV and arff supported).
Limitations and assumptions:
- Currently assumes a complete dataset (i.e. no missing values). If this needs
  to change then the distance methods need to be updated.
- Assumes that the dataset file comes with an appropriate header:
  CSV : top row
  arff: @attribute labels
"""


import re, argparse, math
from itertools import chain

# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw2.md
# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw3.md
class Num:
    def __init__(self):
        self.mu,self.n,self.m2,self.up,self.lo = 0,0,0,-10e32,10e32

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
        tmp= (x - self.lo) / (self.up - self.lo + 10**-32)
        if tmp > 1: return 1
        elif tmp < 0: return 0
        else: return tmp

    def distance(self, x, y):
        dist = self.norm(x) - self.norm(y)
        return dist if dist > 0 else -1*dist

    def furthest(self, x) :
        return self.up if x < (self.up-self.lo)/2 else self.lo

# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw2.md
# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw3.md
class Sym:
    def __init__(self):
        self.counts, self.most, self.mode, self.n = {},0,None,0

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

class Table:
    def __init__(self, filename):
        """
        Initialize the Table object with
        - rows: The rows of data
        - cols: Some statistics we keep for each column
        - header: The name of each column, as a row
        - file_reader: Function for correctly (csv/arff) reading the filename
        """
        self.rows = []
        self.cols = []
        self.header = []
        if filename.split(".")[-1] == "csv":
            self.populate(filename, Table.csv(filename))
        elif filename.split(".")[-1] == "arff":
            self.populate(filename, Table.arff(filename))

    # Gets
    def row_generator(self, features_only = True):
        for row in self.rows:
            yield row[:-1]

    def col_generator(self, features_only = True):
        if features_only:
            for col in self.cols[:-1]:
                yield col
        else:
            for col in self.cols:
                yield col

    def populate(self, filename, file_reader):
        """
        Populate this Table object with the data in filename.
        """
        self.header = file_reader.next()
        self.rows.append(file_reader.next())
        self.cols = map(Table.construct_column, self.rows[-1])
        for row in file_reader:
            self.rows.append(row)
            for item, col in zip(row, self.cols):
                col.add(item)

    def print_statistics(self):
        """
        Print the Table's statistics.
        """
        COL_SIZE = 20
        print "Column Name".ljust(COL_SIZE) + "Statistics"
        for col_name, col in zip(self.header, self.cols):
            print col_name.ljust(COL_SIZE) + col.show()

    # Adapted from Aha's algorithm: http://goo.gl/ZspOeL
    def row_distance(self, row1, row2):
        """
        Compute the distance of row1 from row2 in Table.
        Assumes len(row1) == len(row2) == len(self.cols).
        """
        return math.sqrt(sum([col.distance(item1, item2) for col, item1,
          item2 in zip(self.cols, row1, row2)]))

    def row_distances(self, new_row):
        """
        Generates the distance of new_row from each row in the table.
        """
        class Item():
            def __init__(self, row, distance):
                self.row = row
                self.distance = distance

        for row in self.rows:
            yield Item(distance=self.row_distance(new_row, row), row=row)

    def closest(self, new_row):
        distances = list(self.row_distances(new_row))
        return min(distances, key=lambda item: item.distance).row

    def size(self):
        return len(self.rows)

    @staticmethod
    def construct_column(item):
        """
        Takes an item and constructs the appropriate column type.
        """
        try:
            col = Num()
            col.add(item)
        except:
            col = Sym()
            col.add(item)
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

if __name__ == "__main__":
    pass
