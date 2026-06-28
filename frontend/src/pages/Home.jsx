import { useState } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

export default function Home() {
  const [messages, setMessages] = useState([]);

  return (
    <div className="h-screen flex bg-slate-950">
      <Sidebar />

      <div className="flex-1">
        <ChatWindow
          messages={messages}
          setMessages={setMessages}
        />
      </div>
    </div>
  );
}