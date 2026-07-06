import { useState } from "react";

import ChatSidebar from "../components/ChatSidebar";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

export default function Home() {

  const [messages, setMessages] = useState([]);

  const [currentChat, setCurrentChat] = useState(null);

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  return (
    <div className="h-screen flex bg-slate-950">

      {/* Chat History Sidebar */}
      <ChatSidebar
        currentChat={currentChat}
        setCurrentChat={setCurrentChat}
        setMessages={setMessages}
      />

      {/* Uploaded Documents Sidebar */}
      <Sidebar
        selectedDocuments={selectedDocuments}
        setSelectedDocuments={setSelectedDocuments}
      />

      {/* Main Chat Window */}
      <div className="flex-1">
        <ChatWindow
          messages={messages}
          setMessages={setMessages}
          currentChat={currentChat}
          selectedDocuments={selectedDocuments}
        />
      </div>

    </div>
  );
}