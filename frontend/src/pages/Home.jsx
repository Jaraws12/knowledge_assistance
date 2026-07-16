import { useState } from "react";

import ChatSidebar from "../components/ChatSidebar";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

export default function Home() {

  const [messages, setMessages] = useState([]);

  const [currentChat, setCurrentChat] = useState(null);

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  const [refreshChats, setRefreshChats] = useState(false);

  return (
    <div className="h-screen flex bg-slate-950">

      {/* Chat History Sidebar */}
      <ChatSidebar
    currentChat={currentChat}
    setCurrentChat={setCurrentChat}
    setMessages={setMessages}
    refreshChats={refreshChats}
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
    setCurrentChat={setCurrentChat}
    selectedDocuments={selectedDocuments}
    setRefreshChats={setRefreshChats}
/>
      </div>

    </div>
  );
}