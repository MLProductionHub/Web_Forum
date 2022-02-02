

from hashlib import new
from pyexpat import model
from fastapi import Depends, FastAPI, HTTPException, status, Depends, status
from . import schemas, models

from .database import SessionLacal, engine
from sqlalchemy.orm import Session



models.Base.metadata.create_all(engine)

app = FastAPI()




def get_db():
    """[summary]

    Yields:
        [type]: [description]
    """
    db = SessionLacal()

    try:
        yield db
    
    finally:
        db.close()


@app.post('/login', status_code=status.HTTP_201_CREATED)
def create_user(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    """Create user in database.

    Args:
        username (str): user's username
        password (str): user's password
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [str]: "User was added"
    """

    new_user = models.Auth(
        username = username,
        password = password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return "User was added"


@app.get('/blog')
def get_user(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    user = db.query(
        models.Auth).filter(
            models.Auth.username == username 
        ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this username not found."
        )
    
    pass_check = db.query(
        models.Auth).filter(
            models.Auth.password == password
        ).first()
    if not pass_check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Password is wrong."
        )


