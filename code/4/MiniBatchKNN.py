from Table import Table, Sym, Num
import argparse, copy, random, sys

class Centroid:
    def __init__(self, index, row):
        self.index = index
        self.features = copy.deepcopy(row.features)
        self.outcomes = copy.deepcopy(row.outcomes)

    def __iter__(self):
        for item in self.features:
            yield item
        for item in self.outcomes:
            yield item

class MiniBatchKNN:

    def __init__(self, k_nearest, k_means, train_filename, seed=42):
        self.k_nearest = k_nearest
        self.k_means = k_means
        random.seed(seed)
        self.centroid_table = Table()
        self.centroid_clusters = {}
        self.train(Table(train_filename))

    def train(self, train_table, batch_size = 100, iterations = None):
        """
        Identify k clusters using mini-batch k-means.
        """
        # initialize variables
        if iterations == None:
            iterations = train_table.size() / batch_size + 1
        rows = train_table.iterate_rows(features_only=False)

        # Store the centroids in a Table.
        # Centroids are rows + an index.
        # The index is used to look up the centroid's cluster,
        # which is stored in its own Table.
        for i in xrange(self.k_means):
            next_row = next(rows)
            centroid = Centroid(index=i, row=next(rows))
            self.centroid_table.add_row(centroid)
            self.centroid_clusters[i] = Table()
            self.centroid_clusters[i].add_row(centroid)

        for _ in xrange(iterations):
            # Read in the new batch
            centroid_cache = {}
            batch = []
            for _ in xrange(batch_size):
                try:
                    batch.append(next(rows))
                except:
                    break

            # Cache the centroid
            for row in batch:
                centroid_cache[row] = self.centroid_table.closest(row)

            # Update the centroids with this assignment
            for row in centroid_cache:
                centroid = centroid_cache[row]
                current_cluster = self.centroid_clusters[centroid.index]
                current_cluster.add_row(row)
                learning_rate = 1.0/current_cluster.size()
                self.update_centroid(centroid, row,
                  train_table.iterate_cols(features_only=True), learning_rate)

    def update_centroid(self, centroid, row, cols, learning_rate):
        new_features = []
        for original, new, col in zip(centroid.features, row.features, cols):
            if col.type == "Num":
                new_features.append((1.0-learning_rate) * original + \
                  learning_rate * new)
            elif col.type == "Sym":
                new_features.append(new if learning_rate < random.rand() else \
                  old)
        centroid.features = new_features

    def predict(self, row):
        """
        Find the closest centroid, then find the closest k-items in its cluster.
        """

        closest_centroid = self.centroid_table.closest(row)
        closest_cluster = self.centroid_clusters[closest_centroid.index]

        k_closest = sorted(list(closest_cluster.row_distances(row)),
          key=lambda item: item.distance)[:self.k_nearest]

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
            for outcome, i in zip(self.seen_outcomes, xrange(1, len(self.seen_outcomes)+1)):
                if actual == outcome:
                    actual = str(i) + ":" + outcome
                if predicted == outcome:
                    predicted = str(i) + ":" + outcome
            print str(i+1).rjust(7) + " " + str(actual).rjust(7) +\
              " " + str(predicted).rjust(11) +\
              " " + str(int(actual==predicted)).rjust(18)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-train", type=str,
      help="Filename for the training data", required=True)
    parser.add_argument("-test", type=str,
      help="Filename for the testing data", required=True)
    args = parser.parse_args()
    learner = MiniBatchKNN(k_nearest=1, k_means=20, train_filename=args.train)
    learner.output_predictions(args.test)
