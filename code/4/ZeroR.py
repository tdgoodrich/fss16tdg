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
            actual = str(test_table.rows[i].outcomes[0]).replace("false",
              "2:false").replace("true", "1:true").replace("wine1", "1:wine1").replace("wine2", "2:wine2").replace("wine3", "3:wine3")
            predicted = str(predicted).replace("false",
              "2:false").replace("true", "1:true").replace("wine1", "1:wine1").replace("wine2", "2:wine2").replace("wine3", "3:wine3")
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
