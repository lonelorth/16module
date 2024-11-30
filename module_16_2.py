from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from typing import Annotated

# Создаем объект FastAPI
app = FastAPI()

# Главная страница
@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Главная страница"})

# Страница администратора
@app.get("/user/admin")
async def read_admin():
    return JSONResponse(content={"message": "Вы вошли как администратор"})

# Страница пользователя по ID с валидацией
@app.get("/user/{user_id}")
async def read_user(
    user_id: Annotated[int, Path(gt=0, le=100, description="Enter User ID")]
):
    return JSONResponse(content={"message": f"Вы вошли как пользователь № {user_id}"})

# Страница пользователя по параметрам в строке запроса с валидацией
@app.get("/user/{username}/{age}")
async def read_user_info(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
):
    return JSONResponse(content={"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"})