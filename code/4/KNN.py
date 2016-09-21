from ../3/Table import Table
from collections import Counter

class KNN:
    def __init__(k):
        self.k = k

    def train(table):
        self.table = table

    def predict(self, row):
        """
        k-nearest neighbors: predict the mode of the closest k neighbors.
        Mode computed by arbitrarily choosing from the most common.
        """
        # Compute the k closest rows in the training table
        k_closest = sorted(list(self.table.row_distances(row)),
          key=lambda item: item.distance)[:self.k]

        # Return the most common outcome
        # Need to be careful here: Counter.most_common() is unsorted beyond
        # the actual counts. For reproducability we lexicographically sort the
        # most common items before returning one.
        initial_counts = Counter([row[-1] for row in k_closest]).most_common()
        outcomes = [initial_counts[0][0]]
        max_count = initial_counts[0][1]
        for outcome, count in initial_counts[1:]:
            if count == max_count:
                outcomes.append(outcome)
            else:
                continue
        return sorted(outcomes)[0]
