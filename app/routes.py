from fastapi import APIRouter,HTTPException
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Response, RequestBook

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_response(status: str, code: str, message: str, result=None):
    return {
        "status": status,
        "code": code,
        "message": message,
        "result": result
    }

@router.post("/create")
async def create_book_service(request: RequestBook, db: Session = Depends(get_db)):
    try:
        created_book = crud.create_book(db, book=request.parameter)
        return create_response("Ok", "200", "Book created successfully", created_book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        books = crud.get_book(db, skip, limit)
        return create_response("Ok", "200", "Success fetch all data", books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update")
async def update_book(request: RequestBook, db: Session = Depends(get_db)):
    try:
        up_book = crud.update_book(db, book_id=request.parameter.id,
                                    title=request.parameter.title, description=request.parameter.description)
        return create_response("Ok", "200", "Book update successfully", up_book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}")
async def delete_book(id: int, db: Session = Depends(get_db)):
    try:
        del_book = crud.remove_book(db, book_id=id)
        return create_response("Ok", "200", "Book deleted successfully", del_book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))