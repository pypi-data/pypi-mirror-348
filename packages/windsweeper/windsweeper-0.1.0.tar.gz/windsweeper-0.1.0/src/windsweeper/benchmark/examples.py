"""
Example benchmark tests for the Windsweeper SDK.
"""

import os
import asyncio
from typing import Dict, Any

from .benchmark import create_benchmark, BenchmarkConfig

# Sample benchmark configuration
config: Dict[str, Any] = {
    "name": "Windsweeper Python SDK Core Operations",
    "iterations": 5,
    "warmup": True,
    "warmup_iterations": 2,
    "measure_memory": True,
    "server_url": os.environ.get("MCP_SERVER_URL", "http://localhost:3000"),
    "api_key": os.environ.get("MCP_API_KEY"),
    "timeout": 10000,
    # Disable telemetry for benchmarks
    "client_options": {
        "telemetry": {
            "enabled": False
        }
    }
}

# Create the benchmark suite
benchmark = create_benchmark(config)

# Add test cases
benchmark.add("Server Health Check", lambda client, i: client.check_health())

benchmark.add("List Resources (No Pagination)", lambda client, i: client.list_resources("test-server"))

async def validate_rule(client, i):
    rule_yaml = """
    name: ExampleRule
    description: A sample rule for benchmarking
    pattern:
      kind: AST
      language: python
      query: "Call[func.attr='debug'][func.value.id='logging']"
    message: Using logging.debug is not recommended
    severity: warning
    """
    return await client.validate_rule(rule_yaml)

benchmark.add("Validate Rule", validate_rule)

async def validate_code(client, i):
    code = """
    import logging
    
    def example():
        logging.info("This is an info message")
        logging.debug("This is a debug message")
        logging.error("This is an error message")
        return True
    """
    rule_ids = ["no-logging-debug", "prefer-f-strings"]
    return await client.validate_code(code, rule_ids, "python")

benchmark.add("Validate Code", validate_code)

# Run the benchmarks
async def run_benchmarks():
    """Run all benchmark tests and generate a report."""
    try:
        # Run all tests
        report = await benchmark.run()
        
        # Print formatted report
        print("\n" + benchmark.format_report())
        
        # Save report to file
        timestamp = report["timestamp"].replace(":", "-")
        benchmark.save_report(f"./benchmark-report-{timestamp}.json")
        
        return report
    except Exception as error:
        print(f"Benchmark failed: {error}")
        raise

# Run if directly executed
if __name__ == "__main__":
    asyncio.run(run_benchmarks())
