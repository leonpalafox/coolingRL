# Server Cooling Environment

A reinforcement learning environment for training AI agents to optimize server temperature control and energy consumption.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Environment Details](#environment-details)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Use Cases](#use-cases)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This environment simulates a server cooling system where an AI agent must maintain optimal temperature while minimizing energy consumption. The agent faces realistic challenges including:

- **Seasonal temperature variations** (12-month cycle)
- **Dynamic server load** (varying number of users)
- **Fluctuating data processing rates**
- **Energy efficiency optimization**

The environment is designed for educational purposes and reinforcement learning research, providing a realistic yet manageable scenario for testing various RL algorithms.

## ✨ Features

- **Realistic Physics**: Temperature dynamics based on atmospheric conditions, user load, and data processing
- **Dynamic Environment**: Monthly temperature cycles and random fluctuations in server load
- **Energy Optimization**: Reward system that encourages energy-efficient solutions
- **Flexible Configuration**: Customizable temperature ranges, initial conditions, and constraints
- **Educational Focus**: Comprehensive documentation and examples for learning
- **Training/Inference Modes**: Different behaviors for exploration vs. deployment

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/server-cooling-environment.git
cd server-cooling-environment

# Install dependencies
pip install numpy

# For Jupyter notebook examples
pip install jupyter matplotlib
```

## 🚀 Quick Start

```python
import numpy as np
from environment import Environment

# Create environment
env = Environment(
    optimal_temperature=[18.0, 24.0],  # Target temperature range
    initial_month=0,                   # Start in January
    initial_number_users=20,           # Initial server load
    initial_rate_data=80              # Initial data processing rate
)

# Get initial state
state, reward, done = env.observe()
print(f"Initial state: {state}")
print(f"Initial temperature: {env.temperature_ai:.2f}°C")

# Take an action: cool down with 2.0 energy units
next_state, reward, done = env.update_env(
    direction=-1,    # -1 for cooling, +1 for heating
    energy_ai=2.0,   # Energy consumed by AI
    month=0          # Current month
)

print(f"Reward: {reward:.6f}")
print(f"New temperature: {env.temperature_ai:.2f}°C")
print(f"Episode done: {done}")
```

## 🏗 Environment Details

### State Space
The environment provides a normalized 3-dimensional state vector:
- **Temperature**: Current server temperature (normalized to [0,1])
- **Users**: Number of active users (normalized to [0,1])
- **Data Rate**: Current data processing rate (normalized to [0,1])

### Action Space
Actions are defined by two parameters:
- **Direction**: `-1` (cooling) or `+1` (heating)
- **Energy**: Positive float representing energy consumption

### Reward Function
```
reward = (energy_no_ai - energy_ai) × 1e-3
```
The agent is rewarded for using less energy than a baseline non-AI system.

### Temperature Dynamics
```
intrinsic_temperature = atmospheric_temp + 1.25 × users + 1.25 × data_rate
server_temperature = intrinsic_temperature + ai_action_effect
```

### Environmental Factors

| Factor | Range | Description |
|--------|-------|-------------|
| Atmospheric Temperature | 1°C - 24°C | Monthly cycle (Jan: 1°C, Aug: 24°C) |
| Number of Users | 10 - 100 | Random fluctuations ±5 per step |
| Data Rate | 20 - 300 | Random fluctuations ±10 per step |
| Server Temperature | -20°C - 80°C | Game over if exceeded during training |

## 📖 API Reference

### `Environment(optimal_temperature, initial_month, initial_number_users, initial_rate_data)`

**Parameters:**
- `optimal_temperature`: List `[min, max]` defining target temperature range
- `initial_month`: Integer (0-11) representing starting month
- `initial_number_users`: Integer (10-100) initial server load
- `initial_rate_data`: Integer (20-300) initial data processing rate

### `update_env(direction, energy_ai, month)`

Updates environment after AI action.

**Parameters:**
- `direction`: Integer (-1 for cooling, +1 for heating)
- `energy_ai`: Float representing energy consumed
- `month`: Integer (0-11) current month

**Returns:**
- `next_state`: Normalized state vector
- `reward`: Float reward value
- `game_over`: Boolean indicating episode termination

### `observe()`

Returns current environment state.

**Returns:**
- `current_state`: Normalized state vector
- `reward`: Last reward received
- `game_over`: Boolean indicating episode status

### `reset(new_month)`

Resets environment to initial conditions.

**Parameters:**
- `new_month`: Integer (0-11) starting month for new episode

## 💡 Examples

### Basic Usage
```python
# Initialize environment
env = Environment()

# Run one episode
for step in range(100):
    state, reward, done = env.observe()
    
    if done:
        break
    
    # Simple cooling strategy
    if env.temperature_ai > 21.0:
        direction = -1  # Cool down
        energy = 1.0
    else:
        direction = 1   # Heat up
        energy = 0.5
    
    next_state, reward, done = env.update_env(direction, energy, step % 12)
    print(f"Step {step}: Temp={env.temperature_ai:.2f}°C, Reward={reward:.6f}")
```

### Seasonal Analysis
```python
# Test performance across different seasons
seasons = ['Winter', 'Spring', 'Summer', 'Fall']
starting_months = [0, 3, 6, 9]

for season, month in zip(seasons, starting_months):
    env.reset(month)
    print(f"\n{season} (Month {month}):")
    print(f"  Atmospheric temp: {env.atmospheric_temperature}°C")
    print(f"  Initial server temp: {env.temperature_ai:.2f}°C")
    
    # Run a few steps to see dynamics
    for step in range(5):
        state, reward, done = env.update_env(-1, 1.0, month)
        if done:
            break
```

### Energy Efficiency Comparison
```python
# Compare AI vs non-AI energy consumption
env = Environment()

# Run simulation
for step in range(1000):
    state, reward, done = env.observe()
    if done:
        env.reset(step % 12)
        continue
    
    # AI takes action
    env.update_env(-1, 1.0, step % 12)

print(f"AI total energy: {env.total_energy_ai:.2f}")
print(f"Non-AI total energy: {env.total_energy_noai:.2f}")
print(f"Energy savings: {env.total_energy_noai - env.total_energy_ai:.2f}")
```

## 🎓 Use Cases

### Educational Applications
- **Reinforcement Learning Courses**: Hands-on environment for testing RL algorithms
- **Control Systems**: Understanding feedback control in dynamic systems
- **Energy Optimization**: Teaching sustainable computing practices
- **Multi-objective Optimization**: Balancing performance and efficiency

### Research Applications
- **Algorithm Development**: Testing new RL algorithms on realistic scenarios
- **Transfer Learning**: Adapting models across different seasonal conditions
- **Multi-agent Systems**: Coordinating multiple servers
- **Robustness Testing**: Evaluating performance under varying conditions

### Practical Applications
- **Data Center Management**: Prototyping cooling strategies
- **IoT Systems**: Temperature control for embedded systems
- **Smart Buildings**: HVAC optimization
- **Industrial Control**: Process temperature management

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yourusername/server-cooling-environment.git
cd server-cooling-environment
pip install -e .
```

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
We use [Black](https://black.readthedocs.io/) for code formatting:
```bash
black environment.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by real-world data center cooling challenges
- Designed for educational use in reinforcement learning courses
- Built with simplicity and extensibility in mind

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/server-cooling-environment/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/server-cooling-environment/discussions)
- **Email**: your.email@example.com

---

**Happy Learning! 🚀**
