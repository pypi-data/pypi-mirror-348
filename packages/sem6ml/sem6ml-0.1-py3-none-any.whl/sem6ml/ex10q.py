# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise10 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running Q-Learning Implementation...\n")
    
    # Import required libraries
    import numpy as np
    import random

    # Environment setup
    env_states = 5  # Number of states
    env_actions = 2  # Number of actions
    Q_table = np.zeros((env_states, env_actions))
    print(f"Initialized Q-table with {env_states} states and {env_actions} actions\n")

    # Hyperparameters
    alpha = 0.1  # Learning rate
    gamma = 0.9  # Discount factor
    epsilon = 0.2  # Exploration rate

    # Simulated rewards and transitions
    def get_reward(state, action):
        reward = random.choice([-1, 0, 1])
        print(f"State {state}, Action {action} → Reward: {reward}")
        return reward

    def get_next_state(state, action):
        next_state = (state + action) % env_states
        print(f"State {state}, Action {action} → Next state: {next_state}")
        return next_state

    # Training loop with enhanced logging
    for episode in range(100):
        state = random.randint(0, env_states - 1)
        print(f"\n=== Episode {episode + 1} ===")
        print(f"Starting state: {state}")
        
        for step in range(10):
            # Exploration or exploitation
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, env_actions - 1)
                print(f"Step {step + 1}: Exploring with random action {action}")
            else:
                action = np.argmax(Q_table[state])
                print(f"Step {step + 1}: Exploiting with best action {action}")

            # Interaction with environment
            reward = get_reward(state, action)
            next_state = get_next_state(state, action)

            # Store old Q-value for display
            old_q = Q_table[state, action]
            
            # Q-learning update
            Q_table[state, action] += alpha * (reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action])
            
            print(f"Q-update: State {state}, Action {action}: {old_q:.2f} → {Q_table[state, action]:.2f}")

            # Move to the next state
            state = next_state

    # Display the final Q-Table with formatting
    print("\n=== Final Q-Table ===")
    print("State\tAction 0\tAction 1")
    for state in range(env_states):
        print(f"{state}\t{Q_table[state, 0]:.4f}\t\t{Q_table[state, 1]:.4f}")

if __name__ == "__main__":
    run()