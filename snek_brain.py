import numpy as np
import tensorflow as tf


def _weight(shape, name):
    return tf.Variable(tf.random_normal(shape, stddev=0.35), name=name)


def _bias(shape, name):
    return tf.Variable(tf.zeros(shape), name=name)


def _weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def _bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def _conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def _max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


class SnakeNetwork(object):

    def __init__(self, feature_count, level_width, level_height, action_count):
        assert level_width % 2 == 0
        assert level_height % 2 == 0
        self.feature_count = feature_count
        self.level_width = level_width
        self.level_height = level_height
        self.action_count = action_count
        self.build()
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        tf.summary.FileWriter("logs/", self.session.graph)

    def build(self):
        self.network_input = tf.placeholder(
            tf.float32,
            shape=[None, self.level_width, self.level_height, self.feature_count]
        )

        # First layer
        W_conv1 = _weight_variable([5, 5, self.feature_count, 32])
        b_conv1 = _bias_variable([32])

        # First pool
        h_conv1 = tf.nn.relu(_conv2d(self.network_input, W_conv1) + b_conv1)
        h_pool1 = _max_pool_2x2(h_conv1)  # This halves the size, so output is [width / 2, height / 2]

        # Densely connected layer
        neurons = 128
        flat_neurons = int(self.level_width / 2) * int(self.level_height / 2) * 32
        W_fc1 = _weight_variable([flat_neurons, neurons])
        b_fc1 = _bias_variable([neurons])

        h_pool1_flat = tf.reshape(h_pool1, [-1, flat_neurons])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)

        # Dropout layer
        self.keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

        # Output layer
        output_count = 4
        W_fc2 = _weight_variable([128, output_count])
        b_fc2 = _bias_variable([output_count])

        self.network_output = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

    def store_transition(self, old_state, action, reward, new_state):
        pass

    def choose_action(self, observation):
        observation = observation[np.newaxis, :]

        network_output = self.session.run(
            self.network_output,
            feed_dict={
                self.network_input: observation,
                self.keep_prob: 1.0,
            },
        )
        action = np.argmax(network_output)
        return action

    def learn(self):
        pass
