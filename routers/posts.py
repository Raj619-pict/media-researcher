from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.CreatePost])
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.CreatePost)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post); db.commit(); db.refresh(db_post)
    return db_post

@router.get("/{id}", response_model=schemas.CreatePost)
def read_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Post {id} not found")
    return result

@router.put("/{id}", response_model=schemas.CreatePost)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if not query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Post {id} not found")
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if not query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Post {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
