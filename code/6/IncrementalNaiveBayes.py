from Table import Table
from AnomalyDataGenerator import AnomalyDataGenerator
from collections import Counter
import argparse, sys

class IncrementalNaiveBayes:

    def __init__(self):
        self.seen_outcomes = set()
        self.outcome_counts = {}
        self.outcome_tables = {}

    def incremental_train(self, batch):
        """
        Build tables (with individual statistics) per outcome.
        """
        for row in batch.iterate_rows(features_only=False):
            for outcome in row.outcomes:
                if outcome not in self.seen_outcomes:
                    self.seen_outcomes.add(outcome)
                    self.outcome_counts[outcome] = 0
                    self.outcome_tables[outcome] = Table()
                self.outcome_counts[outcome] = self.outcome_counts[outcome] + 1
                self.outcome_tables[outcome].add_row(row)

    def evaluate_outcome(self, row, outcome):
        """
        Computes the posterior probability of a given outcome.
        """

        result = float(self.outcome_counts.get(outcome, 0)) / sum(self.outcome_counts.itervalues())
        # print "Initial result: ", self.outcome_counts.get(outcome, 0), sum(self.outcome_counts.itervalues())
        for feature, col in zip(row.features, self.outcome_tables[outcome].iterate_cols(features_only=True)):
            # print "Next eval: ", col.bayes_evaluate(feature)
            result *= col.bayes_evaluate(feature)
        return result

    def predict(self, row):
        """
        Choose the outcome with the highest posterior probability.
        """

        # Compute and normalize scores
        scores = [self.evaluate_outcome(row, outcome) for outcome in \
         self.seen_outcomes]
        # print "original scores:\n", scores
        sum_cache = sum(scores) + sys.float_info.epsilon
        scores = map(lambda x: x / sum_cache, scores)
        # print "normalized scores:\n", scores

        # Return the outcome with the highest normalized score
        return sorted(zip(self.seen_outcomes, scores), key=lambda x: x[1],
         reverse=True)[0][0]

    def output_predictions(self, test_table):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-dataset", type=str,
      help="Filename for the training data", required=True)
    args = parser.parse_args()
    generator = AnomalyDataGenerator(args.dataset)
    nb = IncrementalNaiveBayes()

    batch = generator.generate_era(0)
    nb.incremental_train(batch)
    for era in xrange(1, 20):
        print "\n*** Era ", era, " ***"
        batch = generator.generate_era(era)
        nb.output_predictions(batch)
        nb.incremental_train(batch)
