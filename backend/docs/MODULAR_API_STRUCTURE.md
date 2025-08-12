# Modular API Structure

This document describes the new modular API structure for the Installment Fraud Detection System backend.

## Directory Structure

```
backend/app/api/v1/modules/
├── auth/
│   ├── __init__.py
│   ├── auth_routes.py          # Authentication API routes
│   └── auth_service.py         # Authentication business logic
├── installments/
│   ├── __init__.py
│   ├── installment_routes.py   # Installment request API routes
│   └── installment_service.py  # Installment business logic
├── history/
│   ├── __init__.py
│   ├── history_routes.py       # Customer history API routes
│   └── history_service.py      # History business logic
└── [future modules]/
    ├── __init__.py
    ├── [module]_routes.py
    └── [module]_service.py
```

## Module Structure

Each module follows a consistent pattern:

### 1. Routes File (`*_routes.py`)
- Contains FastAPI route definitions
- Handles HTTP requests and responses
- Performs input validation
- Manages authentication and authorization
- Calls service layer for business logic

### 2. Service File (`*_service.py`)
- Contains business logic
- Database operations
- Data processing and validation
- Integration with other services
- No direct HTTP handling

### 3. Module Init (`__init__.py`)
- Module package initialization
- Can export commonly used components

## Current Modules

### Auth Module (`/auth`)
**Routes:**
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user info

**Service:** `AuthService`
- User registration with validation
- User authentication
- JWT token management
- Password hashing

### Installments Module (`/installments`)
**Routes:**
- `GET /api/v1/installments/businesses` - Get available businesses
- `POST /api/v1/installments/requests` - Create installment request
- `GET /api/v1/installments/requests` - Get installment requests (paginated)
- `GET /api/v1/installments/requests/{id}` - Get specific request
- `PUT /api/v1/installments/requests/{id}` - Update request
- `DELETE /api/v1/installments/requests/{id}` - Cancel request

**Services:** 
- `InstallmentRequestService` - Request management
- `BusinessService` - Business operations

### History Module (`/history`)
**Routes:**
- `GET /api/v1/history/customer/{id}` - Get customer history
- `GET /api/v1/history/my-history` - Get personal history
- `GET /api/v1/history/active-plans` - Get active plans
- `GET /api/v1/history/payment-history` - Get payment history

**Service:** `HistoryService`
- Customer history aggregation
- Cross-business analysis
- Risk score calculation

## Benefits of Modular Structure

### 1. **Organization**
- Clear separation of concerns
- Easy to locate functionality
- Logical grouping of related features

### 2. **Maintainability**
- Changes isolated to specific modules
- Easier debugging and testing
- Clear dependency management

### 3. **Scalability**
- Easy to add new modules
- Independent development of features
- Parallel development possible

### 4. **Reusability**
- Services can be reused across routes
- Common patterns established
- Consistent error handling

### 5. **Testing**
- Unit tests for individual services
- Integration tests for route modules
- Isolated test environments

## Adding New Modules

To add a new module (e.g., `fraud`):

1. **Create module directory:**
   ```
   backend/app/api/v1/modules/fraud/
   ├── __init__.py
   ├── fraud_routes.py
   └── fraud_service.py
   ```

2. **Implement routes (`fraud_routes.py`):**
   ```python
   from fastapi import APIRouter, Depends
   from .fraud_service import FraudService
   
   router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])
   
   @router.get("/alerts")
   async def get_fraud_alerts():
       return FraudService.get_alerts()
   ```

3. **Implement service (`fraud_service.py`):**
   ```python
   class FraudService:
       @staticmethod
       def get_alerts():
           # Business logic here
           pass
   ```

4. **Add to main router (`router.py`):**
   ```python
   from .modules.fraud.fraud_routes import router as fraud_router
   api_router.include_router(fraud_router)
   ```

## Schema Organization

Schemas are organized by feature in `app/schemas/`:
- `auth.py` - Authentication schemas
- `installment.py` - Installment schemas
- `history.py` - History schemas
- `base.py` - Base schema classes

## Dependencies

Common dependencies are in `app/api/dependencies.py`:
- Authentication dependencies
- Authorization helpers
- Database session management

## Error Handling

Each module handles errors consistently:
- HTTP exceptions for client errors
- Logging for server errors
- Structured error responses

## Future Modules

Planned modules to be migrated:
- **Admin** (`/admin`) - Administrative functions
- **Fraud** (`/fraud`) - Fraud detection and alerts
- **Approval** (`/approval`) - Request approval workflows
- **User** (`/users`) - User management
- **Translation** (`/translation`) - Multi-language support

## Migration Strategy

1. **Phase 1** ✅ - Core modules (auth, installments, history)
2. **Phase 2** - Business logic modules (fraud, approval)
3. **Phase 3** - Administrative modules (admin, users)
4. **Phase 4** - Utility modules (translation, reporting)

## API Versioning

The modular structure supports API versioning:
- Current: `/api/v1/`
- Future: `/api/v2/` (when needed)
- Backward compatibility maintained

This modular structure provides a solid foundation for scaling the API while maintaining code quality and developer productivity.