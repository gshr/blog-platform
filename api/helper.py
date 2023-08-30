from sqlalchemy.orm import Session
from api.models.models import SessionLocal, Post, User, PostComment


def get_all_posts(db: Session = SessionLocal()):
    return db.query(Post).all()


def get_post_by_id(id: int, db: Session = SessionLocal()):
    post = db.query(Post).filter(Post.id == id).first()
    return post


def get_user_by_id(id: int, db: Session = SessionLocal()):
    post = db.query(User).filter(User.id == id).first()
    return post


def get_comment_by_id(id: int, db):
    comment = db.query(PostComment).filter(PostComment.id == id).first()
    return comment


def get_all_users(db: Session = SessionLocal()):
    return db.query(User).all()


def create_post(title: str, content: str, user, db):
    post1 = Post(title=title, content=content, author=user)
    db.add(post1)
    db.commit()
    db.refresh(post1)
    return {
        "success": True,
        "message": "Post created successfully",
        "post": post1
    }


def update_post(id: int, title: str, content: str, user, db):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        return {"success": False, "message": "Post not found"}

    if post.author != user:
        return {"success": False, "message": "You are not authorized to update this post"}

    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    db.close()

    return {"success": True, "message": "Post updated successfully"}


def create_comment(postId, content, user, db):
    post = db.query(Post).filter(Post.id == postId).first()
    if not post:
        return {
            "success": False,
            "message": "Post not found",
            "comment": None
        }

    new_comment = PostComment(post=post, content=content, author=user)
    db.add(new_comment)
    db.commit()
    return {
        "success": True,
        "message": "Comment created successfully",
        "comment": new_comment
    }


def update_comment(id, content, user, db):
    comment = db.query(PostComment).filter(PostComment.id == id).first()

    if not comment:
        return {
            "success": False,
            "message": "Comment not found"
        }

    if comment.author != user:
        return {
            "success": False,
            "message": "You are not authorized to update this comment"
        }

    comment.content = content
    db.commit()

    return {
        "success": True,
        "message": "Comment updated successfully"
    }


def delete_comment(id: int, currentuser, db):
    comment = db.query(PostComment).filter(PostComment.id == id).first()
    if comment:
        if comment.author != currentuser:
            return {"success": False, "message": "You are not authorized to delete this comment"}
        db.delete(comment)
        db.commit()
        return {"success": True, "message": "comment deleted successfully"}
    else:
        return {"success": False, "message": "comment not found"}


def delete_post(id: int, currentuser, db):
    post = db.query(Post).filter(Post.id == id).first()
    if post:
        print(post.author, currentuser)
        if post.author != currentuser:
            return {"success": False, "message": "You are not authorized to delete this post"}
        db.delete(post)
        db.commit()
        return {"success": True, "message": "Post deleted successfully"}
    else:
        return {"success": False, "message": "Post not found"}
