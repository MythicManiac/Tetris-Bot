import numpy as np


class Random(object):

    def __init__(self, random_seed):
        self.random = np.random.RandomState(random_seed)

    def choice(self, choises):
        return choises[self.random.choice(len(choises))]
