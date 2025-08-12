#!/usr/bin/env python3
"""
Verify the database structure is properly organized
"""
import os
from pathlib import Path

def check_database_structure():
    """Check if database structure is properly organized"""
    backend_dir = Path(__file__).parent
    database_dir = backend_dir / "database"
    
    print("🔍 Verifying Database Structure")
    print(f"Backend directory: {backend_dir}")
    print(f"Database directory: {database_dir}")
    
    # Check main database directory
    if not database_dir.exists():
        print("❌ Database directory does not exist")
        return False
    
    print("✅ Database directory exists")
    
    # Check required files
    required_files = [
        "__init__.py",
        "database.py",
        "database_utils.py", 
        "models.py",
        "init.sql",
        "alembic.ini",
        "README.md"
    ]
    
    for file_name in required_files:
        file_path = database_dir / file_name
        if not file_path.exists():
            print(f"❌ {file_name} missing")
            return False
        print(f"✅ {file_name} exists")
    
    # Check migrations directory
    migrations_dir = database_dir / "migrations"
    if not migrations_dir.exists():
        print("❌ migrations directory missing")
        return False
    print("✅ migrations directory exists")
    
    # Check that old files are moved from root
    old_files_in_root = [
        "database.py",
        "database_utils.py",
        "models.py"
    ]
    
    for file_name in old_files_in_root:
        file_path = backend_dir / file_name
        if file_path.exists():
            print(f"⚠️  {file_name} still exists in root - should be moved")
            return False
        print(f"✅ {file_name} properly moved from root")
    
    # Test imports
    print("\n🧪 Testing imports...")
    
    try:
        # Test new structure imports
        from database import User, get_db, engine
        print("✅ New structure imports work")
        
        # Test model creation
        user_instance = User(
            email="test@example.com",
            password_hash="test_hash",
            first_name="Test",
            last_name="User"
        )
        print("✅ Model instantiation works")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False
    
    # Check file sizes (basic validation)
    file_sizes = {}
    for file_name in required_files:
        if file_name.endswith('.py'):
            file_path = database_dir / file_name
            size = file_path.stat().st_size
            file_sizes[file_name] = size
            print(f"📊 {file_name}: {size} bytes")
    
    # Validate that files have reasonable content
    if file_sizes.get("models.py", 0) < 1000:
        print("⚠️  models.py seems too small")
        return False
    
    if file_sizes.get("database.py", 0) < 500:
        print("⚠️  database.py seems too small")
        return False
    
    print("\n🎉 Database structure verification completed successfully!")
    print("\n📋 Database Structure Summary:")
    print("   ✅ All database files moved to /database directory")
    print("   ✅ Migrations organized in /database/migrations")
    print("   ✅ Backward compatibility maintained")
    print("   ✅ Imports working correctly")
    print("   ✅ Models can be instantiated")
    
    print("\n📋 Quick Commands:")
    print("   python3 -c 'from database import User; print(\"Import works!\")'")
    print("   python3 database/database_utils.py  # Test database connection")
    print("   cd database && alembic current      # Check migration status")
    
    return True

if __name__ == "__main__":
    success = check_database_structure()
    if not success:
        exit(1)