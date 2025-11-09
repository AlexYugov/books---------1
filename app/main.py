from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    auth_router,
    books_router,
    comments_router,
    favorites_router,
    users_router
)
from app.database import Base, engine, get_db
from app.utils.auth import get_password_hash
from app.models.user import User
from sqlalchemy.orm import Session

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Создание аккаунта администратора
def create_admin_user():
    db: Session = next(get_db())
    try:
        admin = db.query(User).filter(User.login == "admin").first()
        if not admin:
            admin = User(
                login="admin",
                email="admin@example.com",
                city="Москва",
                password_hash=get_password_hash("12345678"),
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("Аккаунт администратора создан: login=admin, password=12345678")
        else:
            print("Аккаунт администратора уже существует")
    finally:
        db.close()

# Выполняем создание админа при запуске
create_admin_user()

app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

app.include_router(auth_router)
app.include_router(books_router)
app.include_router(comments_router)
app.include_router(favorites_router)
app.include_router(users_router)

@app.get("/")
async def read_root():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/login.html")
async def read_login():
    with open("frontend/login.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/register.html")
async def read_register():
    with open("frontend/register.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/book.html")
async def read_book():
    with open("frontend/book.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/profile.html")
async def read_profile():
    with open("frontend/profile.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/admin.html")
async def read_admin():
    with open("frontend/admin.html") as f:
        return HTMLResponse(content=f.read())
