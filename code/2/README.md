# Homework 2
## Active Shooter Exercise
* Things _not_ to do
   * Do not enter a situation unprepared, otherwise you'll freeze.
   * Do not run or yell at police.
* Things to do
   * Have a survivor's mentality, identify the exits for rooms you frequent and how you might respond to a shooter.
   * Call 911 when you get the chance, do _not_ assume someone else will.

## ZeroR

My Python implementation heavily relies on the ``Table`` class defined in the next section, plus a quick .arff reader extension:

```python
class ZeroR:
    def __init__(self, training_data):
        self.table = Table(training_data)
```

Once this table is populated, our learner is completely (trivially) trained:

```python
def predict(self, row):
    # Return the most common outcome
    return self.table.cols[-1].mode
```

To call the ``zeror.py`` learner from the ``ninja.rc`` script I filled in the provided ``zeror`` function:

```
zeror() {
  python $Here/../../2/ZeroR.py -train $1 -test $2
}
```

Finally, made a new ``eg11`` by adding ``zeror`` to the learners from ``eg10``. The output after training looks like this:

```
pd

rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,        zeror ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   2 ,           nb ,      45  ,    18 (        ---   *| --           ),25.00, 36.00, 45.00, 53.00, 60.00
   2 ,       rbfnet ,      47  ,    20 (        ------ *   ---        ),25.00, 43.00, 47.00, 60.00, 67.00
   3 ,         bnet ,      60  ,    17 (             --|-- *  -       ),40.00, 55.00, 60.00, 67.00, 71.00
   3 ,         jrip ,      60  ,    23 (          -----|   *   ---    ),33.00, 50.00, 60.00, 71.00, 80.00
   4 ,          j48 ,      72  ,    16 (               |-----  *  --  ),50.00, 65.00, 72.00, 81.00, 87.00
pf

rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,        zeror ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   2 ,          j48 ,       7  ,     6 (     --   *  --|---           ), 4.00,  5.00,  7.00,  9.00, 13.00
   2 ,           nb ,       7  ,     6 (     --   *   -|-             ), 4.00,  5.00,  7.00, 10.00, 12.00
   2 ,         jrip ,       9  ,    10 (  ---        * |------        ), 2.00,  4.00,  9.00, 11.00, 15.00
   2 ,       rbfnet ,       9  ,     5 (     -----   * |----          ), 4.00,  7.00,  9.00, 11.00, 14.00
   2 ,         bnet ,      11  ,     6 (        -----  |*   ------    ), 6.00,  9.00, 11.00, 14.00, 18.00
```

Verifying this output, I saw that ``zeror`` predicts ``false`` for the dataset ``jedit-4.1.arff``, resulting in c = d = 0, which means that pd = pf = 0 as well.


## Table Reader
For the CSV reader, I made some trivial changes to the ``rows`` and ``csv`` methods from [``rows.py``](https://github.com/txt/fss16/blob/master/src/rows.py). In effect, the resulting ``Table.csv(csv_filename)`` generator could be used as a black-box row generator for CSV files. As mentioned above, I also implemented an arff version for convenience.

For the Table class, I used a straightforward constructor that recognized if we passed in a CSV or arff file, and otherwise delegated the heavy lifting to a ``populate`` method:

```python
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
```

The ``populate`` method takes in a filename and populates the ``rows``, ``cols``, and ``header`` fields in the current ``Table`` object by using the appropriate file reader:

```python
def populate(self, filename):
    row_generator = self.file_reader(filename)
    self.header = row_generator.next()
    self.rows.append(row_generator.next())
    self.cols = [Table.construct_column(item) for item in self.rows[-1]]
    for row in row_generator:
        self.rows.append(row)
        for item, col in zip(row, self.cols):
            col.add(item)
```

I first pop off the CSV's header to keep track of the column names for prettier output, then use the first data row to construct the appropriate ``Num`` or ``Sym`` object with ``Table.construct_column(item)``. The rest of the data is then read into the rows and statistics are tracked per column.

At the end, I run a ``print_statistics`` method that iterates through the columns and prints their names and statistics:

```
$ python Table.py -dataset weather.csv
Column Name         Statistics
outlook             mode: sunny, entropy: 1.577406
temperature-        mean: 73.571429, standard deviation: 6.571667
<humidity           mean: 81.642857, standard deviation: 10.285218
windy               mode: FALSE, entropy: 0.985228
>play               mean: 1.071429, standard deviation: 0.997249
```
