# Homework 1

## Run something

### eg0

This example trains a j4810 learner on the weather.arff dataset.
The weather.arff dataset is composed of four attributes (outlook, temperature, humidity, windy) and one outcome (whether you'll play or not).
Some formatting is done to make the data look nice.
The j4810 learner is a j48 decision tree with 10 cross-validation folds to check that we're not overtraining (i.e. memorizing the dataset).
The learner predicts that you'll play golf if it's sunny but not too humid, if it's overcast, or if it's rainy but not windy.

### eg1

This example takes the weather.arff dataset and prints it nicely.
The command ``cat data/weather.arff`` prints the original dataset.
The previous print is then piped to ``gawk -F, "NF==5``, which outputs the lines with five columns (i.e. the actual data).
The previous print is then piped to ``sort``, which sorts the data lexicographically.
The previous output is then piped to ``column -s, -t``, which formats the columns with tabs instead of commas.

### eg2

This example trains a j4810 learner on the weather dataset and outputs the full learner details with line numbers.
The command ``j4810 data/weather.arff`` trains a j4810 learner (decision tree) on the weather data.
The output of the previous command is then piped to ``cat -n``, which adds line numbers to the learner details.
Some output details include the pruned decision tree, time taken to build and test model; the error, accuracy and confusion matrix before cross-validation; and the same details with stratified cross-validation.

### eg3

This example trains and tests a j48 learner on the same weather.arff dataset.
This is a terrible idea because a decision tree will effectively memorize the training data.
Therefore, if testing on the same data, the predictor will be 100 percent correct!
But we have no idea how the learner will perform in the real-world on data not previously seen (memorized).
A better idea would have been to split the existing data into training and testing sets.

### eg4

In tis example, the previous example is run and the only data outputted is two columns: want and got.
Want is the ground truth -- whether golf was played that day or not.
Got is the predicted truth -- whether the predictor thought golf would be played that day or not.
We again see that the eg3 learner is 100 percent correct due to training and testing on the same data.

### eg5

This example runs the previous one through a statistics script, ``abcd``.
The ``abcd`` script outputs a table with two rows, one for each output class (e.g. yes and no).
Again, we see that the learner is 100 percent correct.
This example expresses this correctness using classical statistics metrics such as precision and recall.

### eg6

This example trains both the j48 and jrip learners with a cross-validation script.
The cross-validation script takes in a number of randomizations, a number of folds, and a seed as the first, second, and fourth arguments, respectively.
The randomization is important to _stratify_ the dataset -- we want to ignore the (potentially arbitrary) initial ordering of the data.
As output we get the three-fold runs of each learner with the ``abcd `` script.

### eg7

This example improves on the last one by (a) doing larger cross-validations and (b) storing the data.
First, a 5x5 cross-validation is performed with j48 and jrip as the two learners, and stored in the variable ``$out``.
Next, the ``$out`` dats is searched with ``gawk`` to identify the columns 2 and 10/11; these are the learners (with parameters) and the pd (recall) and pf, respectively.
The pd and pf data are scraped into temporary output files.


### eg8

This example is the last one, but uses column names instead of column indices, increasing self-documentation.
Previously, the pd values were scraped using the line ``gawk `yes/ {print$2,$10}` $out > ${out}.pd;``, where the second and tenth indices were the learner details and pd, respectively.
Now this data is scraped more cleanly with ``columns class yes db pd < $out > ${out}.pd;``.


### eg9

This example visualizes the results from the last example.
Remember that we're running 5x5 cross-validation, so each model has a _distribution_ of 25 different parameter sets.
The ``stats.py`` script called in this example visualizes the 10, 30, 50, 70, and 90 percentiles for these model distributions.
In this particular example, all the results are relatively the same, and so the stats script ranks both j48 and jrip as 1.

### eg10

In this example, we run a 5x5 cross-validation on a larger set of learners, including the new learners nb and bnet.
nb stands for naive Bayes, and computes the posterior probability for each combination of features while assuming their independence.
In other words, naive Bayes computes how likely each outcome is for each possible assignment to the features.
Somewhat related, the bnet learner is a Bayesian network, which models the features and outcomes as a graph and computes belief propagation to predict an outcome.
Like the last example, the final output visualizes the distributions of each learner and ranks them. 
