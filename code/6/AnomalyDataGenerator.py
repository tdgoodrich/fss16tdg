from Table import Table
import argparse, random

class AnomalyDataGenerator:

    def __init__(self, filename, seed=42):
        """
        filename is the path to a dataset with at least 3 classes.
        Populates self.outcomes and self.outcome_tables
        """
        random.seed(seed)

        # Build Tables per outcome
        full_data = Table(filename)
        seen_outcomes = set()
        self.outcome_tables = {}
        for row in full_data.iterate_rows(features_only=False):
            outcome = row.outcomes[0]
            if outcome not in seen_outcomes:
                seen_outcomes.add(outcome)
                self.outcome_tables[outcome] = Table()
            self.outcome_tables[outcome].add_row(row)

        # Take three of the most common outcomes
        most_popular = sorted([(outcome, self.outcome_tables[outcome].size()) \
        for outcome in seen_outcomes], key=lambda x: x[1], reverse=True)

        for x in most_popular[3:]:
            self.outcome_tables.pop(x[0])

        self.outcomes = sorted(x[0] for x in most_popular[:3])


    def __iter__(self):
        for _ in xrange(100):
            rand = random.random()
            if rand < 0.5:
                outcome = self.outcomes[0]
            else:
                outcome = self.outcomes[1]
            yield random.choice(self.outcome_tables[outcome].rows)

        print "\nBREAAAAAAKKKK\n\n"

        for _ in xrange(100):
            rand = random.random()
            if rand < 0.1:
                outcome = self.outcomes[0]
            elif rand < 0.4:
                outcome = self.outcomes[1]
            else:
                outcome = self.outcomes[2]
            yield random.choice(self.outcome_tables[outcome].rows)

# if __name__=="__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-dataset", type=str,
#       help="Filename for the training data", required=True)
#     args = parser.parse_args()
#     generator = AnomalyDataGenerator(args.dataset)
#     for x in generator:
#         print x.outcomes
