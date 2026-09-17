import torch
import torch.optim as optim
import random
from collections import deque
import numpy as np
from src.agent.DQN import DQN

class DQNAgent:
    def __init__(self, input_shape, num_actions, device, lr=1e-4):
        self.device = device #Gaphic card or Cpu
        self.num_actions = num_actions

        #Policy net which will play and train every step
        self.policy_net = DQN(input_shape, num_actions).to(device)

        #Target net is a stable predictor for future rewards
        self.target_net = DQN(input_shape, num_actions).to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval() # Starts evaluation mode (won't calculate any gradients in target)

        #This will optimize the policy net weights using the learning rate
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)

    def select_action(self, state, epsilon):
        """
        We will use Epsilon-Greedy
        Epsilon is a percentaje, for example 0.10 means 10% probability of exploring
        """
        #Generate number between 0-1
        if random.random() < epsilon:
            # Exploration, we do a totally random movement to explore the game
            return random.randrange(self.num_actions)
        else:
            # We use DQN learned experience
            with torch.no_grad(): # Memory saving purposes
                
                # State will come as a numpy matrix (8, 10). 
                # We add batch and channel dimension so the DQN will accept it: (1, 1, 8, 10)
                state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(self.device)
                
                # We use the dqn to obtain the q_values
                q_values = self.policy_net(state_tensor)
                
                # We return the most valuable action
                return q_values.argmax().item()


    def learn(self, memory_buffer, batch_size, gamma=0.99):
            """Bellman ecuation application"""
    
            # If there aren't enought samples in the buffer, we can't start
            if len(memory_buffer) < batch_size:
                return
    
            # Random sample using the buffer function
            states, actions, rewards, next_states, dones = memory_buffer.sample(batch_size, self.device)
    
            #Prediction
            # We send the 64 states to the policy net, returns 160 values per state
            q_values = self.policy_net(states)
            
            # We use gather to extract the values from the chosen action, if it did the action 45, then we extract column 45 value
            current_q_values = q_values.gather(1, actions)
    
            #Real values
            with torch.no_grad():
                # We send the actions after the action
                next_q_values = self.target_net(next_states)

                # We get only the maximum possible value from the next turn
                # .max(1)[0] gets the higher value and unsqueeze(1) transforms it as a column
                max_next_q_values = next_q_values.max(1)[0].unsqueeze(1)

            #Backpropagation
            # Loss between prediction and reality
            # We use smooth l1 loss as its less sensible to extreme values than MSE
            target_q_values = rewards + (gamma * max_next_q_values * (1 - dones))
            loss = torch.nn.functional.smooth_l1_loss(current_q_values, target_q_values)

            # We optimize the weights
            self.optimizer.zero_grad() # We clean the last calculations for optimization
            loss.backward()            # We compute the gradients so we know how much each weight needs to be adjusted
            
            # This is to avoid gradients reaching inf values
            torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
            
            self.optimizer.step()      # We apply the changes to the policy net


class ReplayBuffer:
    def __init__(self, capacity: int):
        # this will erase oldest elements as the buffer reaches the maximum capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """Saves a transition in memory"""
        # state and next_state como as matrix from the function _get_obs() from the env
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int, device: torch.device):
        """Extracts a random sample and packs it as a Pytorch tensor"""
        batch = random.sample(self.buffer, batch_size)
        
        # We unpack the sample
        states, actions, rewards, next_states, dones = zip(*batch)
        
        # we transform every sample item into tensors, + then we send them to the cpu/gpu 
        # we add unsqueeze(1) to the state channel dimension so it matches with the DQN: (batch, 1, height, width) [check DQN]
        states = torch.tensor(np.array(states), dtype=torch.float32).unsqueeze(1).to(device)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32).unsqueeze(1).to(device)
        
        # We do the same for actions rewards and the dones(boolean checks that inform if the actual)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1).to(device) #Must be an int, 0-159 if it was a float it wont work sending an error
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1).to(device)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1).to(device)
        
        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)