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
    def __init__(self, csv_filename):
        self.rows = []
        self.cols = []
        self.header = []
        self.populate(csv_filename)

    def populate(self, csv_filename):
        row_generator = Table.csv(csv_filename)
        self.header = row_generator.next()
        self.cols = [Table.construct_column(item) for item in row_generator.next()]
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
      """ and print (a) the column name and (b) its statistics: and print (a) the column name and (b) its statistics:
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
        Convert rows of strings to ints,floats, or strings
        as appropriate
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-csv_filename", type=str)
    args = parser.parse_args()
    table = Table(args.csv_filename)
    table.print_statistics()
