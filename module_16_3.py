from fastapi import FastAPI, Path, HTTPException

app = FastAPI()

users = {1: "Имя: Example, возраст: 18"}


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def post_user(
        username: str = Path(..., title="Имя пользователя", min_length=3, max_length=20, examples="UrbanUser"),
        age: int = Path(..., title="Возраст пользователя", gl=1, le=120, examples=24),
):
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: int = Path(..., title="ID пользователя", gl=1, examples=100),
        username: str = Path(..., title="Имя пользователя", min_length=3, max_length=20, examples="UrbanProfi"),
        age: int = Path(..., title="Возраст пользователя", gl=1, le=120, examples=28),
):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} has been updated"


@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(..., title="ID пользователя", gl=1, examples=2)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    del users[user_id]
    return f"User {user_id} has been deleted"
