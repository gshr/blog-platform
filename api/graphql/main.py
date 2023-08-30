from ariadne import ObjectType, gql, make_executable_schema, graphql_sync
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Request
from ..helper import create_comment, get_all_posts, get_post_by_id, delete_post, get_all_users, get_user_by_id, \
    create_post, update_post, update_comment, delete_comment, get_comment_by_id
from api.models.models import *
from api.authentication.auth import current_user
from api.models.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['GraphQL']
)

type_defs = gql(open("api/graphql/schema.graphql").read())

query = ObjectType("Query")
mutation = ObjectType("Mutation")


@query.field("users")
def resolve_users(_, info):
    return get_all_users()


@query.field("posts")
def resolve_posts(_, info):
    return get_all_posts()


@query.field("post")
def resolve_post(_, info, id: int):
    return get_post_by_id(id)


@query.field("user")
def resolve_post(_, info, id: int):
    return get_user_by_id(id)


@mutation.field("deletePost")
def resolve_delete_post(_, info, id: int):
    context = info.context
    user = context["currentuser"]
    db = context['db']
    print(user)
    return delete_post(id, user,db)


@mutation.field("createPost")
def resolve_create_post(_, info, title: str, content: str):
    context = info.context
    user = context["currentuser"]
    db = context['db']
    return create_post(title, content, user, db)


@mutation.field("updatePost")
def resolve_update_post(_, info, id: int, title: str, content: str):
    context = info.context
    user = context["currentuser"]
    db = context['db']
    return update_post(id, title, content, user, db)


@mutation.field("createComment")
def resolve_create_comment(_, info, postId: int, content: str):
    context = info.context
    user = context["currentuser"]
    db = context['db']
    return create_comment(postId, content, user, db)


@mutation.field("updateComment")
def resolve_update_comment(_, info, id, content):
    context = info.context
    user = context["currentuser"]
    db = context['db']
    return update_comment(id, content, user, db)


@mutation.field("deleteComment")
def resolve_delete_comment(_, info, id):
    context = info.context
    user = context["currentuser"]
    db = context['db']
    return delete_comment(id, user, db)


@query.field("comment")
def resolve_get_comment(_, info, id):
    context = info.context
    user = context["currentuser"]
    db = context['db']
    return get_comment_by_id(id, db)


schema = make_executable_schema(type_defs, query, mutation)


@router.post("/")
async def graphql_server(request: Request, currentuser: User = Depends(current_user), db: Session = Depends(get_db)):
    data = await request.json()
    value = {"request": request, "currentuser": currentuser, "db": db}
    success, result = graphql_sync(schema, data, context_value=value)
    status_code = 200 if success else 400
    return JSONResponse(result, status_code=status_code)
