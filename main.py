import sys
# sys.path.insert(0, "/app")
from fastapi import FastAPI, HTTPException


from auth.validateRegister import validate_register_data
from models.UserRegister import UserRegister
from db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from modelDB.User import User
from models.UserLogin import UserLog
from passlib.context import CryptContext
from db.database import engine
from modelDB.User import Base
from creatJwt import create_access_token
Base.metadata.create_all(bind=engine)
app = FastAPI()

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)
@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/auth/userRegister")
def userRegister(user: UserRegister, db: Session = Depends(get_db)):
    is_valid, message = validate_register_data(user,db)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db_user = db.query(User).filter(User.email == user.email).first()
    return {"message": "success", "user":new_user}


@app.post("/auth/userLogin")
def userLogin(user:UserLog,db:Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user :
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not pwd_context.verify(user.password,db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "message": "success",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "role": db_user.role
        }
    }


@app.get("/auth/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )