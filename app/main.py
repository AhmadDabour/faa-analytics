from fastapi import FastAPI
from app.routers.analytics import router_analytics
app = FastAPI( 
    title="FAA Analytics",
    description="2025 Flight data"
)

@app.get("/")
def root():
    return {"message": "FAA Analytics API"}

app.include_router(router_analytics)
