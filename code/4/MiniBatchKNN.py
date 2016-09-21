from ../3/Table import Table
import sys

class MiniBatchKNN:
    class Centroid:
        def __init__(self, index, features):
            self.index = index
            self.features = features
            self.count = 1

    def __init__(self, k):
        self.k = k

    def train(table, batch_size = 100, iterations = None):
        """
        Identify k clusters using mini-batch k-means.
        """
        # initialize variables
        if iterations == None:
            iterations = table.size() / batch_size
        data = table.row_generator()
        for i in xrange(k):
            self.centroids = [Centroid(index=i, features=next(data))]

        for _ in xrange(iterations):
            # Read in the new batch
            centroid_cache = {}
            batch = []
            for _ in xrange(batch_size):
                try:
                    batch.append(next(data))
                except:
                    continue

            # Find the centroid assignments
            for item in batch:
                centroid_cache[item] = closest_centroid(table, item).index

            # Update the centroids with this assignment
            for item in centroid_cache:
                centroid = self.centroids[id]
                centroid.counts += 1
                learning_rate = 1.0/centroid.counts
                update_centroid(index, learning_rate, item)

    def closest_centroid(self, table, item):
        closest, min_dist = None, sys.maxint
        for centroid in self.centroids:
            dist = table.row_distance(centroid.features, item)
            if dist < min_dist:
                closest, min_dist = centroid, dist
        return closest

    def update_centroid(self, centroid, learning_rate, item):
        new_features = []
        for col_item1, col_item2, col in zip(centroid.features, item,
          table.col_generator):
            if type(col) == Sym:
                if learning_rate < random.rand():
                    new_features.append(col_item2)
                else:
                    new_features.append(col_item1)
            elif type(col) == Num:
                new_features.append((1-learning_rate) * col_item1 +
                  learning_rate * col_item2)
        centroid.features = new_features

    def predict(self, row):
        """
        Using the k-means clusters, look up the closest cluster and predict the mode of the closest k items.
        """
