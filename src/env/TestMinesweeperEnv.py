from src.env.MinesweeperEnv import MinesweeperEnv

env = MinesweeperEnv()
obs, info = env.reset()

for _ in range(10):
    # We perform a random action
    action = env.action_space.sample() 
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Action: {action} | Reward: {reward} | Terminated?: {terminated}")
    
    if terminated:
        print("Game ended. Reseting...")
        env.reset()