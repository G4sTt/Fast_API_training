from fastapi import FastAPI, HTTPException, Response  # импортирую фастапи
from authx import AuthX, AuthXConfig # импортирую библиотеку в которой есть авторизация гугл, яндекс, вк и тд.
from pydantic import BaseModel # импортирую pydantic для нэйма и пароля

app = FastAPI() # инициализируем приложение(создаем экземпляр FastAPI)

config = AuthXConfig() # создаю конфиг будущих параметров(создаю пустой класс)
config.JWT_SECRET_KEY = "SECRET KEY" # 1 параметр - jwt секретный ключ
config.JWT_ACCESS_COOKIE_NAME = "access_token" # 2 параметр - имя ключа в котором хранится токен
config.JWT_TOKEN_LOCATION = ["cookies"] # 3 параметр - токен будет храниться в куки

security = AuthX(config=config) # создаю переменную и прописываю экземпляр класса Authx, он будет использовать
    # вышеуказанный конфиг

class UserLoginSchema(BaseModel): # создаю pydantic схему для получения пароля и юзернэйма
    username: str
    password: str
    mail: str

@app.get("/")
def hello():
    return {"message": "Hello World!"}

@app.post("/register") # создаю эндпоинт для регистрации пользователя
def register():
    ...

@app.post("/login") # создаю эндпоинт для авторизации пользователя
def login(credentials: UserLoginSchema, response: Response): # использую pydantic схему для получения пароля, почты и нэйма
    if credentials.username == "test" and credentials.mail == "test" and credentials.password == "test": # делаю базовую проверку пароля и нэйма
        token = security.create_access_token(uid="12345") # создаю токен пользователя(uid)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token) # добавляю в ответ куки, чтобы токен мог храниться где-то
        return {"access_token": token} # возвращаю токен, если проверка пройдена
    raise HTTPException(status_code = 401, detail = "Unauthorized, try again") # иначе возвращаю ошибку о неавторизованности

