from Table import Table
from MyTuples import Discretization
from collections import Counter
import argparse, sys

class NaiveBayes:

    def __init__(self, train_filename, discretization):
        self.seen_outcomes = set()
        self.outcome_counts = {}
        self.outcome_tables = {}
        self.train_table = Table(train_filename, discretization)
        self.train()

    def train(self):
        """
        Build tables (with individual statistics) per outcome.
        """
        for row in self.train_table.iterate_rows(features_only=False):
            for outcome in row.outcomes:
                if outcome not in self.seen_outcomes:
                    self.seen_outcomes.add(outcome)
                    self.outcome_counts[outcome] = 0
                    self.outcome_tables[outcome] = Table(discretization=Discretization(method="Handled", bins=None))
                self.outcome_counts[outcome] += 1
                self.outcome_tables[outcome].add_row(row)

        #print "Printing training table:"
        #for row in self.train_table.iterate_rows(features_only=False):
        #    print row.features, row.outcomes

        #print "Outcome tables:"
        #for outcome in self.seen_outcomes:
        #    print "  Outcome: ", outcome
        #    for row in self.outcome_tables[outcome].iterate_rows(features_only=False):
        #        print "  ", row, row.features

    def evaluate_outcome(self, row, outcome):
        """
        Computes the posterior probability of a given outcome.
        """
        result = float(self.outcome_counts.get(outcome, 0)) / sum(self.outcome_counts.itervalues())
        for feature, test_col, train_col in zip(row.features,
                                                self.outcome_tables[outcome].iterate_cols(features_only=True),
                                                self.train_table.iterate_cols(features_only=True)):
            if test_col.type == "Num":
                #print "Feature before: ", feature,
                feature = train_col.eid(feature)
                #print " Discretized feature: ", feature
            result *= test_col.bayes_evaluate(feature)
        return result

    def predict(self, row):
        """
        Choose the outcome with the highest posterior probability.
        """
        #print "Starting prediction"
        # Compute and normalize scores
        scores = [self.evaluate_outcome(row, outcome) for outcome in \
         self.seen_outcomes]
        sum_cache = sum(scores) + sys.float_info.epsilon
        scores = map(lambda x: x / sum_cache, scores)
        #print "Ending prediction"

        # Return the outcome with the highest normalized score
        return sorted(zip(self.seen_outcomes, scores), key=lambda x: x[1],
         reverse=True)[0][0]

    def output_predictions(self, testing_data):
        test_table = Table(testing_data)
        predictions = map(self.predict, test_table.rows)
        print "=== Predictions on test data ===\n"
        print "inst#".rjust(7) + "actual".rjust(7) + "predicted".rjust(11) + \
          "error prediction".rjust(18)
        for i, predicted in enumerate(predictions):
            # enumerate the outcomes:
            actual = str(test_table.rows[i].outcomes[0])
            predicted = str(predicted)
            for outcome, j in zip(self.seen_outcomes, xrange(1, len(self.seen_outcomes)+1)):
                if actual == outcome:
                    actual = str(j) + ":" + outcome
                if predicted == outcome:
                    predicted = str(j) + ":" + outcome
            print str(i+1).rjust(7) + " " + str(actual).rjust(7) +\
              " " + str(predicted).rjust(11) +\
              " " + str(int(actual==predicted)).rjust(18)

if __name__=="__main__":
    # Hardcoded outcomes
    parser = argparse.ArgumentParser()
    parser.add_argument("-train", type=str, help="Filename for the training data", required=True)
    parser.add_argument("-test", type=str, help="Filename for the testing data", required=True)
    parser.add_argument("--discretization_method", type=str, help="Discretization method")
    parser.add_argument("--discretization_bins", type=int, help="Discretization bin count")
    args = parser.parse_args()

    discretization = Discretization(method=args.discretization_method, bins=args.discretization_bins)
    nb = NaiveBayes(train_filename=args.train, discretization=discretization)
    nb.output_predictions(args.test)
