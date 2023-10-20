# 2048 Reinforcement Learning Agent

## Introduction

This project is a reinforcement learning agent that learns to play the game 2048. The agent is trained using a modified version of the game that allows the agent to play the game without any human interaction (see game.py).

The approach used is Deep Q-Learning with Experience Replay. The agent is trained using a simple fully connected neural network with 2 hidden layers (`deep.py`). The input to the network is the current state of the board, and the output is the Q-value for each possible action. 

## game.py

You can play the game directly by running `python game.py`. The game is played using the WASD keys.

## main.py

Training can be started by running `python main.py`.
