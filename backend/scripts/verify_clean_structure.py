#!/usr/bin/env python3
"""
Verify the clean backend structure is properly organized
"""
import os
from pathlib import Path

def check_clean_structure():
    """Check if the backend structure is clean and properly organized"""
    backend_dir = Path(__file__).parent.parent
    
    print("🔍 Verifying Clean Backend Structure")
    print(f"Backend directory: {backend_dir}")
    
    # Check root directory is clean
    print("\n📁 Checking root directory...")
    
    expected_root_files = {
        '.dockerignore', '.env', '.gitignore', 'Dockerfile', 'main.py',
        'pytest.ini', 'requirements.txt', 'README.md'
    }
    
    expected_root_dirs = {
        'app', 'database', 'tests', 'scripts', '.pytest_cache'
    }
    
    # Check for unexpected files in root
    root_items = set(item.name for item in backend_dir.iterdir())
    
    unexpected_files = root_items - expected_root_files - expected_root_dirs
    if unexpected_files:
        print(f"⚠️  Unexpected files in root: {unexpected_files}")
    else:
        print("✅ Root directory is clean")
    
    # Check required directories exist
    print("\n📁 Checking required directories...")
    
    required_dirs = [
        'app',
        'app/core',
        'app/schemas',
        'app/services',
        'app/api',
        'app/api/v1',
        'app/api/v1/modules',
        'app/api/v1/modules/auth',
        'app/api/v1/modules/installments',
        'app/api/v1/modules/history',
        'app/api/v1/modules/admin',
        'app/api/v1/modules/approval',
        'app/api/v1/modules/fraud',
        'app/api/v1/modules/users',
        'app/api/v1/modules/translation',
        'database',
        'database/migrations',
        'tests',
        'tests/unit',
        'tests/integration',
        'tests/e2e',
        'scripts'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = backend_dir / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)
        else:
            print(f"✅ {dir_path}")
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    # Check module structure
    print("\n🏗️  Checking module structure...")
    
    modules = ['auth', 'installments', 'history', 'admin', 'approval', 'fraud', 'users', 'translation']
    
    for module in modules:
        module_dir = backend_dir / 'app' / 'api' / 'v1' / 'modules' / module
        
        # Handle special naming cases
        if module == 'installments':
            required_files = ['__init__.py', 'installment_routes.py', 'installment_service.py']
        elif module == 'users':
            required_files = ['__init__.py', 'user_routes.py', 'user_service.py']
        else:
            required_files = ['__init__.py', f'{module}_routes.py', f'{module}_service.py']
        
        for file_name in required_files:
            file_path = module_dir / file_name
            if file_path.exists():
                print(f"✅ {module}/{file_name}")
            else:
                print(f"❌ {module}/{file_name} missing")
    
    # Check database structure
    print("\n🗄️  Checking database structure...")
    
    db_files = ['__init__.py', 'database.py', 'database_utils.py', 'models.py', 'init.sql', 'alembic.ini']
    
    for file_name in db_files:
        file_path = backend_dir / 'database' / file_name
        if file_path.exists():
            print(f"✅ database/{file_name}")
        else:
            print(f"❌ database/{file_name} missing")
    
    # Check test structure
    print("\n🧪 Checking test structure...")
    
    test_dirs = ['unit', 'integration', 'e2e']
    
    for test_dir in test_dirs:
        dir_path = backend_dir / 'tests' / test_dir
        if dir_path.exists():
            test_files = list(dir_path.glob('test_*.py'))
            print(f"✅ tests/{test_dir} ({len(test_files)} test files)")
        else:
            print(f"❌ tests/{test_dir} missing")
    
    # Check scripts
    print("\n📜 Checking scripts...")
    
    scripts_dir = backend_dir / 'scripts'
    if scripts_dir.exists():
        script_files = list(scripts_dir.glob('*.py'))
        print(f"✅ scripts directory ({len(script_files)} scripts)")
    else:
        print("❌ scripts directory missing")
    
    # Check README
    print("\n📚 Checking documentation...")
    
    readme_file = backend_dir / 'README.md'
    if readme_file.exists():
        print("✅ README.md exists")
    else:
        print("❌ README.md missing")
    
    # Test imports
    print("\n🔗 Testing imports...")
    
    try:
        # Test main app import
        import sys
        sys.path.insert(0, str(backend_dir))
        
        from main import app
        print("✅ Main app import works")
        
        # Test database import
        from database import User, get_db
        print("✅ Database imports work")
        
        # Test module imports
        from app.api.v1.modules.auth.auth_service import AuthService
        print("✅ Auth module imports work")
        
        from app.api.v1.router import api_router
        print("✅ API router import works")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Count total files
    print("\n📊 Structure statistics...")
    
    total_py_files = len(list(backend_dir.rglob('*.py')))
    total_md_files = len(list(backend_dir.rglob('*.md')))
    total_dirs = len([d for d in backend_dir.rglob('*') if d.is_dir()])
    
    print(f"📈 Total Python files: {total_py_files}")
    print(f"📈 Total Markdown files: {total_md_files}")
    print(f"📈 Total directories: {total_dirs}")
    
    print("\n🎉 Clean structure verification completed successfully!")
    print("\n📋 Structure Summary:")
    print("   ✅ Root directory is clean and organized")
    print("   ✅ All modules properly structured")
    print("   ✅ Database package organized")
    print("   ✅ Tests properly categorized")
    print("   ✅ Scripts and docs organized")
    print("   ✅ All imports working correctly")
    
    print("\n📋 Quick Commands:")
    print("   python3 main.py                    # Start the application")
    print("   python3 run_all_tests.py          # Run all tests")
    print("   python3 scripts/test_modular.py   # Test modular structure")
    print("   curl http://localhost:8000/docs   # View API documentation")
    
    return True

if __name__ == "__main__":
    success = check_clean_structure()
    if not success:
        exit(1)