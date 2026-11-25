from pwdlib import PasswordHash
from sqlalchemy import create_engine, String  # импорт sql
from fastapi import FastAPI, HTTPException, Response  # импортирую фастапи
from authx import AuthX, AuthXConfig # импортирую библиотеку в которой есть авторизация гугл, яндекс, вк и тд.
from pydantic import BaseModel # импортирую pydantic для нэйма и пароля
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.testing.pickleable import User

app = FastAPI() # инициализируем приложение(создаем экземпляр FastAPI)

DATABASE_URL = "postgresql+psycopg2://postgres:secret@db:5432/myapp_db" # ссылка на бд
engine_db = create_engine(DATABASE_URL) # Engine — это объект, через который Python общается с базой данных.


config = AuthXConfig() # создаю конфиг будущих параметров(создаю пустой класс)
config.JWT_SECRET_KEY = "SECRET KEY" # 1 параметр - jwt секретный ключ
config.JWT_ACCESS_COOKIE_NAME = "access_token" # 2 параметр - имя ключа в котором хранится токен
config.JWT_TOKEN_LOCATION = ["cookies"] # 3 параметр - токен будет храниться в куки

security = AuthX(config=config) # создаю переменную и прописываю экземпляр класса Authx, он будет использовать
    # вышеуказанный конфиг
password_hash = PasswordHash.recommended() # хэширую пароль через PasswordHash из pwdlib

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    mail: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

class UserSchema(BaseModel): # создаю pydantic схему для получения пароля, почты и юзернэйма
    username: str
    password: str
    mail: str


@app.get("/") # базовый эндпоинт
def hello():
    return {"message": "Hello World!"}

@app.post("/register") # создаю эндпоинт для регистрации пользователя
def register(credentials: UserSchema, response: Response):
    hashed_password = password_hash.hash(credentials.password)

    user = User(
        username=credentials.username,
        mail=credentials.mail,
        password=hashed_password
    )

    with Session(engine_db) as session:
        # try:
            session.add(user)
            session.commit()
            session.refresh(user)
            # Возвращаем объект пользователя, Pydantic автоматически преобразует его в UserResponse
            return user
        # except:
        #     session.rollback()
        #     # Если нарушено ограничение уникальности (username или mail)
        #     raise HTTPException(
        #         status_code=409,
        #         detail="Username or Mail already exists"
        #     )

@app.post("/login") # создаю эндпоинт для авторизации пользователя
def login(credentials: UserSchema, response: Response): # использую pydantic схему для получения пароля, почты и нэйма
    if credentials.username == "test" and credentials.mail == "test" and credentials.password == "test": # делаю базовую проверку пароля и нэйма
        token = security.create_access_token(uid="12345") # создаю токен пользователя(uid)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token) # добавляю в ответ куки, чтобы токен мог храниться где-то
        return {"access_token": token} # возвращаю токен, если проверка пройдена
    raise HTTPException(status_code = 401, detail = "Unauthorized, try again") # иначе возвращаю ошибку о неавторизованности

