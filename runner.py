from hot_pile_sim import HotPile
from hot_pile_sim.strategy.greedy import GreedyPlayer

test = HotPile(GreedyPlayer(), verbose=False)
num_success = 0

for _ in range(1000):
    num_success += 1 if test.sim_game() == 0 else 0
    test.reset()

print(num_success)
