# Installment Fraud Detection System

A comprehensive system to track installment purchases across multiple businesses and detect fraudulent chains where customers obtain products on installment, sell them for cash, and repeat the cycle.

## Features

### Core Functionality
- **Multi-role authentication** (superadmin, business, customer)
- **Installment request management** with business approval workflow
- **Cross-business customer history** for informed credit decisions
- **Advanced fraud detection** to identify installment chains
- **Real-time monitoring** and alerts
- **Comprehensive reporting** for superadmins

### Anti-Fraud Capabilities
- Track customers across multiple businesses
- Detect rapid installment request patterns
- Calculate total debt exposure
- Identify suspicious cash-out and re-purchase cycles
- Risk scoring for each customer
- Automated fraud alerts

## Project Structure

```
project/
├── docker-compose.yml          # Container orchestration
├── .env                        # Environment configuration
├── backend/                    # FastAPI backend
│   ├── Dockerfile             # Backend container
│   ├── init.sql              # Database initialization
│   ├── requirements.txt      # Python dependencies
│   └── main.py               # API application
├── mobile/                     # React Native app
│   ├── Dockerfile.web        # Web container
│   ├── package.json          # Node dependencies
│   └── App.tsx               # Mobile application
└── .kiro/specs/               # Feature specifications
    └── installment-fraud-detection/
```

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Start all services
./start-dev.sh

# Or manually
docker-compose up --build
```

### Option 2: Manual Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Mobile (in new terminal)
cd mobile
npm install
npm run web
```

## Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379

## Default Credentials

- **Superadmin**: admin@system.com / admin123
- **Business**: business1@test.com / admin123
- **Customer**: customer1@test.com / admin123

## Technology Stack

- **Backend**: FastAPI, PostgreSQL, Redis, SQLAlchemy
- **Frontend**: React Native, Expo, TypeScript
- **Infrastructure**: Docker, Docker Compose
- **Authentication**: JWT tokens
- **Real-time**: WebSockets