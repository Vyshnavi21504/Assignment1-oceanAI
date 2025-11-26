# test_backend.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

@app.get("/test")
def test_endpoint():
    return {"status": "OK"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting test backend on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")