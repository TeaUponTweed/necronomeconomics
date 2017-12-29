import math
import itertools as it
import bisect
import random
# class Agent(object):
#     def __init__(self, money=0, preferences=None, employer=None):
#         self.preferences = preferences or {}
#         self.employer = employer
#         self.money = money


# class Firm(object):
#     def __init__(self, product=None, employees=None):
#         self.product = product
#         self.employees = employees or []

#     def __call__(self, dt):
#         pass

def groupby(itr, key):
    grouped_map = {}
    for value in itr:
        k = key(value)
        try:
            grouped_map[k].append(value)
        except KeyError:
            grouped_map[k] = [value]
    return iter(grouped_map.items())

class Agent(object):
    def __init__(self, produces, consumes):
        self.produces = produces
        self.consumes = consumes


class Economy(object):
    def __init__(self, agents=None):
        self.agents = agents or []

    def does_consume(self, *consumes):
        return Economy([a for a in self.agents if all(c in a.consumes for c in consumes)])

    def does_not_consume(self, *not_consumes):
        return Economy([a for a in self.agents if not any(c in a.consumes for c in not_consumes)])

    def does_produce(self, *produces):
        return Economy([a for a in self.agents if all(c in a.produces for c in produces)])

    def does_not_produce(self, *not_produces):
        return Economy([a for a in self.agents if not any(c in a.produces for c in not_produces)])

    def get_firms(self):
        return self.does_not_produce('labor')

    def get_people(self):
        return self.does_produce('labor')

    def _check(self):
        assert not self.get_firms().get_people().agents

    def make_person(self):
        produces = {'labor': random.random()}
        consumes = {'food': 1, 'clothing': 0.1, random.choice(list(ALL_PRODUCTS.keys())): random.random()}
        a = Agent(produces, consumes)
        self.agents.append(a)
        return a

    def make_firm(self):
        demand = {}
        for product, items in groupby(it.chain(*(a.consumes.items() for a in self.agents)), lambda x: x[0]):
            demand[product] = sum(d for _,d in items)
        products, demand = zip(*demand.items())

        next_product = random_choice(products, demand)
        consumes = {p: random.random() for p in [*ALL_PRODUCTS[next_product], 'labor']}
        produces = {next_product: random.random()}
        a = Agent(produces, consumes)
        self.agents.append(a)
        return a

'''
People produce labor and consume goods
Firms consume labor and raw materials and produce goods

Need to have a market, where all goods and services live.

Each individual has:

'''
ALL_PRODUCTS = {
    'food': ['fertilizer'],
    'clothing': ['cloth'],
    'VCR': ['metal'],
    'TV': ['glass', 'metal'],
    'lotion': [],
    'coolness': []
}

product_inputs = set(it.chain(*ALL_PRODUCTS.values(), ['labor']))
product_outputs = set(it.chain(ALL_PRODUCTS.keys(), product_inputs))

'''
def soft_max(lst, weights):
    all_weight = sum(weights)
    print(lst, weights, all_weight)
    # assert False
    # weights = [math.exp(w-all_weight) for w in weights]
    # print(lst, weights)
    # print('***')
    return random_choice(lst, weights=weights)
'''

def random_choice(lst, weights):
    weights = list(it.accumulate(weights))
    total_weight = weights[-1]
    draw = random.random() * total_weight
    ix = bisect.bisect_left(weights, draw)
    return lst[ix]


def main():
    e = Economy()
    for _ in range(1000):
        e.make_person()
    e.make_firm()


if __name__ == '__main__':
    main()
