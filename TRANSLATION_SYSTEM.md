# Translation System Documentation

## Overview

The InstallmentGuard system uses a database-driven internationalization (i18n) system that supports multiple languages with real-time updates through an admin portal.

## Features

### 🌐 Multi-Language Support
- **English (en)** - Default language
- **Urdu (ur)** - RTL support included
- Extensible to add more languages

### 🔧 Admin Management
- Dedicated admin portal at `/portal-admin`
- Visual translation editor
- Search and filter capabilities
- Category-based organization
- Real-time updates across all platforms

### 📱 Cross-Platform
- **Web Platform** (Next.js) - API-based translations
- **Mobile Apps** (React Native) - API-based with fallback
- **Admin Portal** - Separate authentication and management

## Architecture

### Backend Components

1. **Translation Models** (`backend/translation_models.py`)
   - `Translation` - Individual translation entries
   - `TranslationSet` - Optimized JSON storage for fast retrieval

2. **Translation Service** (`backend/translation_service.py`)
   - CRUD operations for translations
   - Automatic translation set updates
   - Default translation seeding

3. **Translation API** (`backend/translation_routes.py`)
   - Public endpoints for fetching translations
   - Admin endpoints for management (superadmin only)

### Frontend Components

1. **Web Platform** (`web/src/lib/translations.ts`)
   - API-based translation loading
   - Client-side caching
   - Fallback to static files

2. **Mobile App** (`mobile/src/i18n/`)
   - API integration with fallback
   - Initialization on app startup
   - Language switching support

## Database Schema

### Translations Table
```sql
CREATE TABLE translations (
    id UUID PRIMARY KEY,
    key VARCHAR(255) NOT NULL,           -- e.g., 'auth.login'
    locale VARCHAR(10) NOT NULL,         -- e.g., 'en', 'ur'
    value TEXT NOT NULL,                 -- Translation text
    category VARCHAR(100),               -- e.g., 'auth', 'dashboard'
    description TEXT,                    -- Context for translators
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Translation Sets Table
```sql
CREATE TABLE translation_sets (
    id UUID PRIMARY KEY,
    locale VARCHAR(10) NOT NULL,
    translations JSON NOT NULL,          -- Nested JSON structure
    version VARCHAR(50) DEFAULT '1.0.0',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## API Endpoints

### Public Endpoints

#### Get Translations by Locale
```http
GET /translations/locale/{locale}
```
Returns nested JSON structure of all translations for a locale.

**Response:**
```json
{
  "locale": "en",
  "translations": {
    "auth": {
      "login": "Login",
      "password": "Password"
    },
    "dashboard": {
      "welcome": "Welcome, {name}!"
    }
  }
}
```

### Admin Endpoints (Superadmin Only)

#### Get All Translations
```http
GET /translations/admin/all
Authorization: Bearer {admin_token}
```

#### Create Translation
```http
POST /translations/admin
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "key": "auth.newField",
  "locale": "en",
  "value": "New Field",
  "category": "auth",
  "description": "Optional description"
}
```

#### Update Translation
```http
PUT /translations/admin/{translation_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "value": "Updated Value",
  "description": "Updated description"
}
```

#### Delete Translation
```http
DELETE /translations/admin/{translation_id}
Authorization: Bearer {admin_token}
```

#### Seed Default Translations
```http
POST /translations/admin/seed
Authorization: Bearer {admin_token}
```

## Usage

### Automatic Startup Seeding

Translations are automatically seeded when the backend starts up:

1. **Database Initialization** - Creates tables if they don't exist
2. **Translation Check** - Checks if translations already exist
3. **Seeding** - Seeds default translations if none exist
4. **Translation Sets** - Creates optimized JSON sets for fast retrieval

### Admin Portal Access

1. **Login**: Visit `/portal-admin` with superadmin credentials
2. **Dashboard**: Overview of admin functions
3. **Translation Management**: Edit, add, delete translations
4. **Real-time Updates**: Changes are immediately available

### Web Platform Integration

```typescript
// Automatic API-based loading
import { useTranslations } from 'next-intl';

function MyComponent() {
  const t = useTranslations('auth');
  return <h1>{t('login')}</h1>;
}
```

### Mobile App Integration

```typescript
// Initialize translations on app start
import { initializeTranslations } from './src/i18n';

useEffect(() => {
  initializeTranslations();
}, []);

// Use translations
import i18n from './src/i18n';
const loginText = i18n.t('auth.login');
```

## Development

### Adding New Languages

1. **Add Locale**: Update locale arrays in middleware and configs
2. **Seed Translations**: Add translations to `translation_service.py`
3. **Update UI**: Add language option to switchers

### Adding New Translation Keys

1. **Via Admin Portal**: Use the web interface
2. **Via API**: POST to `/translations/admin`
3. **Via Seeding**: Add to `seed_default_translations()`

### Testing Translations

```bash
# Test translation endpoints
cd backend
python test_translations.py

# Check specific locale
curl http://localhost:8000/translations/locale/en
curl http://localhost:8000/translations/locale/ur
```

## Deployment

### Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://user:pass@host:port/db
CORS_ORIGINS='["http://localhost:3000", "http://localhost:3001"]'

# Web Platform
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docker Compose

```bash
# Start all services (includes automatic translation seeding)
docker-compose up

# Check logs for translation seeding
docker-compose logs backend | grep -i translation
```

## Troubleshooting

### Common Issues

1. **Translations Not Loading**
   - Check backend API connectivity
   - Verify CORS settings
   - Check browser network tab for API errors

2. **Admin Portal Access Denied**
   - Ensure user has `superadmin` role
   - Check JWT token validity
   - Verify admin authentication flow

3. **Missing Translations**
   - Run seed endpoint: `POST /translations/admin/seed`
   - Check database for translation entries
   - Verify translation key format

### Debug Commands

```bash
# Check backend health
curl http://localhost:8000/health

# Test translation loading
curl http://localhost:8000/translations/locale/en

# Check database
docker-compose exec postgres psql -U postgres -d installment_fraud_db -c "SELECT COUNT(*) FROM translations;"
```

## Performance Considerations

### Caching Strategy
- **Backend**: Translation sets stored as JSON for fast retrieval
- **Frontend**: Client-side caching with cache invalidation
- **Mobile**: Local storage with API sync

### Optimization
- Nested JSON structure reduces API calls
- Indexed database queries for fast lookups
- Lazy loading for non-critical translations

## Security

### Access Control
- Admin endpoints require superadmin role
- JWT token validation on all admin operations
- Separate admin authentication flow

### Data Protection
- SQL injection prevention through ORM
- Input validation on all endpoints
- Audit logging for translation changes

## Future Enhancements

### Planned Features
- Translation versioning and rollback
- Bulk import/export functionality
- Translation approval workflow
- Usage analytics and missing key detection
- Automated translation suggestions
- Multi-tenant translation management

### Scalability
- Redis caching for high-traffic scenarios
- CDN integration for static translations
- Database sharding for large translation sets
- Microservice architecture for translation service