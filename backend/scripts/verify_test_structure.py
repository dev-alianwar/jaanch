#!/usr/bin/env python3
"""
Verify the test structure is properly organized
"""
import os
from pathlib import Path

def check_test_structure():
    """Check if test structure is properly organized"""
    backend_dir = Path(__file__).parent
    tests_dir = backend_dir / "tests"
    
    print("🔍 Verifying Test Structure")
    print(f"Backend directory: {backend_dir}")
    print(f"Tests directory: {tests_dir}")
    
    # Check main test directory
    if not tests_dir.exists():
        print("❌ Tests directory does not exist")
        return False
    
    print("✅ Tests directory exists")
    
    # Check subdirectories
    required_dirs = ["unit", "integration", "e2e"]
    for dir_name in required_dirs:
        dir_path = tests_dir / dir_name
        if not dir_path.exists():
            print(f"❌ {dir_name} directory missing")
            return False
        print(f"✅ {dir_name} directory exists")
        
        # Check __init__.py
        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            print(f"❌ {dir_name}/__init__.py missing")
            return False
        print(f"✅ {dir_name}/__init__.py exists")
    
    # Check required files
    required_files = [
        "conftest.py",
        "README.md",
        "__init__.py"
    ]
    
    for file_name in required_files:
        file_path = tests_dir / file_name
        if not file_path.exists():
            print(f"❌ {file_name} missing")
            return False
        print(f"✅ {file_name} exists")
    
    # Check test files exist
    test_files = [
        "unit/test_security.py",
        "unit/test_models.py", 
        "unit/test_schemas.py",
        "integration/test_auth_service.py",
        "integration/test_database.py",
        "integration/test_auth_modular.py",
        "e2e/test_auth_flow.py"
    ]
    
    for test_file in test_files:
        file_path = tests_dir / test_file
        if not file_path.exists():
            print(f"❌ {test_file} missing")
            return False
        print(f"✅ {test_file} exists")
    
    # Check for old tests_new directory
    tests_new_dir = backend_dir / "tests_new"
    if tests_new_dir.exists():
        print("⚠️  tests_new directory still exists - should be removed")
        return False
    
    print("✅ tests_new directory properly removed")
    
    # Count total test files
    total_tests = 0
    for test_file in test_files:
        file_path = tests_dir / test_file
        with open(file_path, 'r') as f:
            content = f.read()
            # Count test methods
            test_count = content.count("def test_")
            total_tests += test_count
            print(f"📊 {test_file}: {test_count} tests")
    
    print(f"\n📈 Total test methods found: {total_tests}")
    
    # Check pytest configuration
    pytest_ini = backend_dir / "pytest.ini"
    if pytest_ini.exists():
        print("✅ pytest.ini configuration exists")
    else:
        print("❌ pytest.ini configuration missing")
        return False
    
    # Check test runners
    test_runners = [
        "run_all_tests.py",
        "run_tests.py"
    ]
    
    for runner in test_runners:
        runner_path = backend_dir / runner
        if runner_path.exists():
            print(f"✅ {runner} test runner exists")
        else:
            print(f"⚠️  {runner} test runner missing")
    
    print("\n🎉 Test structure verification completed successfully!")
    print("\n📋 Quick Commands:")
    print("   python3 -m pytest tests/unit/ -v          # Run unit tests")
    print("   python3 -m pytest tests/integration/ -v   # Run integration tests") 
    print("   python3 -m pytest tests/e2e/ -v           # Run E2E tests")
    print("   python3 run_all_tests.py                   # Run all tests")
    print("   python3 -m pytest -m auth -v              # Run auth tests only")
    
    return True

if __name__ == "__main__":
    success = check_test_structure()
    if not success:
        exit(1)