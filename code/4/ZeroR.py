import argparse
from Table import Table

class ZeroR:
    def __init__(self, training_data):
        self.table = Table(training_data)

    def predict(self, row):
        # Return the most common outcome
        # Assumes only one outcome
        return self.table.cols.outcomes[0].mode

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
            for outcome, i in zip(self.seen_outcomes, xrange(1, len(self.seen_outcomes)+1)):
                if actual == outcome:
                    actual = str(i) + ":" + outcome
                if predicted == outcome:
                    predicted = str(i) + ":" + outcome
            print str(i+1).rjust(7) + " " + str(actual).rjust(7) +\
              " " + str(predicted).rjust(11) +\
              " " + str(actual==predicted).rjust(18)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-train", type=str, help="Filename for the training data", required=True)
    parser.add_argument("-test", type=str, help="Filename for the testing data", required=True)
    args = parser.parse_args()
    zeror = ZeroR(args.train)
    zeror.output_predictions(args.test)
