import numpy as np
import pandas as pd
import numpy as np
import ray
import matplotlib.pyplot as plt
import itertools as it

from scipy.stats import norm, beta
from itertools import combinations


class BayesianCJ:
    def __init__(self, n_items):
        self.n_items = n_items
        self.prob_dist = {k:[] for k in range(n_items)}
        self.comparison_results = [[-1 if i >= j else [] 
                               for j in range(self.n_items)] 
                                for i in range(self.n_items)]

    def run(
        self, 
        X: list
    ):
        """Runs the Bayesian CJ algorithm, fitting the 
        parameters to the pairwise comparison data results.

        Args:
            X (list): Inputted data following a n by 3 format (a, b, winner).
        """
        @ray.remote
        def _find_expected_score_thread(
            prob_matrix, 
            each_item, 
        ):
            options = list(range(self.n_items))
            checking = each_item
            exp_result = []
            for i in range(1, self.n_items+1):
                rank_position = i
                exp_result.append(self.find_position(options, rank_position, checking, prob_matrix))

            return each_item, exp_result

        @ray.remote
        def find_expected_score(prob_matrix, prob_dist
        ):
            futures = [_find_expected_score_thread.remote(prob_matrix, each_item)
                        for each_item in range(0, self.n_items)]
            results = ray.get(futures)
            for result in results:
                prob_dist[result[0]] = result[1]

            return prob_dist

        number_of_rounds = len(X)

        for _ in range(number_of_rounds):
            a = X[_][0]
            b = X[_][1]
            winner = X[_][2]

            if a > b:
                b, a = a, b

            if winner == a:
                self.comparison_results[a][b].append(1)
            elif winner == b:
                self.comparison_results[a][b].append(0)

            if _ == 0:
                p_matrix = self.create_cdf_matrix(self.comparison_results, 
                                                  self.n_items)
            else:
                p_matrix = self.update_cdf_matrix(self.comparison_results, 
                                                  p_matrix, 
                                                  a, b)

            a = X[_][0]
            b = X[_][1]
            winner = X[_][2]

        self.prob_dist = find_expected_score.remote(p_matrix,
                                                    self.prob_dist)
        self.prob_dist = ray.get(self.prob_dist)
        self.Er_scores = [self.expected_value(range(1,self.n_items+1),
                                                 self.prob_dist[key]) 
                                                    for key in self.prob_dist.keys()]
        self.rank = np.argsort(np.array(self.Er_scores))

    
    def expected_value(
        self, 
        values, 
        weights
    ):
        """_summary_

        Args:
            values (_type_): _description_
            weights (_type_): _description_

        Returns:
            _type_: _description_
        """
        values = np.asarray(values)
        weights = np.asarray(weights)

        return (values * weights).sum() / weights.sum()


    def create_cdf_matrix(
        self, 
        data: list, 
        sample_size: int
    ):
        """_summary_

        Args:
            data (list): _description_
            sample_size (int): _description_

        Returns:
            _type_: _description_
        """
        full_matrix = [[-1 if i >= j else [] for j in range(sample_size)] for i in range(sample_size)] 
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] != -1:
                    a_prob, b_prob = self.get_CDF(data[i][j])
                    full_matrix[i][j] = a_prob
                    full_matrix[j][i] = b_prob

        return full_matrix
    

    def update_cdf_matrix(
        self, 
        data: list, 
        full_matrix: list, 
        a: int, 
        b: int
    ):
        """

        Args:
            data (list): _description_
            full_matrix (list): _description_
            a (int): _description_
            b (int): _description_

        Returns:
            _type_: _description_
        """

        a_prob, b_prob = self.get_CDF(data[a][b])
        full_matrix[a][b] = a_prob
        full_matrix[b][a] = b_prob

        return full_matrix
    

    def get_CDF(self, data):
        """
            r heads in n tosses
            See: https://en.wikipedia.org/wiki/Conjugate_prior#Table_of_conjugate_distributions
        """
        data = np.array(data)
        unique, counts = np.unique(data, return_counts=True)
        N = len(data)
        d = dict(zip(unique, counts))
        try:
            R = d[1]
        except:
            R = 0
        a = 1 # successes
        b = 1 # failures
        a_post = a + R
        b_post = b + N - R
        p_a_wins = beta.cdf(1, a=a_post, b=b_post) - beta.cdf(0.5, a=a_post, b=b_post)
        p_b_wins = 1 - p_a_wins

        return p_a_wins, p_b_wins

    
    def find_position(
        self, 
        items_ops: list, 
        n: int, 
        check_item: int, 
        data: np.ndarray
    ):
        
        items = items_ops.copy()
        number_of_items = len(items)
        items.remove(check_item)

        # Generate all combinations of winning items
        winning_items = combinations(items, n-1)

        each_prod_combination_results = []
        for each_combination in winning_items:
            # Get indices of losing items
            losing_items = np.array(list(set(range(number_of_items)) - set(each_combination) - {check_item}))

            # Compute probabilities of winning and losing items
            prob_win = 1 - np.array([data[check_item][i] for i in each_combination])
            prob_lose = np.array([data[check_item][i] for i in losing_items])

            # Compute product of probabilities
            prod_win = np.multiply.reduce(prob_win)
            prod_lose = np.multiply.reduce(prob_lose)

            # Append product of probabilities to list
            each_prod_combination_results.append(prod_win * prod_lose)

        # Compute total result using numpy's einsum() function
        total_results = np.einsum('i->', each_prod_combination_results)

        return total_results


class BayesianCJMC:
    def check(self):
        print("BayesianCJMC")


class MBayesianCJ:
    def check(self):
        print("Multi-Criterion BayesianCJMC")