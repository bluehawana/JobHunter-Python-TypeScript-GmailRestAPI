# JobHunter - Automated Job Application System

A full-stack application that automates job application processes using Python FastAPI backend and TypeScript React frontend, integrated with Gmail REST API for email management.

## 🚀 Features

- **Automated Job Application Management**: Track and manage job applications efficiently
- **Gmail Integration**: Automatically process job-related emails using Gmail REST API
- **Document Management**: Upload and manage resumes, cover letters, and other documents
- **Dashboard Analytics**: Visual insights into your job search progress
- **User Authentication**: Secure login and user management
- **RESTful API**: Clean, documented API endpoints

## 🏗️ Architecture

```
JobHunter/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Configuration and security
│   │   ├── models/    # Database models
│   │   └── services/  # Business logic
│   └── tests/         # Backend tests
└── frontend/          # TypeScript React frontend
    └── src/
        ├── components/
        ├── pages/
        └── services/
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Gmail REST API** - Email integration
- **JWT** - Authentication

### Frontend
- **TypeScript** - Type-safe JavaScript
- **React** - UI framework
- **Material-UI / Tailwind CSS** - Styling
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Gmail API credentials
- PostgreSQL/SQLite database

## 🚀 Quick Start

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bluehawana/JobHunter-Python-TypeScript-GmailRestAPI.git
   cd JobHunter-Python-TypeScript-GmailRestAPI
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the backend**
   ```bash
   python run.py
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./jobhunter.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gmail API
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret
GMAIL_REDIRECT_URI=http://localhost:8000/auth/gmail/callback
```

### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Add your credentials to the `.env` file

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/jobs/` - List job applications
- `POST /api/v1/jobs/` - Create new job application
- `GET /api/v1/applications/` - List applications
- `POST /api/v1/documents/upload` - Upload documents

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
- Configure production database
- Set production environment variables
- Deploy to your preferred platform (Heroku, AWS, etc.)

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy build folder to your hosting service
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the UI library
- Google for Gmail API integration
- All contributors who help improve this project

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

**Happy Job Hunting! 🎯**