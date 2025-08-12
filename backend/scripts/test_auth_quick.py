#!/usr/bin/env python3
"""
Quick authentication test runner
"""
import subprocess
import sys
import os

def main():
    """Run quick auth tests"""
    print("🧪 Running Quick Authentication Tests")
    
    # Change to backend directory
    os.chdir(os.path.dirname(__file__))
    
    # Install dependencies if needed
    print("📦 Installing test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], 
                  capture_output=True)
    
    # Run specific test classes
    test_commands = [
        "pytest tests/test_auth_e2e.py::TestUserRegistration::test_register_customer_success -v",
        "pytest tests/test_auth_e2e.py::TestUserLogin::test_login_success -v",
        "pytest tests/test_auth_e2e.py::TestUserLogin::test_login_nonexistent_user -v",
        "pytest tests/test_auth_e2e.py::TestAuthenticationFlow::test_register_login_flow -v"
    ]
    
    for cmd in test_commands:
        print(f"\n▶️  {cmd}")
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            print(result.stdout)
            print(result.stderr)

if __name__ == "__main__":
    main()