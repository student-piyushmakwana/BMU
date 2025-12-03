# 🎓 BMU API

> A robust, asynchronous REST API for Bhagwan Mahavir University student portal integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Quart](https://img.shields.io/badge/Quart-0.20.0-green.svg)](https://pgjones.gitlab.io/quart/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](#)

BMU API provides a comprehensive, modern interface to access student data from the Bhagwan Mahavir University portal. Built with async-first principles using Quart, it offers high-performance data scraping, caching with MongoDB, and a clean RESTful API following MVVM architecture.

---

## ✨ Features

### 🔐 Authentication & Security
- **Credential Authentication** - Secure login with BMU portal credentials
- **Google OAuth Integration** - Link Google accounts for seamless access
- **Session Management** - Validate and manage session cookies
- **Secure Logout** - Properly terminate user sessions

### 👤 Student Services
- **Profile Management** - Complete student information (personal, admission, contact, parents, education)
- **Dashboard** - Overview of pending assignments and key metrics
- **Attendance Tracking** - Semester-wise summary, subject-wise breakdown, daily records, absent days
- **Fee Management** - Complete fee history, transactions, receipts with PDF downloads
- **LMS Integration** - Access course materials, syllabus, rate content, download study materials (PDF)
- **Timetable** - Weekly class schedules with effective dates

### 🏛️ University Information
- **Departments** - Browse institute departments with faculty and infrastructure details
- **Public Info** - Latest news, upcoming events, and student testimonials

### ⚡ Technical Features
- **Async Operations** - Non-blocking I/O for high performance
- **Smart Caching** - MongoDB-based caching for faster responses
- **Auto Keep-Alive** - Production scheduler to prevent service sleeping
- **CORS Support** - Cross-origin requests enabled
- **Error Handling** - Comprehensive error handling with detailed messages
- **Data Validation** - Pydantic models for request/response validation

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | [Quart](https://pgjones.gitlab.io/quart/) - Async web framework |
| **Server** | [Hypercorn](https://pgjones.gitlab.io/hypercorn/) - ASGI server |
| **Database** | [MongoDB Atlas](https://www.mongodb.com/) - Cloud NoSQL database |
| **DB Driver** | [Motor](https://motor.readthedocs.io/) - Async MongoDB driver |
| **HTTP Client** | [httpx](https://www.python-httpx.org/) - Async HTTP requests |
| **HTML Parsing** | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - Web scraping |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) - Data validation & serialization |
| **Scheduling** | [APScheduler](https://apscheduler.readthedocs.io/) - Background jobs |
| **CORS** | [Quart-CORS](https://github.com/pgjones/quart-cors) - Cross-origin support |

---

## 🏗️ Architecture

The project follows the **Model-View-ViewModel (MVVM)** pattern for clean separation of concerns:

```
┌─────────────────┐
│   HTTP Request  │
│    (routes.py)  │  ← View Layer
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Business Logic │
│ (viewmodel.py)  │  ← ViewModel Layer
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Models &  │
│  DB Operations  │  ← Model Layer
│   (models.py)   │
└─────────────────┘
```

**Layer Responsibilities:**
- **View (routes.py)** - HTTP request handling, response formatting
- **ViewModel (viewmodel.py)** - Business logic, scraping, external API calls
- **Model (models.py)** - Pydantic schemas, MongoDB documents, data validation

---

## 📂 Project Structure

```
BMU/
├── app/
│   ├── __init__.py           # App factory, blueprint registration
│   ├── core/                 # Core functionality
│   │   ├── client.py         # Shared HTTP client (singleton)
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # MongoDB connection
│   │   └── utils.py          # Helper utilities
│   └── modules/              # Feature modules (MVVM)
│       ├── auth/             # Authentication
│       │   ├── models.py
│       │   ├── routes.py
│       │   └── viewmodel.py
│       ├── departments/      # Department info
│       ├── public/           # Public info (news, events)
│       └── student/          # Student features
│           ├── attendance/
│           ├── dashboard/
│           ├── fees/
│           ├── lms/
│           ├── profile/
│           └── timetable/
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB)
- BMU student portal credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BMU
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # App Configuration
   APP_ENV=development              # development | production
   LOG_LEVEL=INFO                   # DEBUG | INFO | WARNING | ERROR
   BMU_SECRET_KEY=your-secret-key   # Optional, auto-generated if not set
   
   # MongoDB Configuration
   DB_USER=your-mongodb-username
   DB_PASSWORD=your-mongodb-password
   DB_CLUSTER=your-cluster-url      # e.g., cluster0.xxxxx
   
   # Optional Settings
   REQUEST_TIMEOUT=20               # HTTP request timeout (seconds)
   EXTERNAL_URL=https://your-app.com  # For keep-alive in production
   ```

5. **Run the application**
   
   **Development mode:**
   ```bash
   python run.py
   ```
   
   **Production mode (with Hypercorn):**
   ```bash
   hypercorn run:app --bind 0.0.0.0:5000
   ```

6. **Verify it's running**
   ```bash
   curl http://127.0.0.1:5000/
   # Response: {"status": "running", "message": "BMU API is active 🚀"}
   ```

---

## 📡 API Reference

All endpoints are prefixed with `/v2` and require JSON request bodies unless specified otherwise.

### Authentication Endpoints

#### Login with Credentials
```http
POST /v2/auth/login
Content-Type: application/json

{
  "username": "student_username",
  "password": "student_password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "session_cookies": { ... }
  }
}
```

#### Google Authentication
```http
POST /v2/auth/google
Content-Type: application/json

{
  "google_id": "user_google_id",
  "username": "optional_bmu_username",
  "password": "optional_bmu_password"
}
```

#### Validate Session
```http
POST /v2/auth/session/validate
Content-Type: application/json

{
  "session_cookies": { ... }
}
```

#### Logout
```http
POST /v2/auth/logout
Content-Type: application/json

{
  "session_cookies": { ... }
}
```

---

### Student Endpoints

All student endpoints require `session_cookies` in the request body.

#### Get Dashboard
```http
POST /v2/student/dashboard
Content-Type: application/json

{
  "session_cookies": { ... }
}
```

#### Get Profile
```http
POST /v2/student/profile
Content-Type: application/json

{
  "session_cookies": { ... }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "personal_info": { ... },
    "admission_info": { ... },
    "contact_info": { ... },
    "parents_info": { ... },
    "education_qualification": { ... }
  }
}
```

#### Get Attendance
```http
POST /v2/student/attendance
Content-Type: application/json

{
  "session_cookies": { ... }
}
```

#### Get Absent Days
```http
POST /v2/student/attendance/absent
Content-Type: application/json

{
  "session_cookies": { ... },
  "selected_semester": "Sem 1"  # Optional
}
```

#### Get Attendance by Date
```http
POST /v2/student/attendance/date
Content-Type: application/json

{
  "session_cookies": { ... },
  "attendance_date": "2024-01-15"
}
```

#### Get Fee History
```http
POST /v2/student/fees
Content-Type: application/json

{
  "session_cookies": { ... }
}
```

#### Get Fee Posting Details
```http
POST /v2/student/fees/details
Content-Type: application/json

{
  "session_cookies": { ... },
  "fee_posting_id": "12345"
}
```

#### Download Fee Receipt
```http
POST /v2/student/fees/receipt
Content-Type: application/json

{
  "session_cookies": { ... },
  "receipt_id": "ctl00$cphPageContent$..."
}
```

**Response:** Returns PDF file with Content-Type: application/pdf

#### Get LMS Dashboard
```http
POST /v2/student/lms
Content-Type: application/json

{
  "session_cookies": { ... },
  "semester": "Sem 5"  # Optional - filters by semester
}
```

#### Get Subject Details
```http
POST /v2/student/lms/subject
Content-Type: application/json

{
  "session_cookies": { ... },
  "path": "LMS_StudentSubjectContentDetails.aspx?Subj=123"
}
```

#### Download LMS Content/Syllabus
```http
POST /v2/student/lms/pdf
Content-Type: application/json

{
  "session_cookies": { ... },
  "postback_id": "ctl00$cphPageContent$...",
  "form_action": "LMS_StudentSubjectContentDetails.aspx?Subj=123"
}
```

**Response:** Returns PDF file (base64 encoded)

#### Submit Content Rating
```http
POST /v2/student/lms/rating
Content-Type: application/json

{
  "session_cookies": { ... },
  "path": "LMS_StudentSubjectContentDetails.aspx?Subj=123",
  "postback_id": "ctl00$cphPageContent$..."
}
```

#### Get Timetable
```http
POST /v2/student/timetable
Content-Type: application/json

{
  "session_cookies": { ... },
  "timetable_date": "2024-01-15"  # Optional
}
```

---

### Department Endpoints

#### Get All Departments
```http
GET /v2/departments
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "bmu_id": 1,
      "name": "Computer Science",
      "type": "engineering",
      ...
    }
  ]
}
```

#### Get Department Details
```http
POST /v2/department/details
Content-Type: application/json

{
  "bmu_id": 1
}
```

---

### Public Endpoints

#### Get Public Information
```http
GET /v2/public/info
```

**Response:**
```json
{
  "success": true,
  "data": {
    "news": [ ... ],
    "events": [ ... ],
    "testimonials": [ ... ]
  }
}
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_ENV` | Application environment | `production` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `BMU_SECRET_KEY` | Secret key for sessions | Auto-generated | No |
| `DB_USER` | MongoDB username | - | Yes |
| `DB_PASSWORD` | MongoDB password | - | Yes |
| `DB_CLUSTER` | MongoDB cluster URL | - | Yes |
| `REQUEST_TIMEOUT` | HTTP timeout (seconds) | `20` | No |
| `EXTERNAL_URL` | External URL for keep-alive | - | No (Prod only) |

### MongoDB Setup

1. Create a free MongoDB Atlas cluster at [mongodb.com](https://www.mongodb.com/cloud/atlas)
2. Create a database named `BMU`
3. Add two collections: `Departments` and `Users`
4. Get your connection string and extract:
   - Username
   - Password
   - Cluster URL
5. Add these to your `.env` file

---

## 🏃 Running in Production

### Using Hypercorn (ASGI Server)

```bash
# Basic
hypercorn run:app --bind 0.0.0.0:5000

# With workers (recommended)
hypercorn run:app --bind 0.0.0.0:5000 --workers 4

# With auto-reload (development)
hypercorn run:app --bind 0.0.0.0:5000 --reload
```

### Deployment Platforms

**Render.com** (Recommended)
```bash
# Build Command
pip install -r requirements.txt

# Start Command
hypercorn run:app --bind 0.0.0.0:$PORT
```

**Heroku**
```bash
# Add Procfile
web: hypercorn run:app --bind 0.0.0.0:$PORT --workers 4
```

### Production Checklist
- ✅ Set `APP_ENV=production`
- ✅ Configure `EXTERNAL_URL` for keep-alive
- ✅ Use strong `BMU_SECRET_KEY`
- ✅ Enable MongoDB Atlas IP whitelist
- ✅ Set appropriate `LOG_LEVEL` (WARNING or ERROR)
- ✅ Configure HTTPS/SSL
- ✅ Set up monitoring and error tracking

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Health check
curl http://127.0.0.1:5000/health

# Login
curl -X POST http://127.0.0.1:5000/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'

# Get profile (after login)
curl -X POST http://127.0.0.1:5000/v2/student/profile \
  -H "Content-Type: application/json" \
  -d '{"session_cookies":{"ASP.NET_SessionId":"..."}}'
```

### Using Postman

1. Import the API endpoints as a collection
2. Create environment variables for `base_url` and `session_cookies`
3. Use the collection runner for batch testing

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'app'`
- **Solution:** Make sure you're running from the project root directory

**Issue:** `pymongo.errors.ServerSelectionTimeoutError`
- **Solution:** Check MongoDB connection string, verify network access in Atlas, whitelist your IP

**Issue:** `AuthenticationError: Invalid username or password`
- **Solution:** Verify BMU portal credentials are correct. Try logging in manually to the BMU portal first

**Issue:** `Session expired or invalid cookies`
- **Solution:** Re-login to get fresh session cookies. Sessions expire after inactivity.

**Issue:** External service unavailable (502 errors)
- **Solution:** BMU portal might be down or undergoing maintenance. Try again later.

### Debug Mode

Enable detailed logging:
```bash
# Set in .env
LOG_LEVEL=DEBUG
APP_ENV=development
```

---

## 📊 Performance

- **Async Operations:** Non-blocking I/O for concurrent request handling
- **Connection Pooling:** Reused HTTP client for better performance
- **Smart Caching:** MongoDB caching for frequently accessed data
- **Request Timeout:** Configurable timeout to prevent hanging requests
- **Production Optimization:** APScheduler keep-alive prevents cold starts

---

## 🤝 Contributing

This is an educational project. Contributions, issues, and feature requests are welcome!

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the MVVM pattern
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Write descriptive docstrings
- Keep functions focused and single-purpose
- Maintain MVVM separation of concerns

---

## 📄 License

This project is for **educational purposes only**. Not affiliated with or endorsed by Bhagwan Mahavir University.

---

## 👨‍💻 Developer

**Piyush Makwana**

For questions or support, please open an issue on the repository.

---

## 🙏 Acknowledgments

- Bhagwan Mahavir University for the student portal
- Quart framework for excellent async support
- MongoDB Atlas for free-tier database hosting
- All contributors and users of this API

---

<div align="center">
  <sub>Built with ❤️ using Python and Quart</sub>
</div>
