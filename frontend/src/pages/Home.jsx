import { useState } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

export default function Home() {

  const [messages, setMessages] = useState([]);

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  return (
    <div className="h-screen flex bg-slate-950">

      <Sidebar
        selectedDocuments={selectedDocuments}
        setSelectedDocuments={setSelectedDocuments}
      />

      <div className="flex-1">

        <ChatWindow
          messages={messages}
          setMessages={setMessages}
          selectedDocuments={selectedDocuments}
        />

      </div>

    </div>
  );
}