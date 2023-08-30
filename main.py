from fastapi import FastAPI
from api.models.models import *
from api.graphql.main import router
from api.authentication.auth import auth_router
from api.user.main import user_router

app = FastAPI()
app.include_router(router=router)
app.include_router(router=auth_router)
app.include_router(router=user_router)


# def get_db() :
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def add_dummy_data():
    db = SessionLocal()
    user1 = User(username="user1", email="user1@example.com", password="password1")
    user2 = User(username="user2", email="user2@example.com", password="password2")
    db.add(user1)


    post1 = Post(title="Post 1", content="Content for post 1", author=user1)
    post2 = Post(title="Post 2", content="Content for post 2", author=user2)
    db.add(post1)
    db.add(post2)

    db.commit()
    db.close()


# from api.graphql.schema import get_db
# def get_posts(db: Session=Depends(get_db)):
#     return db.query(Post).all()

# @app.get("/posts")
# def fetch_posts(db: Session = Depends(get_db)):
#     return db.query(Post).all()

def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    #create_tables()
    #add_dummy_data()
    import uvicorn

    uvicorn.run(app)
