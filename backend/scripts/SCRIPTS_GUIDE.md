# Scripts Guide

## Overview

This directory contains utility scripts for testing, verification, and maintenance of the Installment Fraud Detection System backend.

## Script Categories

### Test Runners
- **run_all_tests.py** - Comprehensive test runner with multiple options
- **run_tests.py** - Legacy test runner for E2E tests
- **test_auth_quick.py** - Quick authentication test runner
- **test_auth_simple.py** - Simple authentication tests using requests
- **test_modular.py** - Test runner for modular structure

### Structure Verification
- **verify_clean_structure.py** - Verify overall backend structure
- **verify_database_structure.py** - Verify database organization
- **verify_modular_structure.py** - Verify API module structure
- **verify_test_structure.py** - Verify test organization

### Debugging
- **debug_auth.py** - Debug authentication issues

## Detailed Script Documentation

### run_all_tests.py
**Purpose**: Comprehensive test runner with advanced options

**Features**:
- Run all test types (unit, integration, e2e)
- Selective test execution by type
- Coverage reporting
- Verbose output options
- Skip slow tests option

**Usage**:
```bash
# Run all tests
python3 scripts/run_all_tests.py

# Run specific test type
python3 scripts/run_all_tests.py --type unit
python3 scripts/run_all_tests.py --type integration
python3 scripts/run_all_tests.py --type e2e

# With coverage report
python3 scripts/run_all_tests.py --coverage

# Verbose output
python3 scripts/run_all_tests.py --verbose

# Skip slow tests
python3 scripts/run_all_tests.py --fast
```

**Options**:
- `--type {unit,integration,e2e,all}`: Type of tests to run (default: all)
- `--coverage`: Generate coverage report
- `--verbose, -v`: Verbose output
- `--fast`: Skip slow tests

### test_auth_simple.py
**Purpose**: Simple authentication tests using direct HTTP requests

**Features**:
- User registration testing
- Login functionality testing
- Token refresh testing
- Protected endpoint access
- Error condition testing

**Usage**:
```bash
python3 scripts/test_auth_simple.py
```

**Test Cases**:
1. User registration
2. User login
3. Login with wrong password
4. Login with non-existent user
5. Protected endpoint access
6. Token refresh
7. Duplicate registration

### test_modular.py
**Purpose**: Test the modular backend structure

**Features**:
- Health check testing
- Modular API endpoint testing
- Authentication flow testing

**Usage**:
```bash
python3 scripts/test_modular.py
```

### verify_clean_structure.py
**Purpose**: Verify the overall backend structure is clean and organized

**Checks**:
- Root directory cleanliness
- Required directories exist
- Module structure compliance
- Database structure
- Test organization
- Import functionality

**Usage**:
```bash
python3 scripts/verify_clean_structure.py
```

**Verification Areas**:
1. **Root Directory**: Checks for unexpected files
2. **Module Structure**: Verifies all API modules exist with correct files
3. **Database Structure**: Confirms database package organization
4. **Test Structure**: Validates test directory organization
5. **Import Tests**: Ensures all imports work correctly

### verify_database_structure.py
**Purpose**: Verify database package organization

**Checks**:
- Database directory exists
- Required files present
- Old files moved from root
- Import functionality
- File content validation

**Usage**:
```bash
python3 scripts/verify_database_structure.py
```

### verify_modular_structure.py
**Purpose**: Verify API module structure

**Checks**:
- Module directories exist
- Required module files present
- Schema files exist
- Router configuration
- Import functionality
- Route counting

**Usage**:
```bash
python3 scripts/verify_modular_structure.py
```

### verify_test_structure.py
**Purpose**: Verify test organization

**Checks**:
- Test directories exist
- Test files present
- Old test directories removed
- Pytest configuration
- Test runners exist

**Usage**:
```bash
python3 scripts/verify_test_structure.py
```

### debug_auth.py
**Purpose**: Debug authentication issues

**Features**:
- Server health check
- Root endpoint testing
- Simple registration testing
- Detailed error reporting

**Usage**:
```bash
python3 scripts/debug_auth.py
```

## Quick Reference

### Common Tasks

#### Run All Tests
```bash
python3 scripts/run_all_tests.py
```

#### Run Specific Test Type
```bash
python3 scripts/run_all_tests.py --type unit
python3 scripts/run_all_tests.py --type integration
python3 scripts/run_all_tests.py --type e2e
```

#### Test with Coverage
```bash
python3 scripts/run_all_tests.py --coverage
```

#### Verify Structure
```bash
python3 scripts/verify_clean_structure.py
python3 scripts/verify_database_structure.py
python3 scripts/verify_modular_structure.py
python3 scripts/verify_test_structure.py
```

#### Debug Issues
```bash
python3 scripts/debug_auth.py
python3 scripts/test_auth_simple.py
python3 scripts/test_modular.py
```

### Script Dependencies

All scripts require:
- Python 3.8+
- Backend dependencies installed (`pip install -r requirements.txt`)
- Database connection (for database-related tests)
- Running server (for API tests)

### Exit Codes

All scripts follow standard exit code conventions:
- **0**: Success
- **1**: Failure/Error

### Output Format

Scripts provide structured output:
- ✅ Success indicators
- ❌ Failure indicators
- ⚠️ Warning indicators
- 📊 Statistics
- 📋 Summary information

## Script Development Guidelines

### Adding New Scripts

1. **Follow naming convention**: `verb_noun.py` (e.g., `test_auth.py`, `verify_structure.py`)
2. **Include docstring**: Describe purpose and usage
3. **Use consistent output**: Follow existing format with emoji indicators
4. **Handle errors gracefully**: Provide meaningful error messages
5. **Return appropriate exit codes**: 0 for success, 1 for failure
6. **Add to this guide**: Document new scripts

### Script Template
```python
#!/usr/bin/env python3
"""
Script description and purpose
"""
import sys
from pathlib import Path

def main():
    """Main function"""
    print("🚀 Starting Script Name")
    
    try:
        # Script logic here
        print("✅ Script completed successfully")
        return True
    except Exception as e:
        print(f"❌ Script failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

### Best Practices

1. **Make scripts executable**: `chmod +x script_name.py`
2. **Use shebang line**: `#!/usr/bin/env python3`
3. **Handle keyboard interrupts**: Graceful shutdown on Ctrl+C
4. **Provide progress indicators**: Show what the script is doing
5. **Include help text**: Document command-line options
6. **Test scripts thoroughly**: Ensure they work in different environments

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure you're in the backend directory
cd backend

# Check Python path
python3 -c "import sys; print(sys.path)"

# Verify structure
python3 scripts/verify_clean_structure.py
```

#### Database Connection Issues
```bash
# Check database connection
python3 -c "from database.database_utils import check_database_connection; print(check_database_connection())"

# Verify environment variables
echo $DATABASE_URL
```

#### Server Not Running
```bash
# Start the server
python3 main.py

# Check if server is running
curl http://localhost:8000/health
```

#### Permission Issues
```bash
# Make scripts executable
chmod +x scripts/*.py

# Check file permissions
ls -la scripts/
```

### Getting Help

For script-specific help:
```bash
python3 scripts/script_name.py --help
```

For general issues:
1. Check the script's docstring for usage information
2. Verify all dependencies are installed
3. Ensure the backend server is running (for API tests)
4. Check database connectivity (for database tests)
5. Review the script output for specific error messages

This guide provides comprehensive documentation for all utility scripts in the backend system, making it easy to maintain, test, and verify the system's integrity.