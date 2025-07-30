"""
Benchmark utilities for the Windsweeper SDK.
Provides tools for measuring SDK performance and identifying optimization opportunities.
"""

import os
import gc
import json
import time
import platform
import statistics
from typing import Any, Callable, Dict, List, Optional, TypedDict, Union, Tuple
from datetime import datetime
from functools import wraps

from ... import windsweeper  # May need to adjust import path
from ..client import WindsweeperClient

# Type definitions
class BenchmarkResult(TypedDict, total=False):
    """Result of a single benchmark test case."""
    name: str
    success: bool
    duration_ms: float
    error: Optional[str]
    operations: int
    ops_per_second: float
    memory_before: Optional[int]
    memory_after: Optional[int]
    memory_diff: Optional[int]
    metrics: Optional[Dict[str, float]]


class BenchmarkReportSummary(TypedDict):
    """Summary statistics for a benchmark report."""
    total_tests: int
    passed: int
    failed: int
    total_duration_ms: float
    avg_duration_ms: float
    min_duration_ms: float
    max_duration_ms: float


class BenchmarkEnvironment(TypedDict):
    """Environment information for a benchmark report."""
    python_version: str
    platform: str
    platform_version: str
    sdk_version: str


class BenchmarkReport(TypedDict):
    """Complete benchmark report containing results of multiple test runs."""
    name: str
    timestamp: str
    environment: BenchmarkEnvironment
    results: List[BenchmarkResult]
    summary: BenchmarkReportSummary


class BenchmarkConfig(TypedDict, total=False):
    """Configuration for a benchmark test."""
    name: str
    iterations: int
    warmup: bool
    warmup_iterations: int
    measure_memory: bool
    server_url: str
    api_key: Optional[str]
    timeout: Optional[int]
    client_options: Optional[Dict[str, Any]]


# Type for benchmark test functions
BenchmarkTestFn = Callable[[WindsweeperClient, int], None]


class Benchmark:
    """
    Benchmark suite for running performance tests on the Windsweeper SDK.
    
    This class provides tools for measuring the performance of various SDK operations,
    tracking memory usage, and generating comprehensive reports.
    """
    
    def __init__(self, config: BenchmarkConfig):
        """
        Initialize a new benchmark suite.
        
        Args:
            config: Benchmark configuration options
        """
        # Set default configuration values
        self.config = {
            'iterations': 10,
            'warmup': True,
            'warmup_iterations': 2,
            'measure_memory': True,
        }
        # Update with provided config
        self.config.update(config)
        
        # Initialize test collection
        self.tests = {}
        
        # Initialize report
        self.report = {
            'name': self.config['name'],
            'timestamp': datetime.now().isoformat(),
            'environment': {
                'python_version': platform.python_version(),
                'platform': platform.system(),
                'platform_version': platform.release(),
                'sdk_version': self._get_sdk_version()
            },
            'results': [],
            'summary': {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'total_duration_ms': 0,
                'avg_duration_ms': 0,
                'min_duration_ms': float('inf'),
                'max_duration_ms': 0
            }
        }
        
        # Create client instance
        client_kwargs = {
            'server_url': self.config['server_url'],
            'timeout': self.config.get('timeout')
        }
        
        if 'api_key' in self.config and self.config['api_key']:
            client_kwargs['api_key'] = self.config['api_key']
            
        # Add additional client options if provided
        if 'client_options' in self.config:
            client_kwargs.update(self.config['client_options'])
            
        # Create the client
        self.client = windsweeper.create_client(**client_kwargs)
    
    def _get_sdk_version(self) -> str:
        """Get the SDK version."""
        try:
            import pkg_resources
            return pkg_resources.get_distribution("windsweeper").version
        except Exception:
            return "unknown"
    
    def add(self, name: str, test_fn: BenchmarkTestFn) -> 'Benchmark':
        """
        Add a test case to the benchmark suite.
        
        Args:
            name: Name of the test case
            test_fn: Test function that performs the operation to benchmark
            
        Returns:
            The benchmark instance for chaining
        """
        self.tests[name] = test_fn
        return self
    
    async def _run_test(self, name: str, test_fn: BenchmarkTestFn) -> BenchmarkResult:
        """
        Run a single benchmark test.
        
        Args:
            name: Name of the test
            test_fn: Test function
            
        Returns:
            Benchmark result with performance metrics
        """
        print(f"Running test: {name}")
        
        try:
            # Warm up if configured
            if self.config['warmup'] and self.config['warmup_iterations'] > 0:
                print(f"  Warming up ({self.config['warmup_iterations']} iterations)...")
                for i in range(self.config['warmup_iterations']):
                    await test_fn(self.client, i)
            
            # Measure memory before test if configured
            memory_before = None
            memory_after = None
            
            if self.config['measure_memory']:
                gc.collect()  # Force garbage collection
                memory_before = self._get_memory_usage()
            
            # Run the actual benchmark
            print(f"  Running benchmark ({self.config['iterations']} iterations)...")
            
            start_time = time.time()
            
            for i in range(self.config['iterations']):
                await test_fn(self.client, i)
            
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            
            # Measure memory after test if configured
            if self.config['measure_memory']:
                gc.collect()  # Force garbage collection
                memory_after = self._get_memory_usage()
            
            # Calculate results
            operations = self.config['iterations']
            ops_per_second = operations / (duration_ms / 1000)
            
            result = {
                'name': name,
                'success': True,
                'duration_ms': duration_ms,
                'operations': operations,
                'ops_per_second': ops_per_second,
            }
            
            # Add memory metrics if measured
            if memory_before is not None and memory_after is not None:
                result['memory_before'] = memory_before
                result['memory_after'] = memory_after
                result['memory_diff'] = memory_after - memory_before
            
            print(f"  ✓ Completed in {duration_ms:.2f}ms ({ops_per_second:.2f} ops/sec)")
            
            return result
        
        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
            
            return {
                'name': name,
                'success': False,
                'duration_ms': 0,
                'operations': 0,
                'ops_per_second': 0,
                'error': str(e)
            }
    
    def _get_memory_usage(self) -> int:
        """
        Get current memory usage in bytes.
        
        Returns:
            Current memory usage in bytes
        """
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss
        except ImportError:
            # If psutil is not available, return 0
            return 0
    
    async def run(self) -> BenchmarkReport:
        """
        Run all benchmark tests.
        
        Returns:
            Benchmark report with results
        """
        print(f"Starting benchmark: {self.config['name']}")
        print(f"Running {len(self.tests)} tests with {self.config['iterations']} iterations each")
        
        # Reset results
        self.report['results'] = []
        
        # Run each test
        for name, test_fn in self.tests.items():
            result = await self._run_test(name, test_fn)
            self.report['results'].append(result)
            
            # Update summary
            self.report['summary']['total_tests'] += 1
            if result['success']:
                self.report['summary']['passed'] += 1
            else:
                self.report['summary']['failed'] += 1
            
            self.report['summary']['total_duration_ms'] += result['duration_ms']
            self.report['summary']['min_duration_ms'] = min(
                self.report['summary']['min_duration_ms'], 
                result['duration_ms'] if result['success'] else float('inf')
            )
            self.report['summary']['max_duration_ms'] = max(
                self.report['summary']['max_duration_ms'], 
                result['duration_ms'] if result['success'] else 0
            )
        
        # Calculate average duration
        if self.report['summary']['total_tests'] > 0:
            self.report['summary']['avg_duration_ms'] = (
                self.report['summary']['total_duration_ms'] / 
                self.report['summary']['total_tests']
            )
        
        # Handle case where no tests passed
        if self.report['summary']['min_duration_ms'] == float('inf'):
            self.report['summary']['min_duration_ms'] = 0
        
        return self.report
    
    def get_report(self) -> BenchmarkReport:
        """
        Get the benchmark report.
        
        Returns:
            The benchmark report
        """
        return self.report
    
    def save_report(self, path: str) -> None:
        """
        Save the benchmark report to a file.
        
        Args:
            path: File path to save the report to
        """
        with open(path, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"Benchmark report saved to {path}")
    
    def format_report(self) -> str:
        """
        Generate a formatted report.
        
        Returns:
            Formatted report as a string
        """
        report = self.report
        output = []
        
        output.append(f"# Benchmark Report: {report['name']}")
        output.append("")
        output.append(f"Date: {datetime.fromisoformat(report['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Environment: Python {report['environment']['python_version']} ({report['environment']['platform']} {report['environment']['platform_version']})")
        output.append(f"SDK Version: {report['environment']['sdk_version']}")
        output.append("")
        
        output.append("## Summary")
        output.append("")
        output.append(f"- Total Tests: {report['summary']['total_tests']}")
        output.append(f"- Passed: {report['summary']['passed']}")
        output.append(f"- Failed: {report['summary']['failed']}")
        output.append(f"- Total Duration: {report['summary']['total_duration_ms']:.2f}ms")
        output.append(f"- Average Duration: {report['summary']['avg_duration_ms']:.2f}ms")
        output.append(f"- Min Duration: {report['summary']['min_duration_ms']:.2f}ms" if report['summary']['min_duration_ms'] < float('inf') else "- Min Duration: N/A")
        output.append(f"- Max Duration: {report['summary']['max_duration_ms']:.2f}ms")
        output.append("")
        
        output.append("## Test Results")
        output.append("")
        output.append("| Test | Status | Duration (ms) | Ops/Sec | Memory Δ |")
        output.append("|------|--------|--------------|---------|----------|")
        
        for result in report['results']:
            status = "✓ Pass" if result['success'] else "✗ Fail"
            
            memory_diff = "N/A"
            if 'memory_diff' in result and result['memory_diff'] is not None:
                memory_diff = f"{result['memory_diff'] / (1024 * 1024):.2f} MB"
            
            output.append(f"| {result['name']} | {status} | {result['duration_ms']:.2f} | {result['ops_per_second']:.2f} | {memory_diff} |")
        
        return "\n".join(output)


def create_benchmark(config: BenchmarkConfig) -> Benchmark:
    """
    Create and configure a new benchmark suite.
    
    Args:
        config: Benchmark configuration
        
    Returns:
        A new benchmark instance
    """
    return Benchmark(config)
