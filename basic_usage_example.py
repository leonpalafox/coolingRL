#!/usr/bin/env python3
"""
Basic Usage Example for Server Cooling Environment

This script demonstrates the fundamental operations of the server cooling environment:
- Environment initialization
- Taking actions
- Observing states and rewards
- Resetting episodes

Run this script to understand the basic workflow before implementing RL algorithms.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment import Environment
import numpy as np

def basic_interaction_demo():
    """Demonstrate basic environment interaction"""
    print("=== BASIC ENVIRONMENT INTERACTION ===\n")
    
    # Create environment with default settings
    env = Environment(
        optimal_temperature=[18.0, 24.0],
        initial_month=0,  # January
        initial_number_users=20,
        initial_rate_data=80
    )
    
    # Show initial state
    print("1. Initial Environment State:")
    print(f"   Month: January (0)")
    print(f"   Atmospheric temperature: {env.atmospheric_temperature}°C")
    print(f"   Number of users: {env.current_number_users}")
    print(f"   Data rate: {env.current_rate_data}")
    print(f"   Server temperature: {env.temperature_ai:.2f}°C")
    print(f"   Optimal range: {env.optimal_temperature[0]}°C - {env.optimal_temperature[1]}°C")
    
    # Get initial observation
    state, reward, done = env.observe()
    print(f"\n2. Initial Observation:")
    print(f"   Normalized state: {state}")
    print(f"   Reward: {reward}")
    print(f"   Done: {done}")
    
    # Take several actions
    print(f"\n3. Taking Actions:")
    
    actions = [
        {"direction": -1, "energy": 2.0, "description": "Cool down (high energy)"},
        {"direction": -1, "energy": 1.0, "description": "Cool down (low energy)"},
        {"direction": 1, "energy": 0.5, "description": "Heat up (minimal energy)"},
        {"direction": -1, "energy": 1.5, "description": "Cool down (medium energy)"},
    ]
    
    for i, action in enumerate(actions):
        print(f"\n   Action {i+1}: {action['description']}")
        print(f"   Before: Temp = {env.temperature_ai:.2f}°C, Users = {env.current_number_users}")
        
        # Take action
        next_state, reward, done = env.update_env(
            direction=action["direction"],
            energy_ai=action["energy"],
            month=(i + 1) % 12  # Progress through months
        )
        
        print(f"   After:  Temp = {env.temperature_ai:.2f}°C, Users = {env.current_number_users}")
        print(f"   Reward: {reward:.6f}")
        print(f"   Done: {done}")
        
        if done:
            print(f"   Episode ended! Temperature went out of bounds.")
            break
    
    # Show final energy consumption
    print(f"\n4. Final Energy Consumption:")
    print(f"   AI total energy: {env.total_energy_ai:.2f}")
    print(f"   Non-AI total energy: {env.total_energy_noai:.2f}")
    print(f"   Energy saved: {env.total_energy_noai - env.total_energy_ai:.2f}")

def simple_control_strategy():
    """Demonstrate a simple temperature control strategy"""
    print("\n\n=== SIMPLE CONTROL STRATEGY ===\n")
    
    env = Environment()
    
    print("Strategy: Keep temperature between 20-22°C")
    print("- If temp > 22°C: Cool down with energy proportional to excess")
    print("- If temp < 20°C: Heat up with energy proportional to deficit")
    print("- Otherwise: Do nothing (minimal energy)")
    
    total_steps = 50
    temperatures = []
    rewards = []
    actions_taken = []
    
    for step in range(total_steps):
        current_temp = env.temperature_ai
        temperatures.append(current_temp)
        
        # Simple control logic
        if current_temp > 22.0:
            # Too hot - cool down
            direction = -1
            energy = min(3.0, (current_temp - 22.0) * 2.0)  # Proportional cooling
            action_desc = f"Cool (energy: {energy:.2f})"
        elif current_temp < 20.0:
            # Too cold - heat up
            direction = 1
            energy = min(3.0, (20.0 - current_temp) * 2.0)  # Proportional heating
            action_desc = f"Heat (energy: {energy:.2f})"
        else:
            # Just right - minimal action
            direction = -1 if current_temp > 21.0 else 1
            energy = 0.1
            action_desc = f"Maintain (energy: {energy:.2f})"
        
        actions_taken.append(action_desc)
        
        # Take action
        next_state, reward, done = env.update_env(direction, energy, step % 12)
        rewards.append(reward)
        
        if step % 10 == 0:
            print(f"Step {step:2d}: Temp={current_temp:5.2f}°C, Action={action_desc}, Reward={reward:.6f}")
        
        if done:
            print(f"Episode ended at step {step}")
            break
    
    # Summary statistics
    print(f"\nSummary after {len(temperatures)} steps:")
    print(f"  Average temperature: {np.mean(temperatures):.2f}°C")
    print(f"  Temperature std dev: {np.std(temperatures):.2f}°C")
    print(f"  Average reward: {np.mean(rewards):.6f}")
    print(f"  Total energy consumed: {env.total_energy_ai:.2f}")
    print(f"  In optimal range: {np.sum([(t >= 18.0 and t <= 24.0) for t in temperatures])/len(temperatures)*100:.1f}%")

def reset_and_compare():
    """Demonstrate environment reset and compare different starting conditions"""
    print("\n\n=== ENVIRONMENT RESET AND COMPARISON ===\n")
    
    env = Environment()
    
    # Test different starting months
    months = [0, 3, 6, 9]  # January, April, July, October
    month_names = ["January", "April", "July", "October"]
    
    for month, name in zip(months, month_names):
        env.reset(month)
        
        print(f"{name} (Month {month}):")
        print(f"  Atmospheric temp: {env.atmospheric_temperature:5.1f}°C")
        print(f"  Initial server temp: {env.temperature_ai:5.2f}°C")
        
        # Take same action in each season
        next_state, reward, done = env.update_env(-1, 2.0, month)
        
        print(f"  After cooling action: {env.temperature_ai:5.2f}°C")
        print(f"  Reward: {reward:8.6f}")
        print()

if __name__ == "__main__":
    try:
        basic_interaction_demo()
        simple_control_strategy()
        reset_and_compare()
        
        print("\n=== EXAMPLE COMPLETED SUCCESSFULLY ===")
        print("Try modifying the control strategy or parameters to see different behaviors!")
        
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()
