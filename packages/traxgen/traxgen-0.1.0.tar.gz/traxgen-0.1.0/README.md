# Multi-Agent Trajectory Generator

This tool allows you to generate trajectories for multiple agents and combine them in a specified order.

## Features

- Generate valid trajectories for individual agents based on workflow definitions
- Combine multiple agent trajectories in a specified order
- Visualize multi-agent trajectories
- Save trajectories to JSON files

## Usage

### Basic Usage

To generate a trajectory for a sequence of agents, use:

```bash
python run.py [agent1] [agent2] ... [agentN]
```

Example:
```bash
python run.py book_flight cancel_flight
```

This will:
1. Load the workflow definitions for each agent from `test_data/workflows/`
2. Generate valid trajectories for each agent
3. Combine them in the specified order
4. Save the result to `output/trajectory_[agent1]_[agent2]_..._[agentN].json`
5. Generate a visualization at `output/vis_trajectory_[agent1]_[agent2]_..._[agentN].png`

### Output Format

The output is a list in the format:

```
[agent1_name, agent1_trajectory, agent2_name, agent2_trajectory, ...]
```

Each agent's trajectory is a list of steps to be executed in order.

## Workflow Definition Format

Workflows are defined in JSON files in the `test_data/workflows/` directory. Each workflow should include:

- `agent`: Name of the agent
- `steps`: List of steps that the agent can perform
- `soft_ordering`: Optional list of steps that can be executed in any order
- `conditionals`: Optional list of conditions that determine which steps to include

Example workflow definition:

```json
{
  "agent": "book_flight",
  "steps": [
    "get_customer_info(customer_id = customer_id) -> [name, email]",
    "search_flights(origin = origin, destination = destination) -> [flight_options]",
    "select_flight(flight_options = flight_options) -> [selected_flight]",
    "process_payment(customer_id = customer_id, amount = price)"
  ],
  "soft_ordering": [
    ["get_customer_info", "search_flights"]
  ],
  "conditionals": [
    {
      "field": "payment_method",
      "operator": "==",
      "value": "credit_card",
      "then": "process_payment",
      "else": "request_alternative_payment"
    }
  ]
}
```

## Extending

To add new agents:
1. Create a new workflow definition in `test_data/workflows/[agent_name].json`
2. Add the agent color to the `agent_colors` dictionary in the `visualize_multi_agent_trajectory` function

## Requirements

- Python 3.6+
- NetworkX
- Matplotlib