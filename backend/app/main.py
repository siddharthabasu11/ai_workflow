from fastapi import FastAPI

print(">>> LOADED MY MAIN.PY <<<")

app = FastAPI()

@app.get("/health")

def health_check():
    return {"status":"ok"}