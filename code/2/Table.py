import re, argparse, math

def max(x,y) : return x if x>y else y
def min(x,y) : return x if x<y else y

# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw2.md
class Num:
    def __init__(self):
        self.sum,self.mu,self.n,self.m2,self.up,self.lo = 0,0,0,0,-10e32,10e32

    def add(self,x):
        self.n += 1
        x = float(x)
        self.sum += x
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
        return "mean: %f, standard deviation: %f" % (self.sum/self.n,
          self.standard_deviation())

# Adapted from timm's https://github.com/txt/fss16/blob/master/doc/hw2.md
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
        return "mode: %s, entropy: %f" % (self.mode, self.entropy())

class Table:
    def __init__(self, filename):
        self.rows = []
        self.cols = []
        self.header = []
        self.file_reader = None
        if filename.split(".")[-1] == "csv":
            self.file_reader = Table.csv
        elif filename.split(".")[-1] == "arff":
            self.file_reader = Table.arff
        self.populate(filename)

    def populate(self, filename):
        row_generator = self.file_reader(filename)
        self.header = row_generator.next()
        self.rows.append(row_generator.next())
        self.cols = [Table.construct_column(item) for item in self.rows[-1]]
        for row in row_generator:
            self.rows.append(row)
            for item, col in zip(row, self.cols):
                col.add(item)

    def print_statistics(self):
        COL_SIZE = 20
        print "Column Name".ljust(COL_SIZE) + "Statistics"
        for col_name, col in zip(self.header, self.cols):
            print col_name.ljust(COL_SIZE) + col.show()

    # Takes an item and constructs the appropriate column type
    @staticmethod
    def construct_column(item):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-dataset", type=str, required=True)
    args = parser.parse_args()
    table = Table(args.dataset)
    table.print_statistics()
