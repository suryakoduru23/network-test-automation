# Network Test Automation Framework

A production-grade network validation and testing platform for automated network device testing, monitoring, and reporting. Built following industry best practices used at Google, Cisco, Arista, Juniper, and Meta.

## 🎯 Overview

Network Test Automation Framework is a comprehensive solution for:
- **Device Inventory Management**: Centralized network device repository
- **SSH Automation**: Secure device connectivity and command execution
- **Automated Testing**: Multi-layer network validation
- **Failure Simulation**: Detect and report network anomalies
- **Smart Reporting**: HTML, PDF, and CSV exports
- **Real-time Dashboard**: Network health visualization
- **Intelligent Monitoring**: Periodic validation jobs and alerts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│           React Frontend (TypeScript)               │
│    Dashboard • Devices • Tests • Reports • Alerts   │
└──────────────────┬──────────────────────────────────┘
                   │ REST API + WebSocket
┌──────────────────▼──────────────────────────────────┐
│            FastAPI Backend (Python 3.12)            │
│  Device Mgmt • SSH Automation • Test Engine • Jobs  │
├──────────────────────────────────────────────────────┤
│  Core Modules:                                       │
│  ├─ Device Management (Inventory)                   │
│  ├─ SSH Connection Pool (Netmiko, Paramiko)        │
│  ├─ Test Execution Engine (Pytest Integration)     │
│  ├─ Report Generator (HTML, PDF, CSV)              │
│  ├─ Job Scheduler (APScheduler)                     │
│  └─ Alert System (Email, Webhooks)                 │
└──────────────────┬──────────────────────────────────┘
                   │ SQL ORM (SQLAlchemy)
┌──────────────────▼──────────────────────────────────┐
│      Database (SQLite/PostgreSQL)                   │
│  Users • Devices • Tests • Runs • Reports • Alerts  │
└──────────────────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│      Network Devices (SSH/Telnet)                   │
│  Cisco IOS • Juniper JunOS • Arista EOS • etc.     │
└──────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 1. Device Inventory Management
- Add, edit, delete, and search network devices
- Multi-site device grouping
- Device authentication credentials
- Device type classification (Router, Switch, Firewall)

### 2. SSH Automation
- Secure SSH connections via Netmiko
- Parallel device connectivity
- Command execution with timeout handling
- Output parsing and validation

### 3. Comprehensive Test Suite
- **Interface Validation**: Link status, bandwidth, errors
- **Route Validation**: BGP/OSPF routes, route convergence
- **Reachability Testing**: ICMP ping, traceroute
- **DNS Validation**: DNS resolution and TTL
- **DHCP Validation**: DHCP lease and renewal
- **ARP Validation**: ARP cache and entries
- **VLAN Validation**: VLAN configuration and membership
- **BGP Neighbor Validation**: BGP adjacency and metrics
- **OSPF Neighbor Validation**: OSPF adjacency and state

### 4. Failure Simulation & Detection
- Interface shutdown detection
- Route failure identification
- Packet loss detection
- Link down alerts

### 5. Advanced Reporting
- HTML reports with charts
- PDF generation
- CSV export for analysis
- Test history tracking
- Trend analysis

### 6. Real-time Dashboard
- Total devices count
- Healthy vs failed devices
- Network health score
- Success rate metrics
- Live test execution status

### 7. Monitoring & Alerting
- Scheduled validation jobs
- Email alerts
- Webhook notifications
- Alert history and analytics

### 8. Security
- JWT authentication
- Role-based access control (RBAC)
- Encrypted device credentials
- Audit logging

## 🛠️ Tech Stack

### Backend
- **Python 3.12**: Core language
- **FastAPI**: High-performance REST API framework
- **SQLAlchemy**: ORM for database abstraction
- **Pytest**: Testing framework
- **Netmiko**: Multi-vendor SSH automation
- **Nornir**: Network automation framework
- **Paramiko**: SSH protocol library
- **APScheduler**: Task scheduling
- **Pydantic**: Data validation
- **JWT**: Token-based authentication

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization
- **Axios**: HTTP client
- **React Router**: Navigation
- **Zustand**: State management

### Database
- **SQLite**: Development/Testing
- **PostgreSQL**: Production

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline
- **Linux**: Runtime environment

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12
- Node.js 18+
- Git

### Development Setup

```bash
# Clone repository
git clone https://github.com/suryakoduru23/network-test-automation.git
cd network-test-automation

# Start with Docker Compose
docker-compose up -d

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:3000
# API Docs at http://localhost:8000/docs
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📚 API Documentation

Full API documentation available at `/docs` (Swagger UI) after starting the backend.

### Key Endpoints

```
Authentication:
  POST   /api/v1/auth/login
  POST   /api/v1/auth/logout
  POST   /api/v1/auth/refresh

Devices:
  GET    /api/v1/devices
  POST   /api/v1/devices
  GET    /api/v1/devices/{id}
  PUT    /api/v1/devices/{id}
  DELETE /api/v1/devices/{id}

Tests:
  GET    /api/v1/tests
  POST   /api/v1/tests/run
  GET    /api/v1/tests/{id}/results
  GET    /api/v1/tests/history

Reports:
  GET    /api/v1/reports
  POST   /api/v1/reports/generate
  GET    /api/v1/reports/{id}
  GET    /api/v1/reports/{id}/export

Alerts:
  GET    /api/v1/alerts
  GET    /api/v1/alerts/{id}
  PUT    /api/v1/alerts/{id}

Health:
  GET    /api/v1/health
  GET    /api/v1/health/dashboard
```

## 🔒 Security Features

- ✅ JWT token-based authentication
- ✅ Password hashing with bcrypt
- ✅ Encrypted credential storage
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Audit logging
- ✅ Role-based access control

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 🐳 Docker Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📝 Configuration

Copy `.env.example` to `.env` and configure:

```env
# Backend
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key-here
DEBUG=True
LOG_LEVEL=INFO

# Frontend
VITE_API_URL=http://localhost:8000
```

## 📄 License

MIT License - See LICENSE file

## 👨‍💼 Author

**Surya Koduru**
- GitHub: [@suryakoduru23](https://github.com/suryakoduru23)

---

**Network Test Automation Framework** - Production-Grade Network Testing Platform
