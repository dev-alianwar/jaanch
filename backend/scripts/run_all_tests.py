#!/usr/bin/env python3
"""
Comprehensive test runner for all test types
"""
import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_command(command, description, capture_output=False):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    if capture_output:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
    else:
        result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"❌ {description} failed with return code {result.returncode}")
        return False
    else:
        print(f"✅ {description} completed successfully")
        return True

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Run tests for the backend")
    parser.add_argument("--type", choices=["unit", "integration", "e2e", "all"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--coverage", action="store_true", 
                       help="Run with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--fast", action="store_true", 
                       help="Skip slow tests")
    
    args = parser.parse_args()
    
    print("🚀 Starting Comprehensive Test Suite")
    print(f"Test type: {args.type}")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Install test dependencies
    print("📦 Installing test dependencies...")
    if not run_command("python3 -m pip install -r requirements-test.txt", 
                      "Installing test dependencies", capture_output=True):
        print("⚠️  Failed to install dependencies, continuing anyway...")
    
    # Build base pytest command
    base_cmd = "python3 -m pytest"
    
    if args.verbose:
        base_cmd += " -v"
    
    if args.coverage:
        base_cmd += " --cov=app --cov-report=term-missing --cov-report=html"
    
    if args.fast:
        base_cmd += " -m 'not slow'"
    
    # Test commands based on type
    test_commands = []
    
    if args.type == "unit" or args.type == "all":
        test_commands.append({
            "command": f"{base_cmd} tests/unit/ -m unit",
            "description": "Unit Tests"
        })
    
    if args.type == "integration" or args.type == "all":
        test_commands.append({
            "command": f"{base_cmd} tests/integration/ -m integration",
            "description": "Integration Tests"
        })
    
    if args.type == "e2e" or args.type == "all":
        test_commands.append({
            "command": f"{base_cmd} tests/e2e/ -m e2e",
            "description": "End-to-End Tests"
        })
    
    # If running all tests, also run legacy tests
    if args.type == "all":
        test_commands.append({
            "command": f"{base_cmd} tests/test_auth_e2e.py",
            "description": "Legacy E2E Tests"
        })
    
    # Run tests
    failed_tests = []
    
    for test in test_commands:
        if not run_command(test["command"], test["description"]):
            failed_tests.append(test["description"])
    
    # Run specific test categories
    if args.type == "all":
        additional_tests = [
            {
                "command": f"{base_cmd} -m auth",
                "description": "Authentication Tests"
            },
            {
                "command": f"{base_cmd} -m database",
                "description": "Database Tests"
            }
        ]
        
        for test in additional_tests:
            if not run_command(test["command"], test["description"]):
                failed_tests.append(test["description"])
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    total_tests = len(test_commands)
    if args.type == "all":
        total_tests += 2  # Additional test categories
    
    if failed_tests:
        print(f"❌ {len(failed_tests)} test suite(s) failed:")
        for test in failed_tests:
            print(f"   - {test}")
        print(f"✅ {total_tests - len(failed_tests)} test suite(s) passed")
        
        print("\n📋 Quick Commands to Run Failed Tests:")
        for test in failed_tests:
            if "Unit Tests" in test:
                print("   python3 -m pytest tests/unit/ -v")
            elif "Integration Tests" in test:
                print("   python3 -m pytest tests/integration/ -v")
            elif "End-to-End Tests" in test:
                print("   python3 -m pytest tests/e2e/ -v")
        
        sys.exit(1)
    else:
        print(f"✅ All {total_tests} test suites passed!")
        
        if args.coverage:
            print("\n📊 Coverage report generated in htmlcov/index.html")
        
        print("\n🎉 All tests completed successfully!")

if __name__ == "__main__":
    main()