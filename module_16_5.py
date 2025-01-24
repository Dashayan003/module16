from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = [
    User(id=1, username="UrbanUser", age=24),
    User(id=2, username="UrbanTest", age=22),
    User(id=3, username="Capybara", age=60),
]


@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "user": None})


@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user, "users": None})


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
