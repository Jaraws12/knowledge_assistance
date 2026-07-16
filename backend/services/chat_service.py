from sqlalchemy.orm import Session

from models.chat import Chat


def create_chat(db: Session):

    chat = Chat()

    db.add(chat)

    db.commit()

    db.refresh(chat)

    return chat


def get_all_chats(db: Session):

    return (
        db.query(Chat)
        .order_by(Chat.created_at.desc())
        .all()
    )


def get_chat(db: Session, chat_id: int):

    return (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )


def delete_chat(db: Session, chat_id: int):

    chat = get_chat(db, chat_id)

    if chat is None:
        return None

    db.delete(chat)

    db.commit()

    return chat


def rename_chat(
    db: Session,
    chat_id: int,
    title: str
):

    chat = get_chat(db, chat_id)

    if chat is None:
        return None

    chat.title = title

    db.commit()

    db.refresh(chat)

    return chat





def update_chat_title(
    db: Session,
    chat_id: int,
    title: str
):

    chat = get_chat(db, chat_id)

    if chat is None:
        return None

    # Only update if it's still the default title
    if chat.title != "New Chat":
        return chat

    chat.title = title

    db.commit()

    db.refresh(chat)

    return chat
