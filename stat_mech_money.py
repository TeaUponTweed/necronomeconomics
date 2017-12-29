import random

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


class Agent(object):
    def __init__(self, money):
        self.money = money


def main():
    initial_money = 10000
    nagents = 10000
    pdf = stats.expon(initial_money/nagents).pdf
    economy = [Agent(initial_money) for _ in range(nagents)]
    nsteps = 0
    while True:
        nsteps += 1
        random.shuffle(economy)
        for winner, loser in zip(economy[:nagents//2], economy[nagents//2:]):
            delta = .1 * (winner.money + loser.money)
            if delta <= loser.money:
                winner.money += delta
                loser.money -= delta

        if nsteps % 10 == 0:
            # x = np.linspace(0, 1, 10000)
            x = np.arange(10000)
            y = sorted([a.money for a in economy], reverse=True)
            plt.plot(x, y)
            # plt.plot(x, pdf(x)*initial_money*nagents)
            plt.show()


if __name__ == '__main__':
    main()
