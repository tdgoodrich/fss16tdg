from Table import Table
from collections import Counter
import argparse, sys

class NaiveBayes:

    def __init__(self, outcomes, train_filename):
        self.outcomes = outcomes
        self.outcome_counts = {}
        self.outcome_tables = {}
        for outcome in outcomes:
            self.outcome_tables[outcome] = Table()
        self.train(Table(train_filename))

    def train(self, train_table):
        """
        Build tables (with individual statistics) per outcome.
        """
        for row in train_table.iterate_rows(features_only=False):
            for outcome in row.outcomes:
                self.outcome_counts[outcome] = self.outcome_counts.get(outcome, 0) + 1
                self.outcome_tables[outcome].add_row(row)

    def evaluate_outcome(self, row, outcome):
        """
        Computes the posterior probability of a given outcome.
        """

        result = float(self.outcome_counts[outcome]) / sum(self.outcome_counts.itervalues())

        #for feature, col in zip(row.features, self.outcome_tables[outcome].iterate_cols(features_only=True)):
        #    print col.type, feature, col.bayes_evaluate(feature), "   ",
        #print ""

        for feature, col in zip(row.features, self.outcome_tables[outcome].iterate_cols(features_only=True)):
            result *= col.bayes_evaluate(feature)
        #print "Likelihood of ", outcome, ": ", result
        return result

    def predict(self, row):
        """
        Choose the outcome with the highest posterior probability.
        """

        # Compute and normalize scores
        scores = [self.evaluate_outcome(row, outcome) for outcome in \
         self.outcomes]
        sum_cache = sum(scores) + sys.float_info.epsilon
        scores = map(lambda x: x / sum_cache, scores)

        # Return the outcome with the highest normalized score
        return sorted(zip(self.outcomes, scores), key=lambda x: x[1],
         reverse=True)[0][0]

    def output_predictions(self, testing_data):
        test_table = Table(testing_data)
        predictions = map(self.predict, test_table.rows)
        print "=== Predictions on test data ===\n"
        print "inst#".rjust(7) + "actual".rjust(7) + "predicted".rjust(11) + \
          "error prediction".rjust(18)
        for i, predicted in zip(xrange(len(predictions)), predictions):
            actual = str(test_table.rows[i].outcomes[0]).replace("false",
              "2:false").replace("true", "1:true")
            predicted = str(predicted).replace("false",
              "2:false").replace("true", "1:true")
            print str(i+1).rjust(7) + " " + str(actual).rjust(7) +\
              " " + str(predicted).rjust(11) +\
              " " + str(int(actual==predicted)).rjust(18)

if __name__=="__main__":
    # Hardcoded outcomes
    parser = argparse.ArgumentParser()
    parser.add_argument("-train", type=str, help="Filename for the training data", required=True)
    parser.add_argument("-test", type=str, help="Filename for the testing data", required=True)
    args = parser.parse_args()
    nb = NaiveBayes(outcomes=["true", "false"], train_filename=args.train)
    nb.output_predictions(args.test)
