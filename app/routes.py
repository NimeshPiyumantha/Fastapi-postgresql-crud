from fastapi import APIRouter
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


@router.post("/create")
async def create_book_service(request: RequestBook, db: Session = Depends(get_db)):
    created_book = crud.create_book(db, book=request.parameter)
    return Response(status="Ok",
                code="200",
                message="Book created successfully",
                result=created_book).dict(exclude_none=True)


@router.get("/")
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_book(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=books).dict(exclude_none=True)

@router.put("/update")
async def update_book(request: RequestBook, db: Session = Depends(get_db)):
    up_book = crud.update_book(db, book_id=request.parameter.id,
                             title=request.parameter.title, description=request.parameter.description)
    return Response(status="Ok",
                code="200",
                message="Book update successfully",
                result=up_book).dict(exclude_none=True)

@router.delete("/{id}")
async def delete_book(id: int, db: Session = Depends(get_db)):
    del_book = crud.remove_book(db, book_id=id)
    return Response(status="Ok",
                    code="200",
                    message="Book deleted successfully",
                    result=del_book).dict(exclude_none=True)