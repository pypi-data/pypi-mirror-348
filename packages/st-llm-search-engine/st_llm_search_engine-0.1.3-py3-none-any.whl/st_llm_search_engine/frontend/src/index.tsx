// frontend/src/index.tsx

import React from "react";
import ReactDOM from "react-dom";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import Sidebar from "./components/Sidebar";
import ChatPage from "./components/ChatPage";

class StLLMSearchEngine extends StreamlitComponentBase<any> {
  public render() {
    // 取得 API URL 參數
    const apiUrl = this.props.args?.api_url || "http://localhost:8000";

    // 設定 iframe 高度（只需呼叫一次即可）
    Streamlit.setFrameHeight();

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
        <Sidebar title="輿論雷達站" apiUrl={apiUrl} />
        <div style={{
          position: "absolute",
          left: "288px", // Sidebar 的寬度
          top: 0,
          right: 0,
          bottom: 0,
          width: "calc(100% - 288px)",
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          background: "#222",
          margin: 0,
          padding: 0,
          overflow: "hidden",
        }}>
          <ChatPage apiUrl={apiUrl} />
        </div>
      </div>
    );
  }
}

const ConnectedComponent = withStreamlitConnection(StLLMSearchEngine);

ReactDOM.render(
  <React.StrictMode>
    <ConnectedComponent />
  </React.StrictMode>,
  document.getElementById("root")
);

