import React, { useState, useRef, useEffect, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import type { CodeComponent } from "react-markdown/lib/ast-to-react";
import TablePanel from "./TablePanel";

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

const CodeBlock: CodeComponent = ({ className, children }) => {
  const [copied, setCopied] = useState(false);
  const language = className ? className.replace("language-", "") : "";
  const code = String(children).replace(/\n$/, "");
  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1200);
  };
  return (
    <div style={{ position: "relative" }}>
      <button
        onClick={handleCopy}
        style={{
          position: "absolute",
          top: 8,
          right: 8,
          zIndex: 2,
          background: "#222",
          color: "#28c8c8",
          border: "none",
          borderRadius: 4,
          padding: "2px 8px",
          fontSize: 12,
          cursor: "pointer"
        }}
      >
        {copied ? "已複製" : "複製"}
      </button>
      <SyntaxHighlighter language={language} style={oneDark} customStyle={{ borderRadius: 8, fontSize: 14 }}>
        {code}
      </SyntaxHighlighter>
    </div>
  );
};

function renderMessage(msg: Message) {
  console.log("[ChatPage] renderMessage called", msg);
  // 確保消息內容中的換行符被保留，將原始文本轉換為 JSX 元素
  const content = msg.content || ''; // 添加默認值，防止 undefined

  // 檢查是否為 JSON 格式
  if (content && (content.startsWith('```json') || (content.startsWith('```') && !content.startsWith('```tsx')))) {
    try {
      let jsonContent = content;
      if (content.startsWith('```json')) {
        jsonContent = content.replace(/^```json/, '').replace(/```$/, '').trim();
      } else if (content.startsWith('```')) {
        jsonContent = content.replace(/^```/, '').replace(/```$/, '').trim();
      }

      // 嘗試解析JSON數據
      const parsed = JSON.parse(jsonContent);

      // 檢查是否包含表格數據和可能的查詢關鍵詞
      if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === "object") {
        // 從metadata中提取查詢關鍵詞，如果存在的話
        let query = '';
        // 檢查消息的其他部分是否包含查詢信息
        if (msg.metadata && msg.metadata.query) {
          query = msg.metadata.query;
        }

        const columns = Object.keys(parsed[0]).map(key => ({
          field: key,
          headerName: key
        }));
        const rows = parsed;
        return <TablePanel columns={columns} rows={rows} query={query} />;
      }
    } catch {}
  }

  // 直接使用 ReactMarkdown 渲染，不需要额外处理换行
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{ code: CodeBlock }}
    >
      {content}
    </ReactMarkdown>
  );
}

export default function ChatPage({ apiUrl = "http://localhost:8000" }: ChatPageProps) {
  console.log("[ChatPage] 組件渲染");

  // 為每個用戶創建唯一的會話ID
  const [sessionId] = useState<string>(() => {
    // 嘗試從 sessionStorage 獲取現有的 session_id
    const existingId = sessionStorage.getItem('chat_session_id');
    if (existingId) {
      console.log("[ChatPage] 使用現有的會話ID:", existingId);
      return existingId;
    }

    // 如果不存在，創建新的隨機ID
    const newId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    sessionStorage.setItem('chat_session_id', newId);
    console.log("[ChatPage] 創建新的會話ID:", newId);
    return newId;
  });

  const [messages, setMessages] = useState<Message[]>([]);
  console.log("[ChatPage] useState messages 初始化", messages);
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const [isComposing, setIsComposing] = useState(false);
  const [lastMessageId, setLastMessageId] = useState<string | null>(null);
  const [shouldResetMessages, setShouldResetMessages] = useState(false);
  const [isSwitchingSearch, setIsSwitchingSearch] = useState(false);
  const [hasInitialized, setHasInitialized] = useState(false);
  const [skipInitialFetch, setSkipInitialFetch] = useState(true); // 跳過初始獲取

  // 頁面載入或刷新時，重置初始化狀態
  useEffect(() => {
    console.log("[ChatPage] 頁面加載或刷新，重置初始化狀態");
    // 在組件掛載時將 hasInitialized 設置為 false，確保能夠顯示歡迎頁面
    setHasInitialized(false);
    setIsSwitchingSearch(false);
    setSkipInitialFetch(true); // 重置為跳過初始獲取

    // 檢查是否為刷新頁面（與新窗口不同）
    const loadType = window.performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming;
    if (loadType && loadType.type === 'reload') {
      console.log("[ChatPage] 頁面被刷新，重置所有狀態");
      resetLocalChatSession();

      // 清除任何可能的舊消息，防止在頁面刷新後加載
      fetch(`${apiUrl}/api/clear_messages?session_id=${sessionId}`, {
        method: 'POST',
      }).then(() => {
        console.log("[ChatPage] 已清除服務器端消息，會話ID:", sessionId);
      }).catch(err => {
        console.error("[ChatPage] 清除消息失敗:", err);
      });
    }

    // 5秒後允許獲取新消息，這樣用戶有時間看到歡迎頁面
    const timer = setTimeout(() => {
      setSkipInitialFetch(false);
      console.log("[ChatPage] 現在允許獲取新消息");
    }, 5000);

    // 組件卸載時清理
    return () => {
      console.log("[ChatPage] 組件卸載，清理狀態");
      clearTimeout(timer);
    };
  }, [apiUrl, sessionId]);

  // 重置聊天會話 - 直接設置為空
  const resetLocalChatSession = useCallback(() => {
    console.log("[DEBUG] 直接清空本地聊天消息狀態");
    setMessages([]);
    setLastMessageId(null);
    // 設置跳過初始獲取，防止立即拉取舊消息
    setSkipInitialFetch(true);
    console.log("[DEBUG] 重置會話時設置跳過初始獲取");

    // 強制滾動到頂部
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = 0;
    }

    // 設置切換狀態，防止歡迎頁面閃現
    setIsSwitchingSearch(true);
    console.log("[DEBUG] 設置搜索切換狀態為true (in resetLocalChatSession)");
  }, []);

  // 監聽自定義事件，用於從其他組件觸發消息重置
  useEffect(() => {
    console.log("[ChatPage] useEffect 監聽自定義事件");
    const handleClearMessages = (event: Event) => {
      console.log("[DEBUG] 收到清空消息的自定義事件");

      // 檢查是否是CustomEvent並包含detail數據
      const customEvent = event as CustomEvent;
      if (customEvent.detail) {
        console.log("[DEBUG] 接收到事件詳情:", customEvent.detail);
        // 如果是搜索切換，設置切換狀態
        if (customEvent.detail.isSwitchingSearch) {
          setIsSwitchingSearch(true);
          console.log("[DEBUG] 基於事件詳情設置搜索切換狀態為true");

          // 如果是搜索切換，確保應用被標記為已初始化
          if (!hasInitialized) {
            console.log("[DEBUG] 搜索切換時標記應用已初始化");
            setHasInitialized(true);
          }
        }

        // 如果有標題信息，記錄下來
        if (customEvent.detail.title) {
          console.log("[DEBUG] 正在切換到搜索:", customEvent.detail.title);
        }
      } else {
        // 如果沒有detail數據，也設置切換狀態以確保安全
        setIsSwitchingSearch(true);
        console.log("[DEBUG] 未接收到事件詳情，但仍設置搜索切換狀態為true");

        // 確保應用被標記為已初始化
        if (!hasInitialized) {
          console.log("[DEBUG] 未知清空事件時標記應用已初始化");
          setHasInitialized(true);
        }
      }

      // 設置跳過初始獲取，防止立即拉取舊消息
      setSkipInitialFetch(true);
      console.log("[DEBUG] 清除消息時設置跳過初始獲取");

      resetLocalChatSession(); // 直接調用重置函數，不再使用狀態標記
      // 設置加載狀態，以便顯示加載提示而非歡迎頁面
      setLoading(true);
    };

    // 添加一個標記變量，防止事件重複處理
    let isProcessingSearchCompleted = false;
    // 記錄上一次處理的事件ID
    let lastProcessedEventId = '';

    const handleSearchCompleted = (event: Event) => {
      // 檢查是否是CustomEvent並包含detail數據
      const customEvent = event as CustomEvent;
      const eventDetail = customEvent.detail || {};
      const eventId = eventDetail.eventId || '';

      console.log("[DEBUG] 收到搜索處理完成事件", eventDetail);

      // 如果已經在處理中，或者是已處理過的事件ID，忽略後續事件
      if (isProcessingSearchCompleted || (eventId && eventId === lastProcessedEventId)) {
        console.log("[DEBUG] 忽略重複的搜索處理完成事件", eventId);
        return;
      }

      // 更新最後處理的事件ID
      if (eventId) {
        lastProcessedEventId = eventId;
      }

      // 設置處理標記為 true
      isProcessingSearchCompleted = true;
      console.log("[DEBUG] 開始處理搜索完成事件", eventId);

      // 允許立即獲取消息，以顯示搜索結果
      setSkipInitialFetch(false);
      console.log("[DEBUG] 搜索完成後允許獲取消息");

      // 記錄找到的記錄數
      const recordCount = eventDetail.recordCount || 0;
      console.log("[DEBUG] 搜索結果記錄數:", recordCount);

      // 確保延遲一點時間再關閉loading狀態，避免UI閃爍
      setTimeout(() => {
        setLoading(false);
        console.log("[DEBUG] Loading狀態已設為false");

        // 延遲更長時間再重置切換狀態，確保新消息已經渲染
        setTimeout(() => {
          console.log("[DEBUG] 準備重置搜索切換狀態，當前messages長度:", messages.length);
          // 只有當有消息時才重置切換狀態，否則保持切換狀態
          if (messages.length > 0) {
            setIsSwitchingSearch(false);
            console.log("[DEBUG] 搜索切換狀態已重置為false");
          } else {
            console.log("[DEBUG] 消息為空，保持搜索切換狀態為true");
          }

          // 延遲重置處理標記，防止短時間內重複處理
          setTimeout(() => {
            isProcessingSearchCompleted = false;
            console.log("[DEBUG] 搜索處理完成事件處理標記已重置");
          }, 1500);
        }, 1000); // 延長到1000ms
      }, 500); // 延長到500ms，給更多時間加載消息
    };

    // 添加事件監聽器
    window.addEventListener('clearChatMessages', handleClearMessages);
    window.addEventListener('searchProcessingCompleted', handleSearchCompleted);

    // 清理函數
    return () => {
      window.removeEventListener('clearChatMessages', handleClearMessages);
      window.removeEventListener('searchProcessingCompleted', handleSearchCompleted);
    };
  }, [resetLocalChatSession, messages.length, hasInitialized]); // 添加依賴項

  // 當 shouldResetMessages 變為 true 時，重置消息
  useEffect(() => {
    if (shouldResetMessages) {
      console.log("[DEBUG] 執行消息重置");
      resetLocalChatSession();
      setShouldResetMessages(false);
    }
  }, [shouldResetMessages, resetLocalChatSession]);

  // 定期檢查是否有新消息
  useEffect(() => {
    const checkNewMessages = async () => {
      // 如果設置了跳過初始獲取，則不執行請求
      if (skipInitialFetch) {
        console.log("[DEBUG] 跳過初始消息獲取");
        return;
      }

      try {
        const response = await fetch(`${apiUrl}/api/messages?since=${lastMessageId || ''}&session_id=${sessionId}`);

        if (response.ok) {
          const data = await response.json();

          if (data.messages && data.messages.length > 0) {
            console.log("[DEBUG] 收到新消息，數量:", data.messages.length);

            // 將新消息添加到狀態
            setMessages(prevMessages => {
              // 映射新消息
              const newMessages: Message[] = data.messages.map((msg: any) => ({
                id: msg.id || Date.now().toString() + Math.random(),
                role: msg.role || "bot",
                content: msg.content || "",
                timestamp: msg.timestamp || new Date().toLocaleTimeString().slice(0, 5),
                metadata: msg.metadata
              }));

              // 如果之前沒有消息或已被重置，直接使用新消息
              if (prevMessages.length === 0) {
                console.log("[DEBUG] 沒有現有消息，直接設置新消息，數量:", newMessages.length);
                return newMessages;
              } else {
                // 否則追加新消息
                console.log("[DEBUG] 添加新消息到現有消息，現有數量:", prevMessages.length, "新數量:", newMessages.length);
                return [...prevMessages, ...newMessages];
              }
            });

            // 更新最後一條消息的 ID
            if (data.messages.length > 0) {
              const lastMsg = data.messages[data.messages.length - 1];
              setLastMessageId(lastMsg.id);
              console.log("[DEBUG] 更新最後一條消息 ID:", lastMsg.id);
            }
          }
        } else {
          console.error("[DEBUG] 獲取消息失敗，狀態:", response.status);
        }
      } catch (error) {
        console.error("[DEBUG] 檢查新消息時出錯:", error);
      }
    };

    // 每 2 秒檢查一次新消息
    const intervalId = setInterval(checkNewMessages, 2000);

    return () => clearInterval(intervalId);
  }, [apiUrl, lastMessageId, skipInitialFetch, sessionId]);

  useEffect(() => {
    if (!chatContainerRef.current) return;
    const el = chatContainerRef.current;
    el.scrollTop = el.scrollHeight;
  }, [messages.length]);

  const handleSend = async () => {
    console.log("[ChatPage] handleSend 被呼叫，input:", input);
    if (!input.trim()) return;

    const formattedInput = input; // 保存原始輸入，包含換行
    setInput("");

    const timestamp = new Date().toLocaleTimeString().slice(0, 5);
    const newMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: formattedInput, // 使用保存的原始輸入，不使用 trim()
      timestamp: timestamp,
      metadata: { query: input }
    };

    const updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);

    try {
      setLoading(true);
      setError("");

      // 準備API需要的消息格式
      const apiMessages = updatedMessages.map(msg => ({
        role: msg.role, // 保持原有的 "user" 或 "bot" 角色
        content: msg.content
      }));

      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: apiMessages,
          session_id: sessionId  // 添加會話ID
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // 确保 reply 存在，如果不存在则显示错误消息
        const botReply = data && data.reply ? data.reply : "機器人無法回應，請稍後再試";

        const botMessage: Message = {
          id: Date.now().toString() + "-bot",
          role: "bot",
          content: botReply,
          timestamp: new Date().toLocaleTimeString().slice(0, 5),
          metadata: { query: input }
        };

        setMessages(prevMessages => [...prevMessages, botMessage]);
        setLastMessageId(botMessage.id);
      } else {
        console.error('Error:', data);
        setError(`Error: ${data.error || data.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Network error:', error);
      setError(`Network error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  // 處理鍵盤事件，Shift+Enter 換行，Enter 發送
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        // Shift+Enter：不執行任何動作，讓文本框自然換行
        return;
      } else if (!isComposing) {
        // 單獨 Enter：發送訊息
        e.preventDefault(); // 阻止默認的換行行為
        handleSend();
      }
    }
  };

  // 渲染歡迎訊息或訊息列表
  const renderChatContent = () => {
    console.log("[ChatPage] renderChatContent messages:", messages);
    // 如果正在切換搜索，不顯示任何內容，避免歡迎頁面閃現
    if (isSwitchingSearch) {
      return null;
    }

    if (messages.length === 0) {
      // 當沒有訊息時顯示歡迎區塊
      // 但如果正在加載新消息（loading 為 true），則不顯示任何內容，避免與全局加載提示重複
      if (loading) {
        // 返回空內容，因為全局加載提示會由SavedSearchList處理
        return null;
      }

      // 如果應用已經初始化過（即已經顯示過消息），則不再顯示歡迎頁面
      if (hasInitialized) {
        console.log("[DEBUG] 應用已初始化，不顯示歡迎頁面");
        return null;
      }

      // 只有在首次加載且非加載狀態且消息為空時才顯示歡迎頁面
      return (
        <div style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
          width: "100%",
          padding: "20px"
        }}>
          <div style={{
            background: "transparent",
            padding: "30px",
            borderRadius: "12px",
            maxWidth: "600px",
            textAlign: "center"
          }}>
            <h1 style={{ color: "#fff", marginBottom: "20px", fontSize: "32px" }}>
              歡迎使用 AI 雷達站！
            </h1>
            <p style={{ color: "#ccc", fontSize: "18px", lineHeight: "1.6", marginBottom: "24px" }}>
              您可以透過以下方式開始使用：
            </p>
            <ul style={{
              color: "#ccc",
              fontSize: "16px",
              textAlign: "left",
              lineHeight: "1.8",
              listStylePosition: "inside",
              margin: "0 auto",
              maxWidth: "450px",
              paddingLeft: "20px"
            }}>
              <li>從左側選擇已保存的搜索條件</li>
              <li>獲取篩選過的 KOL 數據</li>
              <li>與 AI 助手互動分析數據</li>
            </ul>
          </div>
        </div>
      );
    }

    // 有訊息時顯示訊息列表
    return messages.map((msg, idx) => {
      console.log("[ChatPage] renderChatContent 處理第", idx, "則訊息", msg);
      return (
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
            {renderMessage(msg)}
            <div style={{
              fontSize: 12,
              color: "#aaa",
              marginTop: 4,
              textAlign: msg.role === "user" ? "right" : "left"
            }}>{msg.timestamp}</div>
          </div>
        </div>
      );
    });
  };

  // 監控messages和isSwitchingSearch狀態
  useEffect(() => {
    console.log("[ChatPage] useEffect messages變更:", messages);
    console.log("[DEBUG] 狀態更新 - messages長度:", messages.length, "isSwitchingSearch:", isSwitchingSearch, "loading:", loading);

    // 如果消息為空且不是切換狀態也不是加載狀態，則可能會顯示歡迎頁面
    if (messages.length === 0 && !isSwitchingSearch && !loading) {
      console.log("[DEBUG] 警告: 可能會顯示歡迎頁面的條件已滿足");
    }

    // 如果有消息但仍處於切換狀態，可以考慮重置切換狀態
    if (messages.length > 0 && isSwitchingSearch) {
      console.log("[DEBUG] 檢測到有消息且處於切換狀態，延遲重置切換狀態");
      const timer = setTimeout(() => {
        setIsSwitchingSearch(false);
        console.log("[DEBUG] 基於消息檢測重置切換狀態為false");
      }, 500);

      return () => clearTimeout(timer);
    }
  }, [messages.length, isSwitchingSearch, loading]);

  // 監控messages狀態，設置hasInitialized
  useEffect(() => {
    // 如果有消息，則標記應用已初始化
    if (messages.length > 0 && !hasInitialized) {
      console.log("[DEBUG] 檢測到消息，標記應用已初始化");
      setHasInitialized(true);
    }
  }, [messages.length, hasInitialized]);

  console.log("[ChatPage] return render");
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
        ref={chatContainerRef}
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflowY: "auto",
          padding: "24px 0",
          paddingBottom: "80px", // 為底部輸入框預留空間
        }}
      >
        <div style={{ width: "80%", margin: "0 auto", display: "flex", flexDirection: "column", height: "100%" }}>
          {renderChatContent()}
          {/* 移除底部加載提示，只保留錯誤提示 */}
          {error && (
            <div style={{ color: "#ff4d4f", textAlign: "center", margin: "16px 0" }}>
              {error}
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* 自定義分隔線 */}
      <div style={{
        position: "fixed",
        bottom: "70px",
        left: "calc(288px + 10%)", // Sidebar 寬度 + 10% 的左邊距
        right: "10%", // 10% 的右邊距
        height: "1px",
        background: "#333",
        zIndex: 10
      }} />

      {/* 輸入框 - 固定在底部 */}
      <div style={{
        position: "fixed",
        bottom: 0,
        left: "288px", // Sidebar 的寬度
        right: 0,
        background: "#161616", // 將底部區域背景色從 #111 改為 #161616
        display: "flex",
        alignItems: "center",
        padding: "16px 32px",
        zIndex: 10
      }}>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onCompositionStart={() => setIsComposing(true)}
          onCompositionEnd={() => setIsComposing(false)}
          onKeyDown={handleKeyDown}
          style={{
            flex: 1,
            background: "#222", // 恢復淺灰色背景
            color: "#fff",
            border: "none",
            borderRadius: 12, // 增加圓角
            padding: "12px 16px",
            fontSize: 16,
            outline: "none",
            resize: "none", // 禁止用戶調整大小
            minHeight: "40px",
            maxHeight: "100px",
            overflowY: "auto" // 允許垂直滾動
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
