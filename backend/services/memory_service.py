from collections import deque

MAX_HISTORY = 8

sessions = {}


def get_session(session_id: str):

    if session_id not in sessions:

        sessions[session_id] = deque(
            maxlen=MAX_HISTORY
        )

    return sessions[session_id]


def add_message(
    session_id: str,
    role: str,
    content: str
):

    history = get_session(session_id)

    history.append({
        "role": role,
        "content": content
    })


def get_history(session_id: str):

    history = get_session(session_id)

    return list(history)


def clear_history(session_id: str):

    history = get_session(session_id)

    history.clear()