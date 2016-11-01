from Table import Table
from AnomalyDataGenerator import AnomalyDataGenerator
import argparse, math, sys

class IncrementalNaiveBayes:

    def __init__(self, outcomes):
        self.outcomes = outcomes
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
                self.outcome_counts[outcome] += 1
                self.outcome_tables[outcome].add_row(row)

    def evaluate_outcome(self, row, outcome):
        """
        Computes the posterior probability of a given outcome.
        """

        result = float(self.outcome_counts.get(outcome, 0)) / sum(self.outcome_counts.itervalues())
        for feature, col in zip(row.features, self.outcome_tables[outcome].iterate_cols(features_only=True)):
            result *= col.bayes_evaluate(feature)
        return result

    def predict(self, row):
        """
        Choose the outcome with the highest posterior probability.
        """

        # Compute and normalize scores
        scores = [self.evaluate_outcome(row, outcome) for outcome in \
         self.seen_outcomes]
        sum_cache = sum(scores) + sys.float_info.epsilon
        scores = map(lambda x: x / sum_cache, scores)

        # Return the outcome with the highest normalized score
        return sorted(zip(self.seen_outcomes, scores), key=lambda x: x[1],
         reverse=True)[0]

    def output_predictions(self, test_table):
        predictions = map(self.predict, test_table.rows)

        for desired_outcome in self.outcomes:
            b, d = 0, 0
            for outcome, actual in zip([x[0] for x in predictions], test_table.iterate_rows(features_only=False)):
                if actual.outcomes[0] == desired_outcome:
                    if outcome == desired_outcome:
                        d += 1
                    else:
                        b += 1
            print desired_outcome, " recall: ", float(d) / (b + d + sys.float_info.epsilon)
        # return the log of the likelihoods
        return [math.log(x[1]) for x in predictions]


# Adapted from timm's dotninja stats.py
def a12(list1, list2):
    more = same = 0.0
    for x in sorted(list1):
        for y in sorted(list2):
            if   x==y :
                same += 1
            elif x > y :
                more += 1
    return (more + 0.5*same) / (len(list1)*len(list2))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dataset", type=str,
      help="Filename for the training data", required=True)
    args = parser.parse_args()
    generator = AnomalyDataGenerator(args.dataset)
    nb = IncrementalNaiveBayes(outcomes=["wine1", "wine2", "wine3"])

    batch = generator.generate_era(0)
    nb.incremental_train(batch)
    old_likelihood = None
    old_a12_score = None
    for era in xrange(1, 21):
        print "\n*** Era ", era, " ***"
        batch = generator.generate_era(era)
        likelihood = nb.output_predictions(batch)
        if old_likelihood is not None:
            a12_score = a12(likelihood, old_likelihood)
            print "a12: ", a12_score
            if old_a12_score is not None and math.fabs(old_a12_score - a12_score) > 0.2 * old_a12_score:
                print "a12 score different by >20%, ANOMALY DETECTED!!"
            old_a12_score = a12_score
        old_likelihood = likelihood
        nb.incremental_train(batch)
