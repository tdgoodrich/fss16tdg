# Homework 2
## Active Shooter Exercise
* Things _not_ to do
   * Do not enter a situation unprepared, otherwise you'll freeze.
   * Do not run or yell at police.
* Things to do
   * Have a survivor's mentality, identify the exits for rooms you frequent and how you might respond to a shooter.
   * Call 911 when you get the chance, do _not_ assume someone else will.

## ZeroR

Finally, we call the ``zeror.py`` learner from the ``ninja.rc`` script:

```
zeror() {
  python "$Here/zeror.py -test %s -train %s -header True" % ($1, $2)
}
zeror10() {
  python "$Here/zeror.py -train %s -header True" % ($1)
}

```


## Table Reader
For the CSV reader, I made some trivial changes to the ``rows`` and ``csv`` methods from [``rows.py``](https://github.com/txt/fss16/blob/master/src/rows.py). In effect, the resulting ``Table.csv(csv_filename)`` generator could be used as a black-box row generator for CSV files.

For the Table class, I used a straightforward constructor that delegated the heavy lifting to a ``populate`` method:

```python
def __init__(self, csv_filename):
    self.rows = []
    self.cols = []
    self.header = []
    self.populate(csv_filename)
```

The ``populate`` method takes in a CSV filename and populates the ``rows``, ``cols``, and ``header`` fields in the current ``Table`` object:

```python
def populate(self, csv_filename):
    row_generator = Table.csv(csv_filename)
    self.header = row_generator.next()
    self.cols = [Table.construct_column(item) for item in row_generator.next()]
    for row in row_generator:
        self.rows.append(row)
        for item, col in zip(row, self.cols):
            col.add(item)
```

I first pop off the CSV's header to keep track of the column names for prettier output, then use the first data row to construct the appropriate ``Num`` or ``Sym`` object with ``Table.construct_column(item)``. The rest of the data is then read into the rows and statistics are tracked per column.

At the end, I run a ``print_statistics`` method to iterate through the columns and print their names and statistics:

```
$ python Tables.py -csv_filename weather.csv
Column Name         Statistics
outlook             mode: sunny, entropy: 1.577406
temperature-        mean: 73.571429, standard deviation: 6.571667
<humidity           mean: 81.642857, standard deviation: 10.285218
windy               mode: FALSE, entropy: 0.985228
>play               mean: 1.071429, standard deviation: 0.997249

```
