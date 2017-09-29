import functools
import tensorflow as tf
import numpy as np
import time


def lazy_property(function):
    attribute = '_' + function.__name__

    @property
    @functools.wraps(function)
    def wrapper(self):
        if not hasattr(self, attribute):
            setattr(self, attribute, function(self))
        return getattr(self, attribute)

    return wrapper


class SequenceClassification:
    def __init__(self, data, target, dropout=0.2, num_hidden=200, num_layers=2):
        self.data = data
        self.target = target
        self.dropout = dropout
        self._num_hidden = num_hidden
        self._num_layers = num_layers
        self.prediction
        self.prediction_label
        self.cost
        self.optimize
        self.error
        self.confusion_matrix

    def rnn_cell(self):
        cell = tf.contrib.rnn.LSTMCell(self._num_hidden)  # GRUCell/LSTMCell
        cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=1.0-self.dropout)
        return cell

    @lazy_property
    def prediction(self):
        # Recurrent network.
        # network = tf.contrib.rnn.LSTMCell(self._num_hidden)
        # network = tf.contrib.rnn.DropoutWrapper(network, output_keep_prob=self.dropout)
        network = tf.contrib.rnn.MultiRNNCell([self.rnn_cell() for _ in range(self._num_layers)])
        output, _ = tf.nn.dynamic_rnn(network, self.data, dtype=tf.float32)
        # Select last output.
        output = tf.transpose(output, [1, 0, 2])
        last = tf.gather(output, int(output.get_shape()[0]) - 1)
        # Softmax layer.
        # weight, bias = self._weight_and_bias(self._num_hidden, int(self.target.get_shape()[1]))
        # prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)
        out_size = self.target.get_shape()[1].value
        # logit = tf.contrib.layers.fully_connected(last, out_size, activation_fn=None)
        logit = tf.layers.dense(last, out_size)
        prediction = tf.nn.softmax(logit)
        return prediction

    @lazy_property
    def prediction_label(self):
        return tf.argmax(self.prediction, 1)

    @lazy_property
    def cost(self):
        cross_entropy = -tf.reduce_sum(self.target * tf.log(self.prediction))
        return cross_entropy

    @lazy_property
    def optimize(self):
        learning_rate = 0.1  # 0.001
        optimizer = tf.train.AdadeltaOptimizer(learning_rate)  # AdadeltaOptimizer,RMSPropOptimizer
        return optimizer.minimize(self.cost)

    @lazy_property
    def error(self):
        mistakes = tf.not_equal(tf.argmax(self.target, 1), tf.argmax(self.prediction, 1))
        return tf.reduce_mean(tf.cast(mistakes, tf.float32))

    @lazy_property
    def confusion_matrix(self):
        cm = tf.confusion_matrix(tf.argmax(self.target, 1), tf.argmax(self.prediction, 1), int(self.target.get_shape()[1]))
        return cm

    @staticmethod
    def _weight_and_bias(in_size, out_size):
        weight = tf.truncated_normal([in_size, out_size], stddev=0.01)
        bias = tf.constant(0.1, shape=[out_size])
        return tf.Variable(weight), tf.Variable(bias)


def get_csv_data(source, size):
    filename_queue = tf.train.string_input_producer([source])
    # reader = tf.TableRecordReader()
    reader = tf.TextLineReader()
    features = None
    labels = None
    for i in range(size):
        key, value = reader.read(filename_queue)
        record_defaults = [[''], [''], ['']]
        user_id, travel_by_air_history, max_travel_by_air_in7days = tf.decode_csv(value, record_defaults=record_defaults)
        str_travel_by_air_historys = tf.string_split([travel_by_air_history], '>')
        # tf.sparse_reorder(str_travel_by_air_historys)
        num_travel_historys = tf.string_to_number(str_travel_by_air_historys.values, out_type=tf.float32)
        num_max_travel_level_in7days = tf.string_to_number(max_travel_by_air_in7days, out_type=tf.int32)
        if features is None:
            features = [num_travel_historys]
        else:
            features = tf.concat([features, [num_travel_historys]], 0)
        if labels is None:
            labels = [num_max_travel_level_in7days]
        else:
            labels = tf.concat([labels, [num_max_travel_level_in7days]], 0)

    return features, labels


# user_id,binary_sequence(fixed sequence length),class
# 1,1>0>1>1>0>0>0>0>...>0,1
# 2,0>1>0>1>0>0>0>0>...>0,0
# ...
# 99,0>1>0>1>0>0>0>0>...>0,0

def print_tf_vars(tf_sess, names):
    variables_names = [v.name for v in tf.trainable_variables()]
    values = tf_sess.run(variables_names)
    for k, v in zip(variables_names, values):
        if names is None or names.find(k) >= 0:
            print(k, v)


def main():
    num_classes = 3
    num_sequence = 120
    num_feature = 1

    num_epoch = 1
    batch_size = 100
    num_iteration_train = 10000
    num_iteration_valid = 10
    num_iteration_test = 100
    num_iteration_show = 100

    train_file = "tf_train.csv"
    test_file = "tf_test.csv"

    data = tf.placeholder(tf.float32, [None, num_sequence, num_feature])
    target = tf.placeholder(tf.float32, [None, num_classes])
    # dropout = tf.placeholder(tf.float32)
    model = SequenceClassification(data, target)  # , dropout

    train_feature_batch, train_label_batch = get_csv_data(train_file, batch_size)
    train_label_batch = tf.one_hot(train_label_batch, num_classes)

    test_feature_batch, test_label_batch = get_csv_data(test_file, batch_size)
    test_label_batch = tf.one_hot(test_label_batch, num_classes)

    with tf.Session() as sess:
        # Start populating the filename queue.
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        sess.run(tf.global_variables_initializer())

        for epoch in range(num_epoch):
            for iteration in range(num_iteration_train):
                _train_feature_batch, _train_label_batch = sess.run([train_feature_batch, train_label_batch])
                _train_feature_batch2 = np.reshape(_train_feature_batch, (batch_size, num_sequence, num_feature))
                sess.run(model.optimize, {data: _train_feature_batch2, target: _train_label_batch})
                if iteration % num_iteration_show == 0:
                    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    loss = sess.run(model.cost, {data: _train_feature_batch2, target: _train_label_batch})
                    error_sum = 0.0
                    # predict = sess.run(model.prediction, {data: _train_feature_batch2, target: _train_label_batch})
                    for iteration_v in range(num_iteration_valid):
                        _test_feature_batch, _test_label_batch = sess.run([test_feature_batch, test_label_batch])
                        _test_feature_batch2 = np.reshape(_test_feature_batch, (batch_size, num_sequence, num_feature))
                        error_sum += sess.run(model.error, {data: _test_feature_batch2, target: _test_label_batch})
                    error_batch = error_sum / num_iteration_valid
                    print('{:s}: iteration:{:2d} loss:{:f} accuracy:{:f}'.format(now_time, iteration + 1, loss, 1 - error_batch))
                    # print_tf_vars(sess, "u'rnn/multi_rnn_cell/cell_1/gru_cell/candidate/weights:0'")
                    # print_tf_vars(sess, "u'rnn/multi_rnn_cell/cell_3/lstm_cell/weights:0")

            print('Epoch:{:d} training finished with {:d} iterations'.format(epoch + 1, iteration + 1))
            error_sum = 0.0
            cm = None
            for iteration_t in range(num_iteration_test):
                _test_feature_batch, _test_label_batch = sess.run([test_feature_batch, test_label_batch])
                _test_feature_batch2 = np.reshape(_test_feature_batch, (batch_size, num_sequence, num_feature))
                error_sum += sess.run(model.error, {data: _test_feature_batch2, target: _test_label_batch})
                # predict = sess.run(model.prediction, {data: _test_feature_batch2, target: _test_label_batch})
                _cm = sess.run(model.confusion_matrix, {data: _test_feature_batch2, target: _test_label_batch})
                if cm is None:
                    cm = _cm
                else:
                    cm = np.add(cm, _cm)
            error_batch = error_sum / num_iteration_test
            print('{:s}: accuracy:{:f} confusion_matrix: '.format(now_time, 1 - error_batch))
            print(np.matrix(cm))

        coord.request_stop()
        coord.join(threads)


if __name__ == '__main__':
    main()
