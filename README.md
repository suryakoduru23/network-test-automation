# Network Test Automation Framework

## Overview

The **Network Test Automation Framework (NTAF)** is a comprehensive solution for automating network device testing, validation, and reporting. It provides:

- **SSH-based network automation** - Execute commands on network devices
- **Comprehensive test validators** - Interface, routing, DNS, DHCP, ARP, VLAN, BGP, OSPF, and reachability tests
- **Test execution engine** - Run individual or bulk tests with real-time monitoring
- **Report generation** - Export results in HTML, PDF, or CSV formats
- **Alert management** - Monitor and manage network alerts with severity levels
- **Role-based access control** - Admin, Engineer, and Viewer roles
- **User-friendly dashboard** - Modern React-based web interface
- **RESTful API** - Fully documented API for integration

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              (Dashboard, Devices, Tests)                │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│        ┌──────────────────────────────────────┐        │
│        │      API Routes & Endpoints           │        │
│        ├──────────────────────────────────────┤        │
│        │  Services Layer                       │        │
│        │  - Auth, Device, Test, Report        │        │
│        ├──────────────────────────────────────┤        │
│        │  Core Modules                         │        │
│        │  - SSH, Validators, Security         │        │
│        └──────────────────────────────────────┘        │
└────────────────────┬────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
   Database       SSH Tunnel    File Storage
  (PostgreSQL)   (Netmiko)      (Reports)
```

## Directory Structure

```
network-test-automation/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── core/             # Security, exceptions
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database setup
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt      # Python dependencies
│   ├── run.py                # Entry point
│   └── .env.example          # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── stores/           # State management
│   │   ├── styles/           # Global styles
│   │   ├── App.jsx           # Root component
│   │   └── index.jsx         # Entry point
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── index.html            # HTML template
│
├── docker-compose.yml        # Docker Compose
├── Dockerfile.backend        # Backend Docker image
├── Dockerfile.frontend       # Frontend Docker image
├── README.md                 # This file
└── .gitignore
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- PostgreSQL 15+ (or SQLite for development)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run application
python run.py
```

Backend API will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/api/docs`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### Docker Setup

```bash
# Build and start all services
docker-compose up --build

# Services will be available at:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user

### Devices
- `GET /api/v1/devices` - List all devices
- `POST /api/v1/devices` - Create new device
- `GET /api/v1/devices/{id}` - Get device details
- `PUT /api/v1/devices/{id}` - Update device
- `DELETE /api/v1/devices/{id}` - Delete device
- `POST /api/v1/devices/{id}/test-connectivity` - Test SSH connectivity

### Tests
- `POST /api/v1/tests/run` - Run test
- `POST /api/v1/tests/run-bulk` - Run bulk tests
- `GET /api/v1/tests/{id}` - Get test results
- `GET /api/v1/tests/history` - Get test history

### Reports
- `POST /api/v1/reports/generate` - Generate report
- `GET /api/v1/reports` - List reports
- `GET /api/v1/reports/{id}` - Get report
- `GET /api/v1/reports/{id}/export` - Export report

### Alerts
- `GET /api/v1/alerts` - List alerts
- `GET /api/v1/alerts/{id}` - Get alert
- `PUT /api/v1/alerts/{id}` - Update alert

### Health
- `GET /api/v1/health` - Health check
- `GET /api/v1/health/dashboard` - Dashboard metrics

## Features

### Test Types

1. **Interface Validation** - Verify interface status (up/down)
2. **Route Validation** - Check if route exists in routing table
3. **DNS Validation** - Verify DNS server configuration
4. **DHCP Validation** - Check DHCP lease status
5. **ARP Validation** - Verify ARP entries
6. **VLAN Validation** - Check VLAN existence
7. **BGP Validation** - Monitor BGP neighbor status
8. **OSPF Validation** - Monitor OSPF neighbor status
9. **Reachability Test** - Ping test for connectivity

### Device Support

- Cisco IOS
- Cisco IOS-XE
- Cisco IOS-XR
- Juniper Junos
- Arista EOS
- Linux

### Report Formats

- HTML (with styling)
- PDF (with charts)
- CSV (for spreadsheet import)

## Database Models

### User
- User authentication and role management
- Roles: Admin, Engineer, Viewer

### Device
- Network device inventory
- SSH credentials and connectivity status
- Site and location tracking

### TestCase
- Test definitions and configurations
- Test type and expected results

### TestRun
- Test execution history
- Status tracking and duration

### TestResult
- Individual test results
- Pass/fail status and output

### Report
- Generated test reports
- Statistics and success rates

### Alert
- Network alerts and notifications
- Severity levels (Info, Warning, Critical)

### AuditLog
- User action tracking
- Change history and compliance

## Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt password hashing
- **CORS Protection** - Cross-origin request handling
- **Role-based Access Control** - Fine-grained permissions
- **Audit Logging** - Comprehensive action tracking
- **SSH Key Support** - Alternative to password auth

## Configuration

Key configuration options in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/ntaf_db

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# SSH
SSH_TIMEOUT=30
SSH_PORT=22

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Development

### Running Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Code Formatting

```bash
# Backend
black app/
pylint app/

# Frontend
cd frontend
npm run format
npm run lint
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Migration message"

# Apply migration
alembic upgrade head
```

## Deployment

### Production Deployment

```bash
# Build Docker images
docker-compose -f docker-compose.yml build

# Start services
docker-compose -f docker-compose.yml up -d
```

### Environment Setup

1. Set secure `SECRET_KEY` in `.env`
2. Configure PostgreSQL connection string
3. Set appropriate CORS origins
4. Configure SMTP for email notifications
5. Enable HTTPS in production

## Troubleshooting

### Connection Issues

```bash
# Test SSH connectivity
netmiko_show --host <device_ip> --cmd "show version"

# Check API connectivity
curl http://localhost:8000/api/v1/health
```

### Database Issues

```bash
# Initialize database
python -c "from app.database import init_db; init_db()"

# Check database connection
psql postgresql://user:pass@localhost/ntaf_db
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review API documentation at `/api/docs`

## Roadmap

- [ ] Scheduled test execution
- [ ] Advanced filtering and search
- [ ] Custom test templates
- [ ] Email report delivery
- [ ] Webhook integrations
- [ ] Multi-tenancy support
- [ ] Advanced analytics
- [ ] Mobile app

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Maintainer:** Network Automation Team
