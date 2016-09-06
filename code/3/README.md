# Homework 3
## Extending the Table Code

For normalizing and computing distance between elements, I used timm's code verbatim (with some stylistic changes). Plug and play.

For computing distance between two rows, I used [Aha's equation](http://goo.gl/ZspOeL). Two important assumptions here. First, since we want distance I dropped the negative sign from the similarity equation. Second, I assumed that the loaded dataset is complete (not missing values). This assumption is reasonable given the weather dataset, but should certainly be updated once we know what the missing values look like (e.g. ``NA`` or ``?``, etc.). Mostly this assumption was made for very simple code:

```python
# Adapted from Aha's algorithm: http://goo.gl/ZspOeL
def row_distance(self, row1, row2):
    """
    Compute the distance of row1 from row2 in Table.
    Assumes len(row1) == len(row2) == len(self.cols).
    """
    return math.sqrt(sum([col.distance(item1, item2) for col, item1,
      item2 in zip(self.cols, row1, row2)]))
```

Testing the code on the ``weather.arff`` dataset:
```
$ python Table.py -dataset weather.csv
Row 1          : ['sunny', 85, 85, 'FALSE', 0]
-- closest row : ['sunny', 72, 95, 'FALSE', 0]
-- furthest row: ['overcast', 64, 65, 'TRUE', 2]
Row 2          : ['sunny', 80, 90, 'TRUE', 0]
-- closest row : ['sunny', 75, 70, 'TRUE', 2]
-- furthest row: ['rainy', 68, 80, 'FALSE', 1]
```
