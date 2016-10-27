from Table import Table
from collections import Counter
import argparse

class KNN:
    def __init__(self, k, training_data):
        self.k = k
        self.table = Table(training_data)

    def predict(self, row):
        """
        k-nearest neighbors: predict the mode of the closest k neighbors.
        Mode computed by arbitrarily choosing from the most common.
        """
        # Compute the k closest rows in the training table
        k_closest = sorted(list(self.table.row_distances(row)),
          key=lambda item: item.distance)[:self.k]

        frequencies = {}
        for row in k_closest:
            outcome = row.row.outcomes[0] # Assuming one outcome
            frequencies[outcome] = frequencies.get(outcome, 0) + 1
        return max(frequencies, key=frequencies.get)

    def output_predictions(self, testing_data):
        test_table = Table(testing_data)
        predictions = map(self.predict, test_table.rows)
        print "=== Predictions on test data ===\n"
        print "inst#".rjust(7) + "actual".rjust(7) + "predicted".rjust(11) + \
          "error prediction".rjust(18)
        for i, predicted in zip(xrange(len(predictions)), predictions):
            # enumerate the outcomes:
            actual = str(test_table.rows[i].outcomes[0])
            predicted = str(predicted)
            outcomes = test_table.cols.outcomes[0].counts.keys()
            for outcome, i in zip(outcomes, xrange(1, len(outcomes)+1)):
                if actual == outcome:
                    actual = str(i) + ":" + outcome
                if predicted == outcome:
                    predicted = str(i) + ":" + outcome
            print str(i+1).rjust(7) + " " + str(actual).rjust(7) +\
              " " + str(predicted).rjust(11) +\
              " " + str(int(actual==predicted)).rjust(18)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-train", type=str, help="Filename for the training data", required=True)
    parser.add_argument("-test", type=str, help="Filename for the testing data", required=True)
    args = parser.parse_args()
    knn = KNN(k=1, training_data=args.train)
    knn.output_predictions(args.test)
