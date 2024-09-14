from collections import deque
import numpy
import time


class ABYQueue:
    def __init__(self, maxlen, alpha=1, beta=0.1, gamma=0.001):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.queue = deque(maxlen=maxlen)

    def add(self, value):
        cur_time = time.time_ns()
        self.queue.append((cur_time, value))

    def get_prediction(self):
        if len(self.queue) == 0:
            return None

        last = numpy.array(self.queue)[numpy.array(self.queue)[:, 1] != None]

        if len(last) == 0:
            return None
        if len(last) == 1:
            return last[0][1]
        if len(last) == 2:
            (time1, value1), (time2, value2) = last
            time_diff = time2 - time1
            value_diff = value2 - value1
            trend = value_diff / time_diff
            current_time = time.time_ns()
            time_delta = current_time - time2
            next_value = value2 + trend * time_delta
            return next_value

        # Extract times and values from the queue
        times = numpy.array([t for t, v in last])
        values = numpy.array([v for t, v in last])

        # Calculate differences in time and values (velocity, acceleration trends)
        time_diffs = numpy.diff(times)
        value_diffs = numpy.diff(values)

        # Estimate current level, trend, and acceleration based on past 5 values
        level = self.alpha * values[-1] + (1 - self.alpha) * numpy.mean(values)
        trend = self.beta * value_diffs[-1] / time_diffs[-1] + (1 - self.beta) * numpy.mean(value_diffs / time_diffs)
        acceleration = self.gamma * (value_diffs[-1] - value_diffs[-2]) / (time_diffs[-1] ** 2) + \
            (1 - self.gamma) * numpy.mean(numpy.diff(value_diffs) / (time_diffs[1:] ** 2))

        # Use current time to predict the next value
        cur_time = time.time_ns()
        time_delta = cur_time - times[-1]

        # Prediction based on level, trend, and acceleration
        next_value = level + trend * time_delta + 0.5 * acceleration * (time_delta ** 2)

        return next_value
