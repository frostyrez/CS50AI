# Nim

Teach an AI to play Nim via reinforcement learning.

<img width="300" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/3963b605-5cc8-4ecf-8ba5-76538dd7eb7a">

## Outline

- Nim is a turn-based game consisting of 4 piles of rocks, each pile having either 1, 3, 5, or 7 rocks. Each player can take any number of rocks from any one pile. The last player to remove a rock loses.
- Q-learning is used to train the AI, with the goal being to teach the AI to associate every possible `(state, action)` pair with a certain reward value, and to always pick the action with the highest reward.
- An action that loses the game will have a reward of -1, winning will result in 1, and all other actions will have an immediate reward of 0 but will also have some future reward.
- The Q value for each `(state, action)` is updated each time an action is taken, as such:

$$Q(s,a) \leftarrow Q(s,a) + \alpha * (\text{new value estimate} - \text{old value estimate})$$  

  where $\alpha$ is the learning rate, $\text{new value estimate}$ is the sum of the reward for the current action and the estimate of all future rewards, and $\text{old value estimate}$ is the existing value for $Q(s,a)$.  
  


## Usage
`python play.py`
