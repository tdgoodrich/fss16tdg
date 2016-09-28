import argparse
from Table import Table

class ZeroR:
    def __init__(self, training_data):
        self.table = Table(training_data)

    def predict(self, row):
        # Return the most common outcome
        return self.table.cols[-1].mode

    def output_predictions(self, testing_data):
        table = Table(testing_data)
        predictions = map(self.predict, table.rows)
        SPACING = 15
        print "=== Predictions on test data ===\n"
        print "inst#".rjust(7) + "actual".rjust(7) + "predicted".rjust(11) + "error prediction".rjust(18)
        for i, predicted in zip(xrange(len(predictions)), predictions):
            actual = table.rows[i][-1].replace("false","2:false").replace("true", "1:true")
            predicted = predicted.replace("false","2:false").replace("true", "1:true")
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
