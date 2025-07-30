"""
Command line interface for TheSwarm.
"""
import argparse
import sys
from typing import List

from theswarm import __version__
from theswarm.swarm import Agent, Swarm


def main(args: List[str] = None) -> int:
    """
    Main entry point for TheSwarm CLI.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code
    """
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description="TheSwarm - Distributed AI Framework")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--demo", action="store_true", help="Run a simple demo")
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.version:
        print(f"TheSwarm version {__version__}")
        return 0
        
    if parsed_args.demo:
        print("Running TheSwarm demo...")
        run_demo()
        return 0
        
    parser.print_help()
    return 0


def run_demo():
    """Run a simple demo of TheSwarm functionality."""
    print("Initializing swarm with 3 agents...")
    
    swarm = Swarm(capacity=5, communication_protocol="mesh")
    
    for i in range(3):
        agent = Agent(
            agent_id=f"agent-{i}",
            model_type="transformer",
            specialization="general"
        )
        swarm.add_agent(agent)
        
    print(f"Added {len(swarm.agents)} agents to the swarm")
    
    print("Initializing swarm...")
    swarm.initialize()
    
    print("Running a sample classification task...")
    results = swarm.solve(problem="classification", data={"sample": "data"})
    
    print("\nResults:")
    print(f"Success: {results.summary()['success']}")
    print(f"Metrics: {results.summary()['metrics']}")
    print(f"Agents: {results.summary()['agents_participated']}")


if __name__ == "__main__":
    sys.exit(main()) 