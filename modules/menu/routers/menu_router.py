from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/home", 
    tags=["Menu"]
)

@router.get("")
def main():
    return "here"