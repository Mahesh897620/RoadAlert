from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# AI Backend Router
from routers import reports as ai_reports

# DB Mock Backend Routers
from routes.report import router as report_router
from routes.dashboard import router as dashboard_router
from database.supabase_client import getReports

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On backend startup, call getReports() and log the count
    try:
        reports = getReports()
        count = len(reports) if reports else 0
        print(f"==================================================")
        print(f"✅ Startup check: Supabase connection successful!")
        print(f"📊 Found {count} reports in the database.")
        print(f"==================================================")
    except Exception as e:
        print(f"==================================================")
        print(f"❌ Startup check failed: Could not fetch reports.")
        print(f"   Error: {e}")
        print(f"==================================================")
    yield
    # Shutdown logic if any

app = FastAPI(
    title="RoadAlert API",
    description="AI Road Intelligence Platform — Unified Backend API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root():
    return {"status": "Backend Running"}

# Include AI-based reports router (from root)
app.include_router(ai_reports.router, prefix="/api/reports", tags=["AI Reports"])

# Include DB mock-based routers (from backend database)
app.include_router(report_router, tags=["DB Mock Reports"])
app.include_router(dashboard_router, tags=["Dashboard"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
