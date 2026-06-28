import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [question, setQuestion] = useState("");

  const send = () => {
    if (!question.trim()) return;

    onSend(question);

    setQuestion("");
  };

  return (
    <div className="border-t border-slate-700 p-5">
      <div className="flex gap-3">

        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") send();
          }}
          className="flex-1 bg-slate-800 rounded-xl px-5 py-4 outline-none"
          placeholder="Ask something..."
        />

        <button
          onClick={send}
          className="bg-blue-600 hover:bg-blue-700 px-8 rounded-xl"
        >
          Send
        </button>

      </div>
    </div>
  );
}