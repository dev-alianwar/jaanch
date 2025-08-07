# Full-Stack React Native + FastAPI App

A modern full-stack application with React Native mobile app (with web support) and FastAPI backend.

## Project Structure

- `mobile/` - React Native app with Expo and web support
- `backend/` - FastAPI backend with Python

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Mobile Setup
```bash
cd mobile
npm install
npm run web    # For web development
npm run ios    # For iOS simulator
npm run android # For Android emulator
```

## Features

- Cross-platform mobile app (iOS, Android, Web)
- RESTful API with FastAPI
- Modern React Native with Expo
- Hot reload for development