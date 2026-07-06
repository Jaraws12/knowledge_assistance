import { useState } from "react";
import api from "../services/api";

import ChatInput from "./ChatInput";
import Message from "./Message";
import SourceModal from "./SourceModal";

export default function ChatWindow({
  messages,
  setMessages,
  currentChat,
  selectedDocuments,
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

    if (!currentChat) {

      alert("Please create a chat first.");

      return;

    }

    // Add user message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    // Empty assistant message for streaming
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "",
        sources: [],
      },
    ]);

    try {

      const response = await fetch(
        "http://localhost:8000/ask-stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            chat_id: currentChat,
            question,
            documents: selectedDocuments,
          }),
        }
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let answer = "";
      let sources = [];
      let buffer = "";
      let readingSources = false;

      while (true) {

        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);

        if (!readingSources) {

          if (chunk.includes("<END_SOURCES>")) {

            const parts = chunk.split("<END_SOURCES>");

            answer += parts[0];

            buffer += parts[1];

            readingSources = true;

          } else {

            answer += chunk;

          }

          setMessages((prev) => {

            const updated = [...prev];

            updated[updated.length - 1] = {
              role: "assistant",
              content: answer,
              sources,
            };

            return updated;

          });

        } else {

          buffer += chunk;

        }
      }

      if (buffer.trim()) {

        sources = JSON.parse(buffer);

        setMessages((prev) => {

          const updated = [...prev];

          updated[updated.length - 1] = {
            role: "assistant",
            content: answer,
            sources,
          };

          return updated;

        });

      }

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