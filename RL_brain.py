# import numpy as np
import tensorflow as tf


def _weight(shape, name):
    return tf.Variable(tf.random_normal(shape, stddev=0.35), name=name)


def _bias(shape, name):
    return tf.Variable(tf.zeros(shape), name=name)


class SnakeNetwork:

    def __init__(self, feature_count, level_width, level_height, action_count):
        self.feature_count = feature_count
        self.level_width = level_width
        self.level_height = level_height
        self.action_count = action_count
        self.build()

    def real_build(self):
        pass
        # body_map, head_map, future_head_map, cherry_map = tf.split(
        #     axis=0,
        #     num_or_size_splits=4,
        #     value=[]
        # )

    def build(self):
        # Network input
        networkstate = tf.placeholder(tf.float32, [None, self.feature_count], name="input")
        networkaction = tf.placeholder(tf.int32, [None], name="actioninput")
        networkreward = tf.placeholder(tf.float32, [None], name="groundtruth_reward")
        action_onehot = tf.one_hot(networkaction, self.action_count, name="actiononehot")

        # The variable in our network:
        w1 = _weight([self.feature_count, 16], name="W1")
        w2 = _weight([16, 32], name="W2")
        w3 = _weight([32, 8], name="W3")
        w4 = _weight([8, self.action_count], name="W4")
        b1 = _bias([16], name="B1")
        b2 = _bias([32], name="B2")
        b3 = _bias([8], name="B3")
        b4 = _bias(self.action_count, name="B4")

        # The network layout
        layer1 = tf.nn.relu(tf.add(tf.matmul(networkstate, w1), b1), name="Result1")
        layer2 = tf.nn.relu(tf.add(tf.matmul(layer1, w2), b2), name="Result2")
        layer3 = tf.nn.relu(tf.add(tf.matmul(layer2, w3), b3), name="Result3")
        predictedreward = tf.add(tf.matmul(layer3, w4), b4, name="predictedReward")

        # Learning
        self.qreward = tf.reduce_sum(tf.multiply(predictedreward, action_onehot), reduction_indices=1)
        self.loss = tf.reduce_mean(tf.square(networkreward - self.qreward))
        tf.summary.scalar('loss', self.loss)
        self.optimizer = tf.train.RMSPropOptimizer(0.0001).minimize(self.loss)
        self.merged_summary = tf.summary.merge_all()

    def store_transition(self, old_state, action, reward, new_state):
        pass

    def choose_action(self, observation):
        pass

    def learn(self):
        pass
