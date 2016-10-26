# Homework 6: Anomaly Detection

## Data preprocessing

Since the CK datasets don't have 3 nice classes (nice = enough data per class), I went to the UCI repository and downloaded the `semeion.data` handwritten digits data and the `wine.data` wine data. As usual, I wrote scripts to process these into a useful arff; you can see the scripts at ``data/digit_converter.py`` and ``data/wine_converter.py``.

## Data generator

The data generator code is in ``AnomalyDataGenerator.py``. I start by reading in all the data into ``Table``s based on class value. I then choose to keep the three classes with the most rows.

Once the data is allocated into the respective ``Table``s, generating random data is as easy as (a) keeping track of what era we're on, (b) choosing a ``Table`` with the appropriate weighted random number generator, and (c) choosing a row from this ``Table`` at random.

## Data reader

The data reader is a simple few lines in the main method of ``IncrementalNaiveBayes.py``. We simply loop through the eras with an ``xrange``, request the random data from our ``AnomalyDataGenerator`` object, and feed this data into the ``IncrementalNaiveBayes`` object (initially as testing data, then as training data).

## Incremental NB

The ``NaiveBayes`` classifier from Homework 5 didn't need much updating, mostly just IO bookkeeping. To make it easy, both training and testing functions take a ``Table`` of data instead of filenames or lists of rows. Training makes no assumptions on whether it has been previously trained or not, it simply takes the data we provide and updates the ``Tables`` appropriately. We also need to return the log of the likelihoods, so those are now returned from the ``output_predictions`` method. Since recall depends on your target, ``output_predictions`` also outputs recall for all three classes.


## Output and anomaly detection

When running on digits data, nearly every prediction was the alphabetically-first class. I found this happened because the data is 256 boolean features (the pixels in a 16x16 grid), and so nearly all of the Naive Bayes likelihoods contained at least one zero (e.g. a pixel is always used in Seven but never in Eight), which ruined their multiplication. And this makes sense: we don't expect these pixels to be independent at all. Plus they're very grid-like, probably a good fit for decision trees.

Wine data looked much better:

```
*** Era  1  ***
wine1  recall:  0.979591836735
wine2  recall:  0.941176470588
wine3  recall:  0.0

*** Era  2  ***
wine1  recall:  0.961538461538
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.4629

*** Era  3  ***
wine1  recall:  0.954545454545
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.515

*** Era  4  ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.5116

*** Era  5  ***
wine1  recall:  0.978723404255
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.4941

*** Era  6  ***
wine1  recall:  0.98
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.5335

*** Era  7  ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.5243

*** Era  8  ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.4606

*** Era  9  ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.4816

*** Era  10 (wine 3 introduced) ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  0.0
a12:  0.2986
a12 score different by >20%, ANOMALY DETECTED!!

*** Era  11  ***
wine1  recall:  0.909090909091
wine2  recall:  1.0
wine3  recall:  1.0
a12:  0.7187
a12 score different by >20%, ANOMALY DETECTED!!

*** Era  12  ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  1.0
a12:  0.4876
a12 score different by >20%, ANOMALY DETECTED!!

*** Era  13  ***
wine1  recall:  0.888888888889
wine2  recall:  0.958333333333
wine3  recall:  1.0
a12:  0.4913

*** Era  14  ***
wine1  recall:  1.0
wine2  recall:  0.944444444444
wine3  recall:  1.0
a12:  0.5134

*** Era  15  ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  1.0
a12:  0.4856

*** Era  16  ***
wine1  recall:  1.0
wine2  recall:  0.972222222222
wine3  recall:  1.0
a12:  0.4758

*** Era  17  ***
wine1  recall:  1.0
wine2  recall:  0.95
wine3  recall:  1.0
a12:  0.5617

*** Era  18  ***
wine1  recall:  1.0
wine2  recall:  1.0
wine3  recall:  1.0
a12:  0.5429

*** Era  19  ***
wine1  recall:  1.0
wine2  recall:  0.928571428571
wine3  recall:  1.0
a12:  0.4828

```

As we can see, I detected anomalies by looking for a 20% change from the a12 previous value. At first I was only checking for an increase, but when the ``wine3`` class was introduced I saw that the a12 score actually decreased. But I think this makes sense: a12 gauges how the two distributions interact. A larger a12 score means the distributions are very different, a small means they're pretty close. Either way, if the a12 score changes a lot, then the likelihood distributions have changed and something happened.
