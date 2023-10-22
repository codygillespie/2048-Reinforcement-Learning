import torch
from torch import optim, nn
from collections import namedtuple, deque
import random

from deep import DQN
from game import GameState

DEVICE: str = 'cuda' if torch.cuda.is_available() else 'cpu'

Experience = namedtuple('Experience', ('state', 'action', 'reward', 'next_state', 'done'))
class ReplayMemory:
    def __init__(self, capacity): self.memory: deque['Experience'] = deque([], maxlen=capacity)
    def push(self, *args): self.memory.append(Experience(*args))
    def sample(self, batch_size): return random.sample(self.memory, batch_size)
    def __len__(self): return len(self.memory)

class DQNAgent:
    def __init__(self, input_dim, action_dim, learning_rate=1e-3):
        # Allow device to be changed to 'cpu' for testing
        self.q_network = DQN(input_dim, action_dim).to(DEVICE)
        self.target_network = DQN(input_dim, action_dim).to(DEVICE)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval() # set target network to evaluation mode
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
        self.memory = ReplayMemory(10000)
        self.gamma = 0.99 # discount factor
        self.batch_size = 64

    def select_action(self, state, epsilon = 0):
        if random.random() < epsilon: return random.randrange(4)
        else:
            with torch.no_grad():
                return self.q_network(state).max(1)[1].item()

    def optimize(self):
        if len(self.memory) < self.batch_size: return
        transitions = self.memory.sample(self.batch_size)
        batch = Experience(*zip(*transitions))

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat((torch.tensor(batch.action, dtype=torch.int64).unsqueeze(1).to(DEVICE),))
        reward_batch = torch.cat(batch.reward)
        next_state_batch = torch.cat(batch.next_state)
        done_batch = torch.cat(batch.done)

        q_values = self.q_network(state_batch).gather(1, action_batch)
        next_q_values = self.target_network(next_state_batch).max(1)[0].detach()
        expected_q_values = reward_batch + (self.gamma * next_q_values * (1 - done_batch))

        loss = nn.functional.smooth_l1_loss(q_values, expected_q_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

def train() -> DQNAgent:

    episodes = 1000
    epsilon_start = 1.0
    epsilon_end = 0.1
    epsilon_decay = 0.995
    epsilon = epsilon_start

    agent = DQNAgent(input_dim=16, action_dim=4)

    for episode in range(episodes):
        game = GameState.new() # Start a new game
        state = torch.tensor(game.cells, dtype=torch.float32).unsqueeze(0).to(DEVICE)
        done = False
        while not done:
            action = agent.select_action(state, epsilon)
            next_state = { 0: game.up(), 1: game.down(), 2: game.left(), 3: game.right() }[action]
            reward = next_state.score - game.score
            done = next_state.is_game_over()
            next_state = torch.tensor(next_state.cells, dtype=torch.float32).unsqueeze(0).to(DEVICE)
            reward = torch.tensor([reward], dtype=torch.float32).to(DEVICE)
            done = torch.tensor([done], dtype=torch.uint8).to(DEVICE)
            
            agent.memory.push(state, action, reward, next_state, done)
            state = next_state
            
            agent.optimize()

        if episode % 10 == 0:
            agent.update_target_network()
        
        epsilon = max(epsilon_end, epsilon_decay * epsilon) # decay epsilon

    return agent
