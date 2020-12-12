import random
import time
import sys


class BagList(object):
    """
    - takes memory proportional to n (total number of balls)
    - draw() takes constant time
    - reset() takes constant time
    """

    def __init__(self, *args):  # args = [a, b, c, d] => a balls of color 0, b or color 1 and so on
        self.ball_count = sum(args)
        self.balls = []
        for color, count in enumerate(args):
            self.balls.extend([color] * count)

    def draw(self):
        # does not delete from the list which would be expensive
        random_index = random.randint(0, self.ball_count - 1)
        color = self.balls[random_index]
        self.ball_count -= 1  # we will treat the list such that there are only self.ball_count elements in it
        # swap value with last index
        self.balls[random_index], self.balls[self.ball_count] = self.balls[self.ball_count], color
        return color

    # reset to original state, we would not need to create a new object for each trial this way
    def reset(self):
        self.ball_count = len(self.balls)

    def count(self):
        return self.ball_count


class BagNoList(object):
    """
    - takes memory proportional to the number of distinct colors
    - draw() takes time proportional to the number of distinct colors
    - reset() takes time proportional to the number of distinct colors

    """

    def __init__(self, *args):
        self.ball_count = sum(args)
        self.initial_ball_count_list = list(args)
        self.ball_count_list = self.initial_ball_count_list.copy()  # create a copy

    def draw(self):
        random_index = random.randint(0, self.ball_count - 1)
        self.ball_count -= 1
        for color, count in enumerate(self.ball_count_list):
            if random_index < count:
                self.ball_count_list[color] -= 1
                return color
            random_index -= count

    def reset(self):
        self.ball_count_list = self.initial_ball_count_list.copy()
        self.ball_count = sum(self.ball_count_list)

    def count(self):
        return self.ball_count


def probability_draws_match(bag, after=4, compare=2, trials=100000):
    """
    generalized version probability of `compare` number of balls matching after first drawing out `after` number of balls
    """
    assert bag.count() >= (after + compare)

    match_count = 0

    for i in range(trials):
        # throw away first 4 draws
        for j in range(after):
            bag.draw()

        next_ball = bag.draw()
        if all(bag.draw() == next_ball for k in range(compare - 1)):
            match_count += 1

        # reset for next trial
        bag.reset()

    return float(match_count) / trials  # float() to make this safe for python 2


def probability_draws_match_math(*args, compare=2):
    n = sum(args)
    assert n > (compare - 1)  # otherwise we will have infinity in denominator
    numerator = 0
    for count in args:
        f = 1
        for i in range(compare):
            f = f * (count - i)
        numerator += f
    denominator = 1
    for i in range(compare):
        denominator = denominator * (n - i)
    return float(numerator) / denominator  # float() to make this safe for python 2


def show_results_trials(bag, after=4, compare=2, trials=100000):
    start = time.time()
    prob = probability_draws_match(bag, after=after, compare=compare, trials=trials)
    end = time.time()

    print("")
    print(bag.__class__.__name__)
    print("Probability: " + str(prob))
    print("Time: " + str((end - start) * 1000) + " ms")


def show_results_bag_list(*args, after=4, compare=2):
    bag = BagList(*args)
    show_results_trials(bag, after=after, compare=compare)


def show_results_bag_no_list(*args, after=4, compare=2):
    bag = BagNoList(*args)
    show_results_trials(bag, after=after, compare=compare)


def show_results_math(*args, compare=2):
    start = time.time()
    prob = probability_draws_match_math(*args, compare=compare)
    end = time.time()

    print("")
    print("Math")
    print("Probability: " + str(prob))
    print("Time: " + str((end - start) * 1000) + " ms")


def show_results(*args, after=4, compare=2):
    show_results_bag_list(*args, after=after, compare=compare)
    show_results_bag_no_list(*args, after=after, compare=compare)
    show_results_math(*args, compare=compare)


if __name__ == "__main__":
    cmd_args = [int(a) for a in sys.argv[1:]]
    show_results(*cmd_args)
