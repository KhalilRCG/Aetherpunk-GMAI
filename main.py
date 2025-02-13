import uvicorn
from fastapi import FastAPI
from web.api_routes import router as api_router

app = FastAPI(title="Aetherpunk GMAI", description="Cyberpunk Game Master AI")
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Aetherpunk GMAI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
