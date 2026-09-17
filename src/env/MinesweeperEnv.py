import gymnasium as gym
from gymnasium import spaces
import numpy as np
from src.game.Board import Board
from src.game.Cell import EmptyCell, MineCell, NumberCell

class MinesweeperEnv(gym.Env):
    """ This will be the Enviroment following a gym interface"""
    
    def __init__(self):
        super().__init__()

        #Step 1: We initialize the Board
        self.board = Board()

        #Step 2: We define an action space (the width height values can be changed in Board.py)
        total_cells = self.board.width * self.board.height
        self.action_space = spaces.Discrete(total_cells * 2) #Reveal or Flag, so we have to double the action space
        
        #Step 3: We define what will AI see
        """The range will be considered from -2 to 8 following the next distribution
            -2: Flag
            -1: Hidden
            0: Empty
            1-8: Cell value (number of adjacent mines)
            ---We don't need to assign the mine value as the game will end modifying the gymnasium terminated variable---
            """
        self.observation_space = spaces.Box(
            low=-2,
            high=8, 
            shape=(self.board.height, self.board.width), 
            dtype=np.int8 #More than enough
        )

    def _get_obs(self):
        """This is a traductor from the real board to the info we need via numpy"""
        obs = np.zeros((self.board.height, self.board.width), dtype=np.int8)
        
        for y in range(self.board.height):
            for x in range(self.board.width):
                #we traverse the board assingning the values to the observation space
                cell = self.board._get_cell(x, y) 
                
                if cell.is_flagged():
                    obs[y][x] = -2
                elif not cell.is_revealed():
                    obs[y][x] = -1
                elif isinstance(cell, NumberCell):
                    obs[y][x] = cell.get_value()
                elif isinstance(cell, EmptyCell):
                    obs[y][x] = 0
        return obs    

    def reset(self, seed=None, options=None):
        """This will reset the previous game, generate another and "click" randomly once so the board is initialized"""

        super().reset(seed=seed)
        self.board.reset()
        
        start_x = self.np_random.integers(0, self.board.width)
        start_y = self.np_random.integers(0, self.board.height)
        self.board.click_cell(start_x, start_y)
        
        # We return the generated obs matrix and an empty info dictionary (info is required in the return for gym)
        return self._get_obs(), {}

    def step(self, action):
        """It will execute ai's action and return the result"""

        total_cells = self.board.width * self.board.height

        # Reveal or Flag (action >= total_cells means flag action)
        is_flag_action = action >= total_cells

        # Step 1: Traduce the action. (In a board with area 80, the AI will pick a value between 0-79)
        position = action % total_cells
        x = position % self.board.width
        y = position // self.board.width
        
        # We count how many cells were revealled previously
        revealed_before = self._count_revealed()
        
        # Step 2: We execute the action
        if is_flag_action:
            self.board.flag_cell(x, y)
        else:
            self.board.click_cell(x, y)
        
        # Step 3: We check if it's terminated.
        terminated = self.board.is_game_over() or self.board.is_game_won()
        obs = self._get_obs()
        
        # Step 4: Code for the reward system. Every assignment is written += even for negative numbers, as a way of identifying faster negative and positive rewards
        reward = 0.0
        if self.board.is_game_over():
            reward += -1.0 # Worst punishment: mine clicked

            # Counting of final correct flags
            correct_flags = self._count_flagged()
                        
            # Each correct flag adds 0.02 to the rewards.
            reward += (correct_flags * 0.02) #This value is 10 times fewer than the win ones so the AI doesn't get "suicide" behaviours

        elif self.board.is_game_won():
            reward += 1.0  # Won game base reward
            
            # Counting of final correct flags
            correct_flags = self._count_flagged()
                        
            # Each correct flag adds 0.2 to the rewards.
            reward += (correct_flags * 0.2)

        else:
            if is_flag_action:
                reward += -0.01 # This has a small punishment so it doesn't loop-flag
            else:
                revealed_after = self._count_revealed()
                if revealed_after > revealed_before:
                    # Variable reward depending on the number of cells revealed.
                    reward += 0.1 * (revealed_after - revealed_before)
                else:
                    # Small punishment for already revealed cells.
                    reward += -0.1 
                
        # Gym states that you must return: the observation matrix, rewardpoints, terminated, truncated (this will be false) and info
        return obs, reward, terminated, False, {}

    def _count_revealed(self):
        """Aux function: count revealed cells"""
        count = 0
        for y in range(self.board.height):
            for x in range(self.board.width):
                if self.board._get_cell(x, y).is_revealed():
                    count += 1
        return count

    def _count_flagged(self):
        """Aux function: count flagged cells"""
        correct_flags = 0
        for r in range(self.board.height):
            for c in range(self.board.width):
                cell = self.board._get_cell(c, r)
                if isinstance(cell, MineCell) and cell.is_flagged():
                    correct_flags += 1
        return correct_flags