from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def create_user(
    username: str = Path(..., title="Имя пользователя", min_length=3, max_length=20),
    age: int = Path(..., title="Возраст пользователя", ge=1, le=120),
):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: int = Path(..., title="ID пользователя", ge=1),
    username: str = Path(..., title="Имя пользователя", min_length=3, max_length=20),
    age: int = Path(..., title="Возраст пользователя", ge=1, le=120),
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(..., title="ID пользователя", ge=1)):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")