# Installment Fraud Detection System

A comprehensive system to track installment purchases across multiple businesses and detect fraudulent chains where customers obtain products on installment, sell them for cash, and repeat the cycle.

# Installment Fraud Detection System - Complete Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Backend Structure](#backend-structure)
4. [Database Design](#database-design)
5. [API Structure](#api-structure)
6. [Testing Strategy](#testing-strategy)
7. [Requirements](#requirements)
8. [Quick Start Guide](#quick-start-guide)

## System Overview

The Installment Fraud Detection System is a comprehensive platform that tracks installment purchases across multiple businesses to detect and prevent fraudulent chains. The system uses a multi-tenant architecture with role-based access control, real-time fraud detection algorithms, and cross-business data sharing capabilities.

### Key Features
- **Multi-platform Access**: Pure React Native mobile app, Next.js web platform, and FastAPI backend
- **Role-based Access Control**: Superadmin, business, and customer roles
- **Cross-business Fraud Detection**: Track installment chains across multiple businesses
- **Real-time Analytics**: Comprehensive reporting and fraud pattern detection
- **Secure Architecture**: JWT authentication, encrypted data, audit trails

## Architecture

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Mobile App     │    │  Web Platform   │    │  Backend API    │
│  (React Native)│◄──►│  (Next.js)      │◄──►│  (FastAPI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌─────────────────┐
                                               │  Database       │
                                               │  (PostgreSQL)   │
                                               └─────────────────┘
```

### Technology Stack
- **Backend**: FastAPI (Python), PostgreSQL, Redis
- **Web**: Next.js (TypeScript), Tailwind CSS
- **Mobile**: Pure React Native (TypeScript)
- **Infrastructure**: Docker, Docker Compose


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