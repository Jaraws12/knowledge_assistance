import { useState } from "react";
import api from "../services/api";

import ChatInput from "./ChatInput";
import Message from "./Message";
import SourceModal from "./SourceModal";

export default function ChatWindow({
  messages,
  setMessages,
}) {

  const [selectedSource, setSelectedSource] = useState(null);

  const openSource = async (source) => {
    try {
      const res = await api.get("/chunk", {
        params: {
          filename: source.filename,
          page: source.page,
          chunk: source.chunk,
        },
      });

      setSelectedSource(res.data);

    } catch (err) {
      console.error(err);
    }
  };

  const handleSend = async (question) => {

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    const sessionId =
      localStorage.getItem("session_id") ||
      crypto.randomUUID();

    localStorage.setItem("session_id", sessionId);

    try {

      const res = await api.post("/ask", {
        question,
        session_id: sessionId,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.data.answer,
          sources: res.data.sources,
        },
      ]);

    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      <div className="flex flex-col h-full">

        <div className="flex-1 overflow-y-auto p-10">

          {messages.length === 0 ? (

            <div className="flex items-center justify-center h-full">

              <div className="text-center">

                <h1 className="text-5xl font-bold">
                  📚 Knowledge Assistant
                </h1>

                <p className="mt-4 text-slate-400">
                  Upload documents and ask questions.
                </p>

              </div>

            </div>

          ) : (

            messages.map((message, index) => (

              <Message
                key={index}
                message={message}
                openSource={openSource}
              />

            ))

          )}

        </div>

        <ChatInput onSend={handleSend} />

      </div>

      <SourceModal
        source={selectedSource}
        onClose={() => setSelectedSource(null)}
      />
    </>
  );
}