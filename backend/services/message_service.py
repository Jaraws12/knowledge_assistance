from sqlalchemy.orm import Session

from models.message import Message


def add_message(
    db: Session,
    chat_id: int,
    role: str,
    content: str
):

    message = Message(
        chat_id=chat_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages(
    db: Session,
    chat_id: int
):

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .all()
    )