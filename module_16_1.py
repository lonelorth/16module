from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Создаем объект FastAPI
app = FastAPI()

# Главная страница
@app.get("/")
async def get_main_page():
    return JSONResponse(content={"message": "Главная страница"})

# Страница администратора
@app.get("/user/admin")
async def get_admin_page():
    return JSONResponse(content={"message": "Вы вошли как администратор"})

# Страница пользователя по ID
@app.get("/user/{user_id}")
async def get_user_numder(user_id: int):
    return JSONResponse(content={"message": f"Вы вошли как пользователь № {user_id}"})

# Страница пользователя по параметрам в строке запроса
@app.get("/user")
async def get_user_info(username: str, age: int):
    return JSONResponse(content={"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"})