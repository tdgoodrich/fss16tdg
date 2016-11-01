# CODE5: Naive Bayes Classifier

## Code

We start the Naive Bayes class similarly to the ones from CODE4, with standardized train and predict methods. This time we're going to keep a table for each of the outcome values, and the needed statistics for each table. To evaluate the fit of a particular class, we simply compute the likeihood for each feature:

```python
def evaluate_outcome(self, row, outcome):
    result = float(self.outcome_counts.get(outcome, 0)) / sum(self.outcome_counts.itervalues())
    for feature, col in zip(row.features, self.outcome_tables[outcome].iterate_cols(features_only=True)):
        result *= col.bayes_evaluate(feature)
    return result
```

## Experiments

We continue using CODE4's input corpus. For completeness, we reproduce the table here:


| Dataset  | Source  | Rows   | Features  | Classes | % target class  |
|---|---|---|---|---|
| bool_jedit-4.2.arff | [PROMISE Repo](http://openscience.us/repo/defect/ck/jedit.html) | 492 | 20 | 2 | 2% |
| bool_camel-1.6.arff  | [PROMISE Repo](http://openscience.us/repo/defect/ck/camel.html)   | 965  | 20  | 2  | 19% |
| bool_lucene-2-4.arff  | [PROMISE Repo](http://openscience.us/repo/defect/ck/lucene.html)   | 340  | 20  | 2  | 60% |
| bool_xalan-2.7.arff  | [PROMISE Repo](http://openscience.us/repo/defect/ck/xalan.html)   | 909  | 20  | 2  | 98% |
| wine.arff | [UCI Repo](https://archive.ics.uci.edu/ml/datasets/Wine)  | 178 | 13 | 3 | 33% |

Running the datasets, we get the following solution qualities:

```
bool_jedit-4.3.arff
pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,        zeror ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   2 ,        kdknn ,      25  ,    50 (         *    -|------------- ), 0.00,  0.00, 33.00, 50.00, 100.00
   2 ,           nb ,      40  ,    80 (-------    *  -|------------- ), 0.00, 25.00, 40.00, 50.00, 100.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,        zeror ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,        kdknn ,       0  ,     1 (*              |              ), 0.00,  0.00,  0.00,  1.00,  2.00
   2 ,           nb ,       6  ,    36 (- *   ---------|------------- ), 2.00,  3.00,  6.00, 17.00, 76.00

```


```
bool_camel-1.6.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,        zeror ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   2 ,           nb ,      25  ,     8 (      -- * --  |              ),17.00, 23.00, 25.00, 29.00, 34.00
   3 ,        kdknn ,      69  ,    12 (               |    ----  * - ),54.00, 63.00, 69.00, 73.00, 77.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,        zeror ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   2 ,           nb ,       7  ,     3 (         --  * |----          ), 5.00,  6.00,  7.00,  9.00, 11.00
   2 ,        kdknn ,       9  ,     3 (         ----  |* ----        ), 5.00,  7.00,  9.00, 10.00, 12.00

```


```
bool_lucene-2-4.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,      43  ,    12 ( --  * ----    |              ),33.00, 37.00, 43.00, 47.00, 56.00
   2 ,        kdknn ,      86  ,     7 (               |   ---- *--   ),76.00, 84.00, 86.00, 89.00, 95.00
   3 ,        zeror ,     100  ,     0 (               |             *),100.00, 100.00, 100.00, 100.00, 100.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,       9  ,    10 (--* ---        |              ), 3.00,  7.00,  9.00, 16.00, 24.00
   2 ,        kdknn ,      21  ,    15 (  --- * -      |              ),10.00, 17.00, 21.00, 30.00, 33.00
   3 ,        zeror ,     100  ,     0 (               |             *),100.00, 100.00, 100.00, 100.00, 100.00

```

```
bool_xalan-2.7.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,      85  ,     9 (  -----   *    |--------      ),79.00, 83.00, 85.00, 90.00, 96.00
   2 ,        zeror ,     100  ,     0 (               |             *),100.00, 100.00, 100.00, 100.00, 100.00
   2 ,        kdknn ,     100  ,     0 (               |            -*),99.00, 100.00, 100.00, 100.00, 100.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,       0  ,    25 (*    ------    |              ), 0.00,  0.00,  0.00, 17.00, 40.00
   1 ,        kdknn ,       0  ,    33 (*        ------|----          ), 0.00,  0.00,  0.00, 33.00, 67.00
   1 ,        zeror ,     100  ,     0 (---------------|-------------*), 0.00, 100.00, 100.00, 100.00, 100.00

```

```
wine.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,        zeror ,       0  ,     0 (*--------------|------------- ), 0.00,  0.00,  0.00,  0.00, 100.00
   1 ,        kdknn ,      93  ,    10 (               |         --*  ),86.00, 91.00, 93.00, 100.00, 100.00
   1 ,           nb ,     100  ,     9 (               |         --  *),86.00, 92.00, 100.00, 100.00, 100.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,        zeror ,       0  ,     0 (*--------------|------------- ), 0.00,  0.00,  0.00,  0.00, 100.00
   1 ,        kdknn ,       5  ,     8 ( *-            |              ), 0.00,  0.00,  5.00,  5.00, 11.00

```

We see somewhat varied performance. On the CK datasets, KDTreeKNN comes out as the slight winner in most (camel, lucene, xalan). However, Naive Bayes performs better on the wine data. Perhaps this difference is actually a difference in the datasets. Could the object-oriented metrics have high dependencies, whereas he wine attributes are more independent? If so, is a good learner for one data a
bad learner for the other? Something to ponder.
