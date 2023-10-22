import torch
from game import GameState
from train import DEVICE, train

def main():
    agent = train()

    game = GameState.new()
    game.pretty_print()
    input()
    while True:
        action = agent.select_action(torch.tensor(game.cells, dtype=torch.float32).unsqueeze(0).to(DEVICE), 0.0)
        game = { 0: game.up(), 1: game.down(), 2: game.left(), 3: game.right() }[action]
        game.pretty_print()
        input()


if __name__ == '__main__':
    main()