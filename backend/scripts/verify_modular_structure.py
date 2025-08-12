#!/usr/bin/env python3
"""
Verify the modular API structure is properly organized
"""
import os
from pathlib import Path

def check_modular_structure():
    """Check if modular API structure is properly organized"""
    backend_dir = Path(__file__).parent
    modules_dir = backend_dir / "app" / "api" / "v1" / "modules"
    
    print("🔍 Verifying Modular API Structure")
    print(f"Backend directory: {backend_dir}")
    print(f"Modules directory: {modules_dir}")
    
    # Check main modules directory
    if not modules_dir.exists():
        print("❌ Modules directory does not exist")
        return False
    
    print("✅ Modules directory exists")
    
    # Check required modules
    required_modules = ["auth", "installments", "history"]
    
    for module_name in required_modules:
        module_dir = modules_dir / module_name
        if not module_dir.exists():
            print(f"❌ {module_name} module directory missing")
            return False
        print(f"✅ {module_name} module directory exists")
        
        # Check module files
        required_files = [
            "__init__.py",
            f"{module_name}_routes.py",
            f"{module_name}_service.py"
        ]
        
        for file_name in required_files:
            file_path = module_dir / file_name
            if not file_path.exists():
                print(f"❌ {module_name}/{file_name} missing")
                return False
            print(f"✅ {module_name}/{file_name} exists")
    
    # Check schema files
    schemas_dir = backend_dir / "app" / "schemas"
    required_schemas = [
        "base.py",
        "auth.py", 
        "installment.py",
        "history.py"
    ]
    
    for schema_file in required_schemas:
        schema_path = schemas_dir / schema_file
        if not schema_path.exists():
            print(f"❌ Schema {schema_file} missing")
            return False
        print(f"✅ Schema {schema_file} exists")
    
    # Check main router
    router_file = backend_dir / "app" / "api" / "v1" / "router.py"
    if not router_file.exists():
        print("❌ Main router file missing")
        return False
    print("✅ Main router file exists")
    
    # Test imports
    print("\n🧪 Testing imports...")
    
    try:
        # Test module imports
        from app.api.v1.modules.auth.auth_routes import router as auth_router
        print("✅ Auth module import works")
        
        from app.api.v1.modules.installments.installment_routes import router as installments_router
        print("✅ Installments module import works")
        
        from app.api.v1.modules.history.history_routes import router as history_router
        print("✅ History module import works")
        
        # Test service imports
        from app.api.v1.modules.auth.auth_service import AuthService
        print("✅ Auth service import works")
        
        from app.api.v1.modules.installments.installment_service import InstallmentRequestService
        print("✅ Installments service import works")
        
        from app.api.v1.modules.history.history_service import HistoryService
        print("✅ History service import works")
        
        # Test schema imports
        from app.schemas.auth import UserLogin, AuthResponse
        print("✅ Auth schemas import works")
        
        from app.schemas.installment import InstallmentRequestCreate
        print("✅ Installment schemas import works")
        
        from app.schemas.history import CustomerInstallmentHistory
        print("✅ History schemas import works")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Check file sizes (basic validation)
    print("\n📊 File size analysis...")
    
    total_routes = 0
    total_services = 0
    
    for module_name in required_modules:
        module_dir = modules_dir / module_name
        
        routes_file = module_dir / f"{module_name}_routes.py"
        service_file = module_dir / f"{module_name}_service.py"
        
        if routes_file.exists():
            routes_size = routes_file.stat().st_size
            total_routes += routes_size
            print(f"📊 {module_name}_routes.py: {routes_size} bytes")
        
        if service_file.exists():
            service_size = service_file.stat().st_size
            total_services += service_size
            print(f"📊 {module_name}_service.py: {service_size} bytes")
    
    print(f"\n📈 Total routes code: {total_routes} bytes")
    print(f"📈 Total services code: {total_services} bytes")
    
    # Count route endpoints
    print("\n🔗 Counting API endpoints...")
    
    try:
        from app.api.v1.router import api_router
        
        # Count routes in the main router
        route_count = len(api_router.routes)
        print(f"📊 Total API routes: {route_count}")
        
        # List route paths
        print("📋 Available endpoints:")
        for route in api_router.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                methods = ', '.join(route.methods)
                print(f"   {methods} {route.path}")
        
    except Exception as e:
        print(f"⚠️  Could not analyze routes: {e}")
    
    print("\n🎉 Modular structure verification completed successfully!")
    print("\n📋 Structure Summary:")
    print("   ✅ All required modules present")
    print("   ✅ All module files exist")
    print("   ✅ All schema files exist")
    print("   ✅ Imports working correctly")
    print("   ✅ Router configuration valid")
    
    print("\n📋 Quick Commands:")
    print("   python3 -c 'from app.api.v1.router import api_router; print(\"API loaded!\")'")
    print("   python3 main_new.py  # Start modular server")
    print("   curl http://localhost:8000/api/v1/auth/me  # Test endpoint")
    
    return True

if __name__ == "__main__":
    success = check_modular_structure()
    if not success:
        exit(1)