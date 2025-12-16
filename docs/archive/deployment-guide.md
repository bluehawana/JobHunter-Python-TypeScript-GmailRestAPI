# Deployment Guide - Job Application Automation

## Overview
This guide covers deploying the Job Application Automation system using serverless architecture on free-tier cloud services.

## Architecture
- **Frontend**: React app deployed on Netlify
- **Backend**: FastAPI deployed on Vercel
- **Database**: MongoDB Atlas (free tier)
- **File Storage**: Vercel Blob or Netlify Large Media

## Prerequisites
1. GitHub account
2. Netlify account
3. Vercel account
4. MongoDB Atlas account
5. Google Cloud Console project with Gmail API enabled

## Backend Deployment (Vercel)

### 1. Prepare Environment Variables
Set these in Vercel dashboard:
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/job_automation
SECRET_KEY=your-long-random-secret-key
GMAIL_CLIENT_ID=your-gmail-client-id-here
GMAIL_CLIENT_SECRET=your-gmail-client-secret
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
REDIS_URL=your-redis-url (optional)
ENVIRONMENT=production
```

### 2. Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to backend directory
cd backend

# Deploy
vercel --prod
```

### 3. Update CORS Settings
After deployment, update `backend/app/core/config.py`:
```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "https://your-frontend-domain.netlify.app",
    "https://your-custom-domain.com"
]
```

## Frontend Deployment (Netlify)

### 1. Build Configuration
Update `frontend/.env.production`:
```
REACT_APP_API_URL=https://your-backend.vercel.app
REACT_APP_ENVIRONMENT=production
REACT_APP_GOOGLE_CLIENT_ID=your-gmail-client-id-here
```

### 2. Deploy to Netlify
```bash
# Build the project
cd frontend
npm run build

# Deploy via Netlify CLI or drag & drop build folder to Netlify
```

### 3. Configure Redirects
The `netlify.toml` file handles:
- API proxy to backend
- SPA routing
- Security headers

## Database Setup (MongoDB Atlas)

### 1. Create Cluster
1. Go to MongoDB Atlas
2. Create free M0 cluster
3. Create database user
4. Whitelist IP addresses (0.0.0.0/0 for serverless)

### 2. Initialize Database
```bash
# Run database initialization
python backend/app/core/init_db.py
```

## Google OAuth Setup

### 1. Update Redirect URIs
In Google Cloud Console, add:
```
https://your-frontend.netlify.app/auth/gmail/callback
https://your-backend.vercel.app/api/v1/auth/gmail/callback
```

### 2. Update JavaScript Origins
```
https://your-frontend.netlify.app
https://your-backend.vercel.app
```

## Environment-Specific Configurations

### Development
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Database: Local MongoDB or Atlas

### Production
- Frontend: `https://your-app.netlify.app`
- Backend: `https://your-api.vercel.app`
- Database: MongoDB Atlas

## Monitoring and Logging

### Vercel
- Built-in function logs
- Performance monitoring
- Error tracking

### Netlify
- Build logs
- Form submissions
- Analytics

## Security Considerations

### Environment Variables
- Never commit secrets to git
- Use platform-specific secret management
- Rotate keys regularly

### CORS Configuration
- Restrict origins to your domains
- Use HTTPS in production
- Validate all inputs

### Database Security
- Use connection strings with authentication
- Enable IP whitelisting
- Regular backups

## Cost Optimization

### Free Tier Limits
- **Vercel**: 100GB bandwidth, 100 serverless functions
- **Netlify**: 100GB bandwidth, 300 build minutes
- **MongoDB Atlas**: 512MB storage, shared cluster

### Optimization Tips
1. Enable caching headers
2. Optimize bundle sizes
3. Use CDN for static assets
4. Implement request rate limiting

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check BACKEND_CORS_ORIGINS configuration
   - Verify frontend URL matches exactly

2. **OAuth Redirect Mismatch**
   - Ensure redirect URIs match exactly in Google Console
   - Check for trailing slashes

3. **Database Connection Issues**
   - Verify MongoDB connection string
   - Check IP whitelist settings

4. **Build Failures**
   - Check Node.js version compatibility
   - Verify all dependencies are listed

### Debug Commands
```bash
# Check backend health
curl https://your-backend.vercel.app/health

# Check frontend build
npm run build

# Test API endpoints
curl -H "Authorization: Bearer <token>" https://your-backend.vercel.app/api/v1/auth/me
```

## Scaling Considerations

### Performance
- Implement caching strategies
- Use database indexes
- Optimize API queries

### Reliability
- Add health checks
- Implement retry logic
- Monitor error rates

### Future Enhancements
- Add Redis for caching
- Implement queue system for background jobs
- Add monitoring and alerting