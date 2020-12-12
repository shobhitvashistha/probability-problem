import random
import time
import sys


RED = 0
GREEN = 1
BLUE = 2


class BagList(object):
    """
    Could be generalized to take any number of colors of balls, not just r, g, b

    - takes memory proportional to n (total number of balls)
    - draw() takes constant time
    - reset() takes constant time

    """

    def __init__(self, r_count, g_count, b_count):
        self.ball_count = r_count + g_count + b_count
        self.balls = ([RED] * r_count) + ([GREEN] * g_count) + ([BLUE] * b_count)

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
    Could be generalized to take any number of colors of balls, by maintaining a color frequency list instead of
    individual variables

    - takes memory proportional to the number of distinct colors
    - draw() takes time proportional to the number of distinct colors
    - reset() takes time proportional to the number of distinct colors

    """

    def __init__(self, r_count, g_count, b_count):
        self.ball_count = r_count + g_count + b_count
        self.initial_r_count = r_count
        self.initial_g_count = g_count
        self.initial_b_count = b_count
        self.r_count = r_count
        self.g_count = g_count
        self.b_count = b_count

    def draw(self):
        random_index = random.randint(0, self.ball_count - 1)
        self.ball_count -= 1
        if random_index < self.r_count:
            self.r_count -= 1
            return RED
        elif random_index < self.r_count + self.g_count:
            self.g_count -= 1
            return GREEN
        else:
            self.b_count -= 1
            return BLUE

    def reset(self):
        self.r_count = self.initial_r_count
        self.g_count = self.initial_g_count
        self.b_count = self.initial_b_count
        self.ball_count = self.r_count + self.g_count + self.b_count

    def count(self):
        return self.ball_count


def probability_3rd_draw_matches(bag, trials=100000):
    assert bag.count() >= 6
    match_count = 0

    for i in range(trials):
        # throw away first 4 draws
        for j in range(4):
            bag.draw()

        ball_5 = bag.draw()
        ball_6 = bag.draw()
        if ball_5 == ball_6:
            match_count += 1

        # reset for next trial
        bag.reset()

    return float(match_count) / trials  # float() to make this safe for python 2


def probability_3rd_draw_matches_math(r_count, g_count, b_count):
    n = r_count + g_count + b_count
    assert n > 1  # otherwise we will have infinity in denominator
    numerator = r_count * (r_count - 1) + g_count * (g_count - 1) + b_count * (b_count - 1)
    denominator = n * (n - 1)
    return float(numerator) / denominator  # float() to make this safe for python 2


def show_results_trials(bag, trials=100000):
    start = time.time()
    prob = probability_3rd_draw_matches(bag, trials)
    end = time.time()

    print("")
    print(bag.__class__.__name__)
    print("Probability: " + str(prob))
    print("Time: " + str((end - start) * 1000) + " ms")


def show_results_bag_list(r_count, g_count, b_count):
    bag = BagList(r_count, g_count, b_count)
    show_results_trials(bag)


def show_results_bag_no_list(r_count, g_count, b_count):
    bag = BagNoList(r_count, g_count, b_count)
    show_results_trials(bag)


def show_results_math(r_count, g_count, b_count):
    start = time.time()
    prob = probability_3rd_draw_matches_math(r_count, g_count, b_count)
    end = time.time()

    print("")
    print("Math")
    print("Probability: " + str(prob))
    print("Time: " + str((end - start) * 1000) + " ms")


def show_results(r_count, g_count, b_count):
    show_results_bag_list(r_count, g_count, b_count)
    show_results_bag_no_list(r_count, g_count, b_count)
    show_results_math(r_count, g_count, b_count)


if __name__ == "__main__":
    r, g, b = [int(a) for a in sys.argv[1:]]
    show_results(r, g, b)
