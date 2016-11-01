# CODE7: Discretization

## Code

The code was a fairly straightforward modification of CODE5. First, we need the `Num` class to support two different discretization methods: EID and EFD. The EID one is very easy to integrate, we simply take the max and min and divide the middle into equal sized bins. When we're ready to check which bin a value belongs to, we simply plug it into the equation:

```python

def eid(self, feature_value):
   return int((self.discretization.bins-1) * (feature_value - self.lo) / (self.up - self.lo))
```

The EFD function took a little more thought. First, the frequency needs to be recorded over the whole training data, so we need to keep the
training data around in the Naive Bayes learner. Some care also must be taken for the bookkeeping of which values are discretized and which aren't;
I ended up maintaining two lists of rows. The standard `rows` list maintained the raw input values, and an `output_row` contained
what the outside world would see (through something like `Table.iterate_rows()`). If the `Table()` object wasn't given a specific
discretization, then these two lists were the same; otherwise the `output_row` list would contain the discretized values.

## Experiments

In the tradition of CODE4, 5, and 6, I've used the same dataset and preprocessing scripts:

| Dataset  | Source  | Rows   | Features  | Classes | % target class  |
|---|---|---|---|---|
| bool_jedit-4.2.arff | [PROMISE Repo](http://openscience.us/repo/defect/ck/jedit.html) | 492 | 20 | 2 | 2% |
| bool_camel-1.6.arff  | [PROMISE Repo](http://openscience.us/repo/defect/ck/camel.html)   | 965  | 20  | 2  | 19% |
| bool_lucene-2-4.arff  | [PROMISE Repo](http://openscience.us/repo/defect/ck/lucene.html)   | 340  | 20  | 2  | 60% |
| bool_xalan-2.7.arff  | [PROMISE Repo](http://openscience.us/repo/defect/ck/xalan.html)   | 909  | 20  | 2  | 98% |
| wine.arff | [UCI Repo](https://archive.ics.uci.edu/ml/datasets/Wine)  | 178 | 13 | 3 | 33% |

Because the discretization methods each include a parameter (number of bins), I ranged over the powers of 2 from 2^1 to 2^12. The output looked like this:

```
bool_camel-1.6.arff

pd

rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,   nb_efd2048 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,   nb_efd4096 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,      nb_eid2 ,       0  ,     3 (*              |              ), 0.00,  0.00,  0.00,  3.00,  6.00
   1 ,   nb_efd1024 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   2 ,    nb_efd256 ,      12  ,     7 (---*--         |              ), 3.00, 10.00, 12.00, 14.00, 20.00
   3 ,      nb_eid4 ,      16  ,     7 (  --*--        |              ), 9.00, 14.00, 16.00, 19.00, 25.00
   3 ,    nb_efd128 ,      17  ,     6 (  -- *         |              ), 7.00, 13.00, 17.00, 19.00, 22.00
   3 ,     nb_efd64 ,      19  ,    11 (  -- * --      |              ), 8.00, 14.00, 19.00, 23.00, 30.00
   4 ,     nb_efd32 ,      21  ,    13 (    - *---     |              ),13.00, 17.00, 21.00, 25.00, 33.00
   4 ,     nb_efd16 ,      23  ,    11 (    -- *-      |              ),14.00, 20.00, 23.00, 29.00, 32.00
   4 ,           nb ,      25  ,     8 (     --*--     |              ),17.00, 23.00, 25.00, 29.00, 34.00
   4 ,      nb_eid8 ,      26  ,    12 (     -- *-     |              ),18.00, 23.00, 26.00, 31.00, 34.00
   5 ,      nb_efd8 ,      30  ,     9 (      -  *--   |              ),21.00, 25.00, 30.00, 33.00, 40.00
   5 ,     nb_eid32 ,      33  ,     9 (       -- * -  |              ),24.00, 31.00, 33.00, 39.00, 45.00
   5 ,     nb_eid16 ,      33  ,     8 (       -- *-   |              ),25.00, 31.00, 33.00, 38.00, 42.00
   5 ,     nb_eid64 ,      34  ,    13 (        - * ---|              ),26.00, 31.00, 34.00, 40.00, 53.00
   5 ,    nb_eid128 ,      39  ,     8 (        --  *--|--            ),27.00, 35.00, 39.00, 43.00, 61.00
   5 ,      nb_efd4 ,      40  ,    12 (        --  *- |              ),28.00, 34.00, 40.00, 44.00, 48.00
   5 ,    nb_eid256 ,      42  ,    12 (         -- * -|------        ),32.00, 36.00, 42.00, 47.00, 74.00
   5 ,    nb_eid512 ,      45  ,     9 (          ---* |-------       ),35.00, 43.00, 45.00, 50.00, 75.00
   5 ,    nb_efd512 ,      45  ,    12 (         --- * |-             ),32.00, 39.00, 45.00, 50.00, 55.00
   5 ,      nb_efd2 ,      46  ,    11 (         ---  *|-             ),32.00, 42.00, 46.00, 49.00, 56.00
   5 ,   nb_eid1024 ,      47  ,     8 (              *|--------      ),39.00, 42.00, 47.00, 50.00, 79.00
   5 ,   nb_eid2048 ,      49  ,    11 (            -  *--------      ),40.00, 45.00, 49.00, 54.00, 79.00
   5 ,   nb_eid4096 ,      50  ,    11 (            -  * --------     ),40.00, 45.00, 50.00, 55.00, 81.00
pf

rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,   nb_efd2048 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,   nb_efd4096 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,      nb_eid2 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,   nb_efd1024 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   2 ,   nb_eid1024 ,       1  ,     2 (*--------------|              ), 0.00,  0.00,  1.00,  2.00, 19.00
   2 ,   nb_eid4096 ,       1  ,     1 (*--------------|-             ), 0.00,  0.00,  1.00,  1.00, 22.00
   2 ,    nb_eid512 ,       1  ,     1 (*-----------   |              ), 0.00,  1.00,  1.00,  2.00, 15.00
   2 ,   nb_eid2048 ,       1  ,     2 (*--------------|-             ), 0.00,  0.00,  1.00,  1.00, 21.00
   2 ,    nb_eid256 ,       1  ,     1 (*--------      |              ), 1.00,  1.00,  1.00,  2.00, 12.00
   2 ,    nb_efd256 ,       2  ,     2 ( *             |              ), 0.00,  1.00,  2.00,  2.00,  3.00
   2 ,    nb_eid128 ,       3  ,     3 (- *---         |              ), 1.00,  2.00,  3.00,  4.00,  8.00
   2 ,    nb_efd128 ,       3  ,     1 (- *-           |              ), 1.00,  2.00,  3.00,  3.00,  5.00
   2 ,      nb_eid4 ,       4  ,     2 ( - *--         |              ), 2.00,  3.00,  4.00,  4.00,  8.00
   2 ,     nb_efd64 ,       4  ,     3 ( - *-          |              ), 2.00,  3.00,  4.00,  6.00,  7.00
   3 ,     nb_efd32 ,       6  ,     3 (  --*--        |              ), 3.00,  5.00,  6.00,  7.00,  9.00
   3 ,     nb_eid64 ,       6  ,     3 (   -* --       |              ), 4.00,  6.00,  6.00,  8.00, 11.00
   3 ,           nb ,       7  ,     3 (     * -       |              ), 5.00,  6.00,  7.00,  9.00, 11.00
   3 ,      nb_eid8 ,       8  ,     5 (    - * --     |              ), 5.00,  7.00,  8.00, 11.00, 13.00
   3 ,     nb_efd16 ,       8  ,     4 (      * -      |              ), 5.00,  6.00,  8.00, 10.00, 12.00
   3 ,     nb_eid32 ,       9  ,     5 (   --- *---    |              ), 4.00,  8.00,  9.00, 11.00, 14.00
   3 ,     nb_eid16 ,      10  ,     4 (    --  *---   |              ), 6.00,  8.00, 10.00, 12.00, 16.00
   4 ,      nb_efd8 ,      15  ,     5 (       --   *--|-             ), 9.00, 12.00, 15.00, 17.00, 22.00
   5 ,      nb_efd4 ,      23  ,     4 (             --|- *------     ),17.00, 21.00, 23.00, 23.00, 31.00
   6 ,    nb_efd512 ,      27  ,     4 (               |---  *---     ),19.00, 24.00, 27.00, 28.00, 31.00
   6 ,      nb_efd2 ,      29  ,     6 (             --|-----  * ---- ),17.00, 26.00, 29.00, 31.00, 36.00
```

Clearly evaluating this many learners looks messy if all the data is presented, so in the below output I'm presenting the following five learners:
1. The original Naive Bayes classifier.
2. The top performing EID.
3. The worst performing EID.
4. The top performing EFD.
5. The worst performing EFD.

Specifically, performance is evaluated as (a) top category recall, (b) lowest category false alarm, and (c) smallest number of bins. The last one is important because run times increase as the number of bins grow.


```
bool_camel-1.6.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,   nb_efd2048 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,      nb_eid2 ,       0  ,     3 (*              |              ), 0.00,  0.00,  0.00,  3.00,  6.00
   4 ,           nb ,      25  ,     8 (     --*--     |              ),17.00, 23.00, 25.00, 29.00, 34.00
   5 ,      nb_efd2 ,      46  ,    11 (         ---  *|-             ),32.00, 42.00, 46.00, 49.00, 56.00
   5 ,   nb_eid4096 ,      50  ,    11 (            -  * --------     ),40.00, 45.00, 50.00, 55.00, 81.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,   nb_efd2048 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,      nb_eid2 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   3 ,           nb ,       7  ,     3 (     * -       |              ), 5.00,  6.00,  7.00,  9.00, 11.00
   2 ,   nb_eid4096 ,       1  ,     1 (*--------------|-             ), 0.00,  0.00,  1.00,  1.00, 22.00
   6 ,      nb_efd2 ,      29  ,     6 (             --|-----  * ---- ),17.00, 26.00, 29.00, 31.00, 36.00
```

```
bool_jedit-4.3.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,   nb_efd2048 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,      nb_eid8 ,       0  ,    25 (*      ------- |              ), 0.00,  0.00,  0.00, 25.00, 50.00
   1 ,      nb_efd8 ,      20  ,    50 (     *        -|------        ), 0.00,  0.00, 20.00, 50.00, 75.00
   1 ,           nb ,      40  ,    80 (-------    *  -|------------- ), 0.00, 25.00, 40.00, 50.00, 100.00
   1 ,     nb_eid32 ,      50  ,    50 (-----         *| ------------ ), 0.00, 20.00, 50.00, 60.00, 100.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,   nb_efd2048 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,      nb_eid8 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  1.00
   1 ,     nb_eid32 ,       0  ,     1 (*              |              ), 0.00,  0.00,  0.00,  1.00,  3.00
   2 ,      nb_efd8 ,       4  ,     5 (-*-            |              ), 1.00,  3.00,  4.00,  6.00, 10.00
   3 ,           nb ,       6  ,    36 (- *   ---------|------------- ), 2.00,  3.00,  6.00, 17.00, 76.00
```

```
bool_lucene-2.4.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,      43  ,    12 ( --  * ----    |              ),33.00, 37.00, 43.00, 47.00, 56.00
   1 ,   nb_eid1024 ,      71  ,    43 (        ----   | *          - ),50.00, 59.00, 71.00, 96.00, 100.00
   1 ,      nb_efd4 ,      63  ,    13 (         ---  *|---           ),51.00, 59.00, 63.00, 67.00, 76.00   
   1 ,     nb_efd64 ,      71  ,    11 (           ----| * -          ),56.00, 65.00, 71.00, 74.00, 77.00
   1 ,      nb_eid8 ,      72  ,    17 (           --- |  *---        ),56.00, 63.00, 72.00, 76.00, 82.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,   nb_eid1024 ,       8  ,    41 (  *        --- |              ), 0.00,  3.00,  8.00, 38.00, 48.00
   1 ,           nb ,       9  ,    10 (--* ---        |              ), 3.00,  7.00,  9.00, 16.00, 24.00
   1 ,      nb_efd4 ,      29  ,    18 (    --  * ---  |              ),15.00, 23.00, 29.00, 36.00, 44.00
   1 ,      nb_eid8 ,      30  ,    11 (    --- * -    |              ),16.00, 25.00, 30.00, 35.00, 38.00
   1 ,     nb_efd64 ,      31  ,    17 (    ---  * -   |              ),14.00, 25.00, 31.00, 37.00, 42.00
```

```
bool_xalan-2.7.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,      85  ,     9 (  -----   *    |--------      ),79.00, 83.00, 85.00, 90.00, 96.00
   1 ,    nb_efd256 ,      93  ,     2 (               |  - * ----    ),91.00, 92.00, 93.00, 94.00, 97.00
   1 ,     nb_eid32 ,      97  ,     3 (               |      --  *-- ),94.00, 96.00, 97.00, 98.00, 100.00
   1 ,      nb_efd2 ,      97  ,     2 (               |      ----*-  ),94.00, 97.00, 97.00, 98.00, 99.00
   1 ,     nb_eid64 ,      98  ,     1 (               |          -*- ),97.00, 98.00, 98.00, 99.00, 100.00


pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,       0  ,    25 (*    ------    |              ), 0.00,  0.00,  0.00, 17.00, 40.00
   1 ,     nb_eid32 ,       6  ,    33 ( *       ------|----          ), 0.00,  0.00,  6.00, 33.00, 67.00
   1 ,      nb_efd2 ,       7  ,    33 (  *      ------|------        ), 0.00,  0.00,  7.00, 33.00, 75.00
   1 ,     nb_eid64 ,      25  ,    40 (       * ------|----          ), 0.00,  0.00, 25.00, 33.00, 67.00
   1 ,    nb_efd256 ,      33  ,    46 (-        *    -|------------- ), 0.00,  6.00, 33.00, 50.00, 100.00
```

```
wine.arff

pd
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,    nb_efd512 ,       0  ,     0 (*--------------|------------- ), 0.00,  0.00,  0.00,  0.00, 100.00
   1 ,      nb_eid2 ,      15  ,    82 (--  *        --|------------- ), 0.00,  8.00, 15.00, 45.00, 100.00
   1 ,           nb ,     100  ,     9 (               |         --  *),86.00, 92.00, 100.00, 100.00, 100.00
   1 ,      nb_eid8 ,     100  ,     9 (               |         --  *),86.00, 91.00, 100.00, 100.00, 100.00
   1 ,      nb_efd2 ,     100  ,     0 (               |           --*),92.00, 100.00, 100.00, 100.00, 100.00

pf
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           nb ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  0.00
   1 ,      nb_efd2 ,       0  ,     0 (*              |              ), 0.00,  0.00,  0.00,  0.00,  4.00
   1 ,      nb_eid8 ,       0  ,     5 (*---           |              ), 0.00,  0.00,  0.00,  5.00, 15.00
   1 ,    nb_efd512 ,       0  ,     8 (*--------------|------------- ), 0.00,  0.00,  0.00,  5.00, 100.00
   1 ,      nb_eid2 ,       0  ,    85 (*  ------------|-----------   ), 0.00,  0.00,  0.00, 11.00, 92.00
```

The Doughery et al. seems to hold. In all datasets we see an increase in recall for a proper number of bins, and some have very high increase. Of course, the false alarm rate also increased in most of them, but perhaps that's a penalty that users would pay for higher recall.  
