from hot_pile_sim import HotPile
from hot_pile_sim.strategy.rngesus import RandomPlayer

win_pct = 0
num_piles = 1
num_trials = 10000

while win_pct < 50:
    num_wins = 0
    num_cards_left = 0

    game = HotPile(RandomPlayer(), num_piles=num_piles)
    for _ in range(num_trials):
        if result := game.sim_game():
            num_cards_left += result
        else:
            num_wins += 1
        game.reset()

    win_pct = round(num_wins / num_trials * 100, 2)
    print(num_piles, win_pct, round(num_cards_left / (num_trials - num_wins), 2))

    num_piles += 1
