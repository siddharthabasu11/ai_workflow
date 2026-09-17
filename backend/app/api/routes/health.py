from fastapi import APIRouter

print(">>> LOADED MY MAIN.PY <<<")

router = APIRouter()

@router.get("/health")

def health_check():
    return {"status":"ok"}