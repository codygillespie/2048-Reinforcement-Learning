import unittest
import argparse

import torch
from tfe.game import GameState, do_game_loop
from tfe.train import DEVICE, train

def run_unit_tests():
    suite = unittest.TestLoader().discover('tfe/tests')
    unittest.TextTestRunner(verbosity=2).run(suite)


def train_model():
    # TODO: clean up this function
    agent = train()
    print('Training complete!')

    game = GameState.new()
    game.pretty_print()
    input()
    while True:
        action = agent.select_action(torch.tensor(game.cells, dtype=torch.float32).unsqueeze(0).to(DEVICE), 0.0)
        game = { 0: game.up(), 1: game.down(), 2: game.left(), 3: game.right() }[action]
        game.pretty_print()
        input()

        if game.is_game_over():
            print('Game over!')
            break

# play
def play_game():
    do_game_loop()

def main():
    # Parse primary commands: unittest, train, play
    # Input should look like "python main.py unittest"
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='The command to run')
    args = parser.parse_args()

    if args.command == 'unittest':
        run_unit_tests()
    elif args.command == 'train':
        train_model()
    elif args.command == 'play':
        play_game()
    else:
        print('Invalid command')

if __name__ == '__main__':
    main()