# AI-Sweeper

AI-Sweeper is a small experiment done purely for fun and learning purposes focused on teaching an artificial intelligence to play the classic Minesweeper game using reinforcement learning.

The goal of this project is to create a self learning agent capable of identifying safe moves and avoiding mines through trial and error, improving its strategy over time.

---

## Features (planned)

- Basic Minesweeper game logic (custom environment)
- Reinforcement learning agent (Q-Learning / DQN)
- Reward-based training system
- Progress visualization and performance tracking
- Optional visual interface to watch the AI play in real time

---

## Tech Stack

- Python 3.12+
- NumPy
- PyTorch (for deep learning)
- Gymnasium (for the training environment)
- Matplotlib / Seaborn (for stats and visualization)

---

## Project Structure (planned)

```
ai-sweeper/
│
├── src/
│ ├── game/ # Minesweeper game logic
│ ├── env/ # RL environment wrapper (Gym-style)
│ ├── agent/ # The AI (Q-Learning / DQN)
│ ├── train.py # Training loop
│ └── visualize.py # Optional visualization
│
├── tests/ # Unit tests
├── requirements.txt
└── README.md
```
---

## Setup

```bash
# Clone the repo
git clone https://github.com/Alejandrorr572/ai-sweeper.git
cd ai-sweeper

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## How it works (concept overview)

### Game Environment
A simplified Minesweeper game that generates a new board every episode.

### Agent
The AI receives partial information (the visible board) and decides which cell to open or flag.

### Reward System

Opening a safe cell → small positive reward

Flagging a mine -> small positive reward

Hitting a mine → strong negative reward

Clearing the board → large positive reward

### Learning Loop
Through many episodes, the AI learns which actions lead to higher long-term rewards.

## Goals

Implement the full Minesweeper logic ✅

Design a Gym-like environment ✅

Train a DQN agent with PyTorch via Deep Q-Learning ✅

Visualize the learning process ⏳

## Notes

This project is mainly a learning exercise in reinforcement learning and AI environment design.
It is open for anyone interested in experimenting, improving, or extending it.

### License

MIT License © 2025 — Developed by Alejandro Rivada Rodríguez.
