import torch
import numpy as np
from src.env.MinesweeperEnv import MinesweeperEnv
from src.agent.DQNAgent import DQNAgent, ReplayBuffer

def train():
    # Hardware
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Starting training in: {device}")

    # Params
    EPISODES = 5000              # Number of games
    BATCH_SIZE = 64             
    GAMMA = 0.99                 
    LR = 1e-4                   
    TARGET_UPDATE_FREQ = 1000    # Frequency that states when will the target policy will get updated
    
    # Changes on epsilon
    EPSILON_START = 1.0       
    EPSILON_END = 0.05          
    EPSILON_DECAY = 0.999       

  
    env = MinesweeperEnv()
    
    agent = DQNAgent(input_shape=(1, 8, 10), num_actions=160, device=device, lr=LR)
    memory = ReplayBuffer(capacity=10000)

    epsilon = EPSILON_START
    total_steps = 0

    # Main loop
    for episode in range(EPISODES):
        state, _ = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            # Action phase
            action = agent.select_action(state, epsilon)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # Meory phase
            memory.push(state, action, reward, next_state, float(done))
            
            # We update the values
            state = next_state
            total_reward += reward
            total_steps += 1
            
            # Learning phase
            agent.learn(memory, BATCH_SIZE, GAMMA)
            
            # Target sincronization
            if total_steps % TARGET_UPDATE_FREQ == 0:
                agent.target_net.load_state_dict(agent.policy_net.state_dict())

        # Epsilon reduction
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

        # Prints
        if episode % 10 == 0:
            print(f"Episode {episode} | Total_Steps: {total_steps} | Reward: {total_reward:.2f} | Epsilon: {epsilon:.3f} | Memory: {len(memory)}")

        # Saving learning experiences
        if episode % 500 == 0 and episode > 0:
            torch.save(agent.policy_net.state_dict(), f"dqn_minesweeper_ep{episode}.pth")
            print(f"Model saved in episode {episode}")

    # Final save
    torch.save(agent.policy_net.state_dict(), "dqn_minesweeper_final.pth")
    print("Training finished")

if __name__ == "__main__":
    train()