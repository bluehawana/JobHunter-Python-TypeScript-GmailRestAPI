from fastapi import APIRouter
from app.api.v1.endpoints import auth, jobs, applications, documents, dashboard, gmail, automation, job_fetcher, job_aggregator

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(gmail.router, prefix="/gmail", tags=["gmail"])
api_router.include_router(automation.router, prefix="/automation", tags=["automation"])
api_router.include_router(job_fetcher.router, prefix="/job-fetcher", tags=["job-fetcher"])
api_router.include_router(job_aggregator.router, prefix="/job-aggregator", tags=["job-aggregator"])