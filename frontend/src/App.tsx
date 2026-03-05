import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import DocumentUpload from "./components/DocumentUpload";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState<"chat" | "upload">("chat");

  return (
    <div className="app">
      <header className="header">
        <h1>📚 RAG Dokumenten-Chatbot</h1>
        <p className="subtitle">
          Stellen Sie Fragen zu Ihren Dokumenten – mit Quellenangabe
        </p>
      </header>

      <nav className="tabs">
        <button
          className={activeTab === "chat" ? "active" : ""}
          onClick={() => setActiveTab("chat")}
        >
          💬 Chat
        </button>
        <button
          className={activeTab === "upload" ? "active" : ""}
          onClick={() => setActiveTab("upload")}
        >
          📄 Dokumente hochladen
        </button>
      </nav>

      <main className="main">
        {activeTab === "chat" ? <ChatWindow /> : <DocumentUpload />}
      </main>

      <footer className="footer">
        <p>
          Powered by <strong>Qdrant</strong> + <strong>AWS Bedrock</strong> +{" "}
          <strong>FastAPI</strong>
        </p>
        <p className="hint">
          <a
            href="https://bojatschkin.de/blog/rag-chatbot-bedrock"
            target="_blank"
            rel="noopener"
          >
            Blogpost lesen
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
