import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, FileText, Loader2 } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Array<{
    filename: string;
    page: number;
    score: number;
    snippet: string;
  }>;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hallo! Ich bin Ihr Dokumenten-Assistent. Stellen Sie mir Fragen zu Ihren hochgeladenen Dokumenten.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: input,
          tenant_id: "demo",
        }),
      });

      if (!response.ok) throw new Error("Failed to get response");

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer,
        sources: data.sources,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content:
            "Entschuldigung, es ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="avatar">
              {message.role === "user" ? <User size={20} /> : <Bot size={20} />}
            </div>
            <div className="content">
              <div className="text">{message.content}</div>

              {message.sources && message.sources.length > 0 && (
                <div className="sources">
                  <p className="sources-title">
                    <FileText size={14} /> Quellen:
                  </p>
                  {message.sources.map((source, i) => (
                    <div key={i} className="source">
                      <span className="filename">{source.filename}</span>
                      <span className="page">Seite {source.page}</span>
                      <span className="score">
                        ({(source.score * 100).toFixed(0)}%)
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant loading">
            <div className="avatar">
              <Bot size={20} />
            </div>
            <div className="content">
              <Loader2 className="spinner" size={20} />
              <span>Analysiere Dokumente...</span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Frage zu Ihren Dokumenten..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          <Send size={20} />
        </button>
      </form>
    </div>
  );
}
