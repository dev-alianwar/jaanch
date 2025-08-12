#!/usr/bin/env python3
"""
Test runner script for the Installment Fraud Detection System
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"❌ {description} failed with return code {result.returncode}")
        return False
    else:
        print(f"✅ {description} completed successfully")
        return True

def main():
    """Main test runner"""
    print("🚀 Starting Installment Fraud Detection System Tests")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Install test dependencies
    if not run_command("pip install -r requirements-test.txt", "Installing test dependencies"):
        sys.exit(1)
    
    # Run different types of tests
    test_commands = [
        {
            "command": "pytest tests/test_auth_e2e.py -v -m 'not slow'",
            "description": "Authentication E2E Tests (Fast)"
        },
        {
            "command": "pytest tests/test_auth_e2e.py::TestUserRegistration -v",
            "description": "User Registration Tests"
        },
        {
            "command": "pytest tests/test_auth_e2e.py::TestUserLogin -v",
            "description": "User Login Tests"
        },
        {
            "command": "pytest tests/test_auth_e2e.py::TestTokenRefresh -v",
            "description": "Token Refresh Tests"
        },
        {
            "command": "pytest tests/test_auth_e2e.py::TestAuthenticationFlow -v",
            "description": "Authentication Flow Tests"
        },
        {
            "command": "pytest tests/test_auth_e2e.py::TestAuthenticationSecurity -v",
            "description": "Authentication Security Tests"
        }
    ]
    
    failed_tests = []
    
    for test in test_commands:
        if not run_command(test["command"], test["description"]):
            failed_tests.append(test["description"])
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if failed_tests:
        print(f"❌ {len(failed_tests)} test suite(s) failed:")
        for test in failed_tests:
            print(f"   - {test}")
        print(f"✅ {len(test_commands) - len(failed_tests)} test suite(s) passed")
        sys.exit(1)
    else:
        print(f"✅ All {len(test_commands)} test suites passed!")
        print("\n🎉 All tests completed successfully!")

if __name__ == "__main__":
    main()