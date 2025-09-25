from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import buildings, components, emissions

app = FastAPI(
    title="Smart Building Emissions API",
    description="Digital Twin Interface for Lifecycle Emissions Calculation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(buildings.router)
app.include_router(components.router)
app.include_router(emissions.router)

@app.get("/")
async def root():
    return {"message": "Smart Building Emissions API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"} 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)