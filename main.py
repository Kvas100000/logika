from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr


users = [
    User(id=1, username="Бабазаки", email="alice@example.com"),
    User(id=2, username="Ваня я не дам деньги", email="bob@example.com"),
    User(id=3, username="Бебебе", email="carol@example.com"),
]

@app.get("/users", response_model=List[User])
def get_users():
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/create_user", response_model=User)
def create_user(user: UserCreate):
    new_id = max(u.id for u in users) + 1 if users else 1
    new_user = User(id=new_id, username=user.username, email=user.email)
    users.append(new_user)
    return new_user

#uvicorn main:app --reload