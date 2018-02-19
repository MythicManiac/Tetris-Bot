import numpy as np
import tensorflow as tf


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

    def __init__(self, feature_count, level_width, level_height, action_count,
                 checkpoint_path, epsilon=0.1, learning_rate=1e-4):
        assert level_width % 2 == 0
        assert level_height % 2 == 0
        assert level_width / 2 % 2 == 0
        assert level_height / 2 % 2 == 0
        self.feature_count = feature_count
        self.level_width = level_width
        self.level_height = level_height
        self.action_count = action_count
        self.checkpoint_path = checkpoint_path
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.build()
        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.config.gpu_options.per_process_gpu_memory_fraction = 0.2
        self.session = tf.Session(config=self.config)
        self.session.run(tf.global_variables_initializer())
        tf.summary.FileWriter("logs/", self.session.graph)

    def build(self):
        self.network_input = tf.placeholder(
            tf.float32,
            shape=[None, self.level_width, self.level_height, self.feature_count],
            name="GameState"
        )

        # First layer
        W_conv1 = _weight_variable([2, 2, self.feature_count, 16])
        b_conv1 = _bias_variable([16])

        # First pool
        h_conv1 = tf.nn.relu(_conv2d(self.network_input, W_conv1) + b_conv1)
        h_pool1 = _max_pool_2x2(h_conv1)  # This halves the size, so output is [width / 2, height / 2]

        # Second layer
        W_conv2 = _weight_variable([2, 2, 16, 32])
        b_conv2 = _bias_variable([32])

        # Second pool
        h_conv2 = tf.nn.relu(_conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = _max_pool_2x2(h_conv2)

        # Densely connected layer
        neurons = 128
        flat_neurons = int(self.level_width / 2 / 2) * int(self.level_height / 2 / 2) * 32
        W_fc1 = _weight_variable([flat_neurons, neurons])
        b_fc1 = _bias_variable([neurons])

        h_pool2_flat = tf.reshape(h_pool2, [-1, flat_neurons])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        # Output layer
        output_count = 4
        W_fc2 = _weight_variable([neurons, output_count])
        b_fc2 = _bias_variable([output_count])

        self.network_output = tf.matmul(h_fc1, W_fc2) + b_fc2
        self.action = tf.argmax(self.network_output, 1)

        # Loss & train
        self.target = tf.placeholder(tf.float32, [None, output_count], name="Target")
        error = tf.reduce_sum(tf.square(self.network_output - self.target))
        L2_norm = tf.reduce_sum(tf.square(b_fc1)) + tf.reduce_sum(tf.square(b_fc2))
        L2_norm += tf.reduce_sum(tf.square(W_fc1)) + tf.reduce_sum(tf.square(W_fc2))
        self.loss = error + L2_norm * 1e-6

        self.train = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)

        correct_prediction = tf.equal(self.action, tf.argmax(self.target, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    def learn(self, old_state, action, reward, new_state, Q_base):
        gamma = 0.99
        old_state = old_state[np.newaxis, :]
        new_state = new_state[np.newaxis, :]

        Q = self.session.run(
            self.network_output,
            feed_dict={
                self.network_input: new_state,
            }
        )
        Q_target = Q_base
        Q_target[0, action] = reward + gamma * np.max(Q)

        # Train
        self.session.run(
            self.train,
            feed_dict={
                self.network_input: old_state,
                self.target: Q_target
            }
        )

    def choose_action(self, observation):
        observation = observation[np.newaxis, :]

        network_output, action = self.session.run(
            [self.network_output, self.action],
            feed_dict={
                self.network_input: observation,
            },
        )
        if np.random.rand(1) < self.epsilon:
            action = np.random.randint(0, self.action_count)

        return action, network_output

    def save(self):
        saver = tf.train.Saver()
        save_path = saver.save(self.session, self.checkpoint_path)
        print("Saved parameters to %s" % save_path)

    def load(self):
        saver = tf.train.Saver()
        if tf.train.checkpoint_exists(self.checkpoint_path):
            saver.restore(self.session, self.checkpoint_path)
            print("Loaded model")
            return True
        else:
            print("No checkpoints found, initializing new model")
            return False
