import argparse, collections, itertools, math
from Table import Table

def square_distance(a, b):
    s = 0
    for x, y in itertools.izip(a, b):
        d = x - y
        s += d * d
    return s

Node = collections.namedtuple("Node", 'point axis label left right')

class KDTreeKNN(object):
    """A tree for nearest neighbor search in a k-dimensional space.

    For information about the implementation, see
    http://en.wikipedia.org/wiki/Kd-tree

    Usage:
    objects is an iterable of (point, label) tuples
    we're using the label to store our outcomes
    k is the number of dimensions

    t = KDTree(k, objects)
    point, label, distance = t.nearest_neighbor(destination)
    """

    def __init__(self, k, train_filename):
        self.k = k
        rows = Table(train_filename)
        self.root = self.train([(row.features, row.outcomes) for row in \
          rows.iterate_rows(features_only=False)])

    def train(self, objects, axis=0):
        if not objects:
            return None

        objects.sort(key=lambda o: o[0][axis])
        median_idx = len(objects) // 2
        with open("debug.txt", "w") as outfile:
            outfile.write(str(objects) + "   median_idx: " + str(median_idx))
        median_point, median_label = objects[median_idx]

        next_axis = (axis + 1) % self.k
        return Node(median_point, axis, median_label,
                    self.train(objects[:median_idx], next_axis),
                    self.train(objects[median_idx + 1:], next_axis))

    def nearest_neighbor(self, destination):

        best = [None, None, float('inf')]
        # state of search: best point found, its label,
        # lowest squared distance

        def recursive_search(here):

            if here is None:
                return
            point, axis, label, left, right = here

            here_sd = square_distance(point, destination)
            if here_sd < best[2]:
                best[:] = point, label, here_sd

            diff = destination[axis] - point[axis]
            close, away = (left, right) if diff <= 0 else (right, left)

            recursive_search(close)
            if diff ** 2 < best[2]:
                recursive_search(away)

        recursive_search(self.root)
        return best[0], best[1], math.sqrt(best[2])

    def predict(self, row):
        """
        Look up the closest point and take its outcome.
        """
        featues, outcomes, dist = self.nearest_neighbor(row.features)
        return outcomes[0]

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
              " " + str(int(actual==predicted)).rjust(18)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-train", type=str,
      help="Filename for the training data", required=True)
    parser.add_argument("-test", type=str,
      help="Filename for the testing data", required=True)
    args = parser.parse_args()
    learner = KDTreeKNN(k=20, train_filename=args.train)
    learner.output_predictions(args.test)
