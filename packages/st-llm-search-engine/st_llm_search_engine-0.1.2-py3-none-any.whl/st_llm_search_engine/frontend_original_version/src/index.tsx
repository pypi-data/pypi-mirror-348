// frontend/src/index.tsx

// 聲明全局變量，解決 TypeScript 類型問題
declare const React: any;
declare const ReactDOM: any;

import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import Sidebar from "./components/Sidebar";
import ChatPage from "./components/ChatPage";

// 聲明全局API URL變量
let API_URL = "http://localhost:8000";

// 定義 React 元件
class StLLMSearchEngine extends StreamlitComponentBase {
  public componentDidMount() {
    // 從Streamlit獲取API URL
    if (this.props.args.api_url) {
      API_URL = this.props.args.api_url;
      console.log("API URL:", API_URL);
    }

    // 設置全局變量以供其他組件使用
    window.REACT_APP_API_URL = API_URL;
    console.log("設置全局 window.REACT_APP_API_URL:", window.REACT_APP_API_URL);

    // 設置框架高度
    this.updateFrameHeight();

    // 監聽視窗大小變化
    window.addEventListener('resize', this.updateFrameHeight);

    // 調試 Streamlit 可用性
    console.log("檢查 Streamlit 可用性:");
    console.log("Streamlit:", Streamlit);
    console.log("window.Streamlit:", window.Streamlit);
    try {
      Streamlit.setFrameHeight();
      console.log("Streamlit.setFrameHeight 成功調用");
    } catch (e) {
      console.error("調用 Streamlit.setFrameHeight 失敗:", e);
    }

    try {
      // 嘗試主動發送一個測試消息
      Streamlit.setComponentValue({type: "TEST", data: "Initial test"});
      console.log("通過 Streamlit 發送測試消息成功");
    } catch (e) {
      console.error("發送測試消息失敗:", e);
    }

    // 調試信息
    console.log("組件已掛載", this.props);
    console.log("窗口尺寸:", window.innerWidth, window.innerHeight);
  }

  componentWillUnmount() {
    // 移除事件監聽器
    window.removeEventListener('resize', this.updateFrameHeight);
    console.log("組件已卸載");
  }

  // 更新框架高度的方法
  updateFrameHeight = () => {
    const height = window.innerHeight;
    Streamlit.setFrameHeight(height);
    console.log("Frame height updated to:", height);
  }

  public render() {
    console.log("渲染組件", this.props);

    // 添加全局樣式，確保沒有邊距和內邊距
    const globalStyle = document.createElement('style');
    globalStyle.innerHTML = `
      body, html {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100vh;
      }
      #root {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100vh;
      }
      /* 從 demo.py 移過來的 iframe 相關樣式 */
      iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
      }
    `;
    document.head.appendChild(globalStyle);

    // 設置背景顏色為可見的顏色
    return (
      <div style={{
        width: "100%",
        height: "100vh",
        background: "#111",
        color: "white",
        fontFamily: "'Inter', 'PingFang TC', 'Microsoft JhengHei', Arial, sans-serif",
        display: "flex",
        position: "relative",
        margin: 0,
        padding: 0,
      }}>
        {/* 調試信息 */}
        <div style={{
          position: "absolute",
          top: 0,
          left: 0,
          background: "rgba(0,0,0,0.8)",
          color: "lime",
          padding: "5px",
          fontSize: "10px",
          zIndex: 9999,
          display: "none"
        }}>
          Debug: {new Date().toISOString()}
        </div>

        <Sidebar title="AI 雷達站" />
        <div style={{
          position: "absolute",
          left: "288px", // Sidebar 的寬度
          top: 0,
          right: 0,
          bottom: 0,
          width: "calc(100% - 288px)", // 計算剩餘寬度
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          background: "#222",
          margin: 0,
          padding: 0,
          overflow: "hidden", // 改為 hidden 讓內部 ChatPage 處理滾動
        }}>
          <ChatPage apiUrl={API_URL} />
        </div>
      </div>
    );
  }
}

// 使用官方的 withStreamlitConnection 高階元件
const ConnectedComponent = withStreamlitConnection(StLLMSearchEngine);

// 渲染元件到 DOM
ReactDOM.render(
  <React.StrictMode>
    <ConnectedComponent />
  </React.StrictMode>,
  document.getElementById("root")
);

// 導出API URL以供其他組件使用
export const getApiUrl = () => API_URL;

