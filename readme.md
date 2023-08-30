# Blog Platform

This is the source code  of  blog platform that allows users to create and publish blog posts.

## Installation

- Clone this repo into your local machine and create a virtual  environment and install add dependencies
from requirements.txt

```

python -m venv env
env/scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload

```

- Run Using docker

```
 docker build -t myimage . 
 docker run -d --name mycontainer -p 8000:80 myimage

```

## How to Run 

- This application consists of several REST and GraphQL Apis. To run this application first register yourself by using below endpoint
```
http://127.0.0.1:8000/register

Body:
{
  "username": "test1",
  "email": "test1@gmail.com",
  "password": "password1"
}

```

![register.png](images%2Fregister.png)

- Now to login go to Login endpoint and send username and password in form data it will if credentials are valid then it will return us access_token and token_type.This access
token we will send with every request to validate user authorization for particular process.

![login.png](images%2Flogin.png)

`` http://127.0.0.1:8000/login ``

-  Before sending request add this token in Bearer under authorization

![token.png](images%2Ftoken.png)

- To get all the posts
 ````
query Posts {
    posts {
        id
        title
        content
        created_at
        updated_at
    }
}

