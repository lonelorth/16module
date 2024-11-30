from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Имитируем базу данных в виде списка
users: List['User'] = []


# Определяем модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int


# Создаем объект Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Изначальные пользователи
users = [
    User(id=1, username="UrbanUser ", age=24),
    User(id=2, username="UrbanTest", age=22),
    User(id=3, username="Capybara", age=60),
]


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# Получение всех пользователей
@app.get("/users", response_model=List[User])
async def get_users():
    return users


# Добавление пользователей
@app.post("/users", response_model=User)
async def create_user(user: User):
    # Проверка на уникальность ID
    if any(u.id == user.id for u in users):
        raise HTTPException(status_code=400, detail="User  with this ID already exists.")

    # Генерация ID для нового пользователя
    user_id = (users[-1].id + 1) if users else 1
    new_user = User(id=user_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user


# Получение пользователя по ID
@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return templates.TemplateResponse("users.html", {"request": request, "users": [user]})


# Обновление пользователя
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = user.username
            existing_user.age = user.age
            return existing_user
    raise HTTPException(status_code=404, detail="User  not found")


# Удаление пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User  not found")