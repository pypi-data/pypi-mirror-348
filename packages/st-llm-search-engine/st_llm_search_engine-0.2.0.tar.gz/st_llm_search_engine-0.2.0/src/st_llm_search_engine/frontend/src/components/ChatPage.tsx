import React, { useState, useRef, useEffect, useCallback } from "react";

// 為 window 添加類型聲明
declare global {
  interface Window {
    Streamlit: any;
    REACT_APP_API_URL?: string;
  }
}

type Message = {
  id: string;
  role: "user" | "bot";
  content: string;
  timestamp: string;
  metadata?: { query?: string };
};

type ChatPageProps = {
  apiUrl?: string;
};

export default function ChatPage({ apiUrl = "http://localhost:8001" }: ChatPageProps) {
  // 為每個用戶創建唯一的會話ID
  const [sessionId] = useState<string>(() => {
    const existingId = sessionStorage.getItem('chat_session_id');
    if (existingId) return existingId;
    const newId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    sessionStorage.setItem('chat_session_id', newId);
    return newId;
  });

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 定期檢查是否有新消息
  useEffect(() => {
    const checkNewMessages = async () => {
      try {
        const response = await fetch(`${apiUrl}/api/messages?session_id=${sessionId}`);
        if (response.ok) {
          const data = await response.json();
          if (data.messages && data.messages.length > 0) {
            setMessages(data.messages.map((msg: any) => ({
              id: msg.id || Date.now().toString() + Math.random(),
              role: msg.role || "bot",
              content: msg.content || "",
              timestamp: msg.timestamp || new Date().toLocaleTimeString().slice(0, 5),
              metadata: msg.metadata
            })));
          }
        }
      } catch (error) {
        setError(`Network error: ${error}`);
      }
    };
    checkNewMessages();
    const intervalId = setInterval(checkNewMessages, 2000);
    return () => clearInterval(intervalId);
  }, [apiUrl, sessionId]);

  useEffect(() => {
    if (!bottomRef.current) return;
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages.length]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const formattedInput = input;
    setInput("");
    const timestamp = new Date().toLocaleTimeString().slice(0, 5);
    const newMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: formattedInput,
      timestamp: timestamp,
      metadata: { query: input }
    };
    const updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);
    try {
      setLoading(true);
      setError("");
      const apiMessages = updatedMessages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: apiMessages, session_id: sessionId })
      });
      const data = await response.json();
      if (response.ok) {
        const botReply = data && data.reply ? data.reply : "機器人無法回應，請稍後再試";
        const botMessage: Message = {
          id: Date.now().toString() + "-bot",
          role: "bot",
          content: botReply,
          timestamp: new Date().toLocaleTimeString().slice(0, 5),
          metadata: { query: input }
        };
        setMessages(prevMessages => [...prevMessages, botMessage]);
      } else {
        setError(`Error: ${data.error || data.detail || 'Unknown error'}`);
      }
    } catch (error) {
      setError(`Network error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      width: "100%",
      height: "100vh",
      position: "relative"
    }}>
      {/* 訊息串 - 可滾動區域 */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflowY: "auto",
          padding: "24px 0",
          paddingBottom: "80px",
        }}
      >
        <div style={{ width: "80%", margin: "0 auto", display: "flex", flexDirection: "column", height: "100%" }}>
          {messages.length === 0 && !loading && (
            <div style={{ color: "#aaa", textAlign: "center", marginTop: 40 }}>
              歡迎使用 AI 雷達站！請輸入訊息開始對話。
            </div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={msg.id}
              style={{
                display: "flex",
                flexDirection: msg.role === "user" ? "row-reverse" : "row",
                alignItems: "flex-end",
                marginBottom: 16,
              }}
            >
              <div
                style={{
                  background: msg.role === "user" ? "#222" : "none",
                  color: "#fff",
                  borderRadius: 12,
                  padding: "12px 16px",
                  maxWidth: msg.role === "user" ? "42%" : "70%",
                  wordBreak: "break-word",
                  fontSize: 16,
                  marginLeft: msg.role === "user" ? 0 : 12,
                  marginRight: msg.role === "user" ? 12 : 0,
                  alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                }}
              >
                {msg.content}
                <div style={{
                  fontSize: 12,
                  color: "#aaa",
                  marginTop: 4,
                  textAlign: msg.role === "user" ? "right" : "left"
                }}>{msg.timestamp}</div>
              </div>
            </div>
          ))}
          {error && (
            <div style={{ color: "#ff4d4f", textAlign: "center", margin: "16px 0" }}>
              {error}
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>
      {/* 輸入框 - 固定在底部 */}
      <div style={{
        position: "fixed",
        bottom: 0,
        left: "288px",
        right: 0,
        background: "#161616",
        display: "flex",
        alignItems: "center",
        padding: "16px 32px",
        zIndex: 10
      }}>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          style={{
            flex: 1,
            background: "#222",
            color: "#fff",
            border: "none",
            borderRadius: 12,
            padding: "12px 16px",
            fontSize: 16,
            outline: "none",
            resize: "none",
            minHeight: "40px",
            maxHeight: "100px",
            overflowY: "auto"
          }}
          placeholder="請輸入訊息..."
        />
        <button
          onClick={handleSend}
          style={{
            marginLeft: 16,
            background: "#28c8c8",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            padding: "10px 20px",
            fontSize: 16,
            cursor: "pointer"
          }}
        >送出</button>
      </div>
    </div>
  );
}
