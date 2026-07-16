import { useEffect, useState } from "react";
import api from "../services/api";

export default function ChatSidebar({

    currentChat,
    setCurrentChat,
    setMessages,
    refreshChats

}) {

    const [chats, setChats] = useState([]);
    const [editingChat, setEditingChat] = useState(null);
const [editedTitle, setEditedTitle] = useState("");

    const loadChats = async () => {

        try {

            const res = await api.get("/chats");

            setChats(res.data);

        } catch (err) {

            console.error(err);

        }

    };

    useEffect(() => {

    loadChats();

}, [refreshChats]);

    const createChat = async () => {

        try {

            const res = await api.post("/chats");

            setChats(prev => [

                res.data,
                ...prev

            ]);

            setCurrentChat(res.data.id);

            // New chat starts empty
            setMessages([]);

        } catch (err) {

            console.error(err);

        }

    };


    const renameChat = async (chatId) => {

    try {

        await api.patch(`/chats/${chatId}`, {
            title: editedTitle
        });

        setChats(prev =>
            prev.map(chat =>
                chat.id === chatId
                    ? { ...chat, title: editedTitle }
                    : chat
            )
        );

        setEditingChat(null);

    } catch (err) {

        console.error(err);

    }

};


const deleteChat = async (chatId) => {

    const confirmed = window.confirm(
        "Are you sure you want to delete this chat?"
    );

    if (!confirmed) return;

    try {

        await api.delete(`/chats/${chatId}`);

        setChats(prev =>
            prev.filter(chat => chat.id !== chatId)
        );

        if (currentChat === chatId) {

            setCurrentChat(null);

            setMessages([]);

        }

    } catch (err) {

        console.error(err);

    }

};

    const selectChat = async (chatId) => {

        try {

            setCurrentChat(chatId);

            const res = await api.get(`/chats/${chatId}/messages`);

            const formattedMessages = res.data.map(message => ({

                role: message.role,
                content: message.content,
                sources: []

            }));

            setMessages(formattedMessages);

        } catch (err) {

            console.error(err);

        }

    };

    return (

        <div className="w-72 bg-slate-900 border-r border-slate-700 p-5">

            <button

                onClick={createChat}

                className="w-full bg-blue-600 rounded-lg py-2 font-semibold hover:bg-blue-500"

            >

                + New Chat

            </button>

            <div className="mt-6">

                {

                    chats.map(chat => (

                        <div
    key={chat.id}
    onClick={() => selectChat(chat.id)}
    onDoubleClick={() => {
        setEditingChat(chat.id);
        setEditedTitle(chat.title);
    }}

                            className={`
                                p-3
                                rounded-lg
                                cursor-pointer
                                mb-2
                                transition-colors
                                ${
                                    currentChat === chat.id
                                        ? "bg-slate-700"
                                        : "bg-slate-800 hover:bg-slate-700"
                                }
                            `}

                        >

                           {editingChat === chat.id ? (

    <input
        autoFocus
        value={editedTitle}
        onChange={(e) => setEditedTitle(e.target.value)}

        onKeyDown={(e) => {

            if (e.key === "Enter") {

                renameChat(chat.id);

            }

            if (e.key === "Escape") {

                setEditingChat(null);

            }

        }}

        onBlur={() => renameChat(chat.id)}

        className="w-full bg-transparent outline-none"

    />

) : (

   <div
    className="flex items-center justify-between"
>

    <div
        className="flex-1 truncate"
    >

        {editingChat === chat.id ? (

            <input
                autoFocus
                value={editedTitle}
                onChange={(e) => setEditedTitle(e.target.value)}
                onKeyDown={(e) => {

                    if (e.key === "Enter") {
                        renameChat(chat.id);
                    }

                    if (e.key === "Escape") {
                        setEditingChat(null);
                    }

                }}
                onBlur={() => renameChat(chat.id)}
                className="w-full bg-transparent outline-none"
            />

        ) : (

            chat.title

        )}

    </div>

    <button
        onClick={(e) => {

            e.stopPropagation();

            deleteChat(chat.id);

        }}
        className="ml-3 text-red-400 hover:text-red-300"
    >
        🗑️
    </button>

</div>

)}

                        </div>

                    ))

                }

            </div>

        </div>

    );

}