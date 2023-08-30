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
    from faker import Faker
    fake = Faker()

    db = SessionLocal()

    for i in range(5):
            user1 = User(username=f"user{i}", email=f"user{i}@example.com", password=f"password{i}")
            db.add(user1)
            for j in range(20):
                title = fake.sentence()
                content = fake.paragraph()
                post1 = Post(title=title, content=content, author=user1)
                db.add(post1)
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
    # create_tables()
    # add_dummy_data()
    import uvicorn

    uvicorn.run(app)
