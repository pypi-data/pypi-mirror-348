import React, { useMemo, useCallback, useEffect, useState } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { ModuleRegistry, GridApi } from 'ag-grid-community';
import { AllCommunityModule } from 'ag-grid-community';

ModuleRegistry.registerModules([AllCommunityModule]);

// 為 window 添加類型聲明
declare global {
  interface Window {
    Streamlit: any;
    REACT_APP_API_URL?: string;
  }
}

interface GridStyleProps {
  height: number;
  width: string;
  maxWidth: string;
  minWidth: string;
  margin: string;
  border: string;
  borderRadius: number;
  background: string;
  overflowX: "auto" | "hidden" | "scroll";
}

interface CellStyleProps {
  fontSize: number;
  padding: string;
  whiteSpace: string;
  color: string;
  overflow: string;
  textOverflow: string;
  display?: string;
  WebkitLineClamp?: number;
  WebkitBoxOrient?: string;
  lineHeight: string;
  maxHeight?: string;
}

// 欄位中英文對照表
const columnTranslations: Record<string, string> = {
  doc_id: "文件ID",
  kol_name: "KOL",
  created_time: "發布時間",
  post_url: "連結",
  content: "內容",
  reaction_count: "互動數",
  share_count: "分享數"
  // 可以繼續添加更多欄位的翻譯
};

export default function TablePanel({ columns, rows, query }: { columns: any[]; rows: any[]; query?: string }) {
  const safeQuery = query || "";
  const [aiResponse, setAiResponse] = useState<string>("");
  const [isAiLoading, setIsAiLoading] = useState<boolean>(false);
  const apiUrl = window.REACT_APP_API_URL || "http://localhost:8000"; // 修正為使用 window 對象
  const [hasRequestedAI, setHasRequestedAI] = useState<boolean>(false);

  console.log("TablePanel渲染 - 行數:", rows?.length, "列數:", columns?.length, "查詢:", safeQuery);

  // 當獲取到數據且有查詢關鍵詞時，向AI請求分析
  useEffect(() => {
    console.log("TablePanel useEffect觸發 - 檢查條件:", {
      hasRows: !!rows && rows.length > 0,
      rowsLength: rows?.length || 0,
      hasQuery: !!safeQuery,
      queryValue: safeQuery,
      hasRequestedAI: hasRequestedAI
    });

    if (rows && rows.length > 0 && safeQuery && !hasRequestedAI) {
      setHasRequestedAI(true);
      console.log("符合條件：數據已載入且有查詢參數，準備請求AI分析");

      // 向AI發送請求的函數，獨立提取出來以便執行和調試
      const fetchAiResponse = async () => {
        try {
          setIsAiLoading(true);
          setAiResponse(""); // 清空之前的響應

          console.log("開始發送數據給AI進行分析...");
          console.log("API URL:", `${apiUrl}/api/gemini_analysis`);

          // 準備發送給AI的數據
          const aiRequestData = {
            data: rows.slice(0, 10), // 進一步限制數據量避免請求過大
            query: safeQuery
          };

          console.log("發送數據摘要:", {
            dataCount: rows.length,
            actualSendCount: aiRequestData.data.length,
            queryLength: safeQuery.length,
            firstRowSample: rows[0] ? JSON.stringify(rows[0]).substring(0, 100) + "..." : "無數據"
          });

          // 使用fetch的完整選項以獲得更好的控制和錯誤處理
          const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(aiRequestData),
            // 增加超時處理
            signal: AbortSignal.timeout(30000) // 30秒超時
          };

          try {
            console.log("開始fetch請求...");
            const response = await fetch(`${apiUrl}/api/gemini_analysis`, requestOptions);
            console.log("收到fetch回應, 狀態:", response.status, response.statusText);

            // 讀取響應文本
            const responseText = await response.text();
            console.log("原始響應文本 (前100字符):", responseText.substring(0, 100));

            // 嘗試解析JSON
            let result;
            try {
              result = JSON.parse(responseText);
              console.log("成功解析JSON響應:", result);
            } catch (e) {
              console.error("響應不是有效的JSON:", e);
              setAiResponse("收到無效的API響應格式。原始響應: " + responseText.substring(0, 200));
              return;
            }

            // 檢查響應狀態和內容
            if (response.ok) {
              if (result && typeof result.response === 'string') {
                console.log("AI回答內容長度:", result.response.length);
                console.log("AI回答摘要:", result.response.substring(0, 100) + "...");
                setAiResponse(result.response);
              } else {
                console.error("API返回格式不符合預期:", result);
                if (result && result.error) {
                  setAiResponse(`API返回錯誤: ${result.error}`);
                } else {
                  setAiResponse("AI沒有提供分析結果，或返回格式異常。");
                }
              }
            } else {
              console.error("API請求失敗:", response.status, result);
              setAiResponse(`無法獲取AI分析，請稍後再試。狀態碼: ${response.status}, 錯誤: ${result?.error || '未知錯誤'}`);
            }
          } catch (fetchError) {
            if (fetchError instanceof Error && fetchError.name === 'AbortError') {
              console.error("請求超時:", fetchError);
              setAiResponse("AI分析請求超時，可能是服務器忙碌或網絡問題，請稍後再試。");
            } else if (fetchError instanceof Error) {
              console.error("Fetch請求失敗:", fetchError);
              setAiResponse(`無法連接到AI分析API: ${fetchError.message}`);
            } else {
              console.error("Fetch請求失敗(非標準Error):", fetchError);
              setAiResponse("無法連接到AI分析API，且錯誤型別未知。");
            }
          }
        } catch (error) {
          console.error("AI分析整體處理出錯:", error);
          setAiResponse(`AI分析過程中發生未知錯誤: ${error instanceof Error ? error.message : String(error)}`);
        } finally {
          setIsAiLoading(false);
          console.log("AI分析請求完成，isAiLoading設為false");
        }
      };

      // 執行AI請求
      console.log("立即調用fetchAiResponse函數");
      fetchAiResponse().catch(e => {
        console.error("fetchAiResponse拋出未捕獲的異常:", e);
        setAiResponse(`AI分析過程中發生未處理的異常: ${e.message}`);
        setIsAiLoading(false);
      });
    } else {
      console.log("不符合觸發AI分析的條件，跳過請求");
    }
  }, [rows, safeQuery, apiUrl, hasRequestedAI]);

  // ag-grid columns 需要 field, headerName
  const agColumns = useMemo(() => columns.map(col => {
    // 自動配置欄位寬度
    let columnWidth = 100; // 默認寬度

    if (col.field === 'doc_id') {
      columnWidth = 90; // 文件ID欄位較窄
    } else if (col.field === 'kol_name') {
      columnWidth = 140; // KOL名稱欄位
    } else if (col.field === 'created_time') {
      columnWidth = 220; // 發布時間欄位加寬，確保能顯示完整時間戳
    } else if (col.field === 'post_url') {
      columnWidth = 180; // URL欄位
    } else if (col.field === 'content') {
      columnWidth = 300; // 內容欄位最寬
    } else if (col.field === 'reaction_count') {
      columnWidth = 90; // 互動數較窄
    } else if (col.field === 'share_count') {
      columnWidth = 90; // 分享數較窄
    }

    // 為不同欄位設置不同的樣式
    let cellStyle: any;

    if (col.field === 'created_time') {
      // 發布時間欄位使用單行顯示
      cellStyle = {
        fontSize: 15,
        padding: "6px 8px",
        whiteSpace: "nowrap", // 不換行
        color: "#333",
        overflow: "visible", // 允許內容溢出
        textOverflow: "clip",
        lineHeight: "1.4em"
      };
    } else {
      // 其他欄位使用多行顯示
      cellStyle = {
        fontSize: 15,
        padding: "6px 8px",
        whiteSpace: "normal", // 允許文字換行
        color: "#333",
        overflow: "hidden",
        textOverflow: "ellipsis",
        display: "-webkit-box",
        WebkitLineClamp: 2, // 最多顯示兩行
        WebkitBoxOrient: "vertical",
        lineHeight: "1.4em",
        maxHeight: "2.8em" // 兩行文字的高度
      };
    }

    return {
    field: col.field,
      headerName: columnTranslations[col.field] || col.headerName || col.field,
      width: columnWidth,
      minWidth: col.field === 'created_time' ? 220 : 80, // 發布時間需要更大的最小寬度
      maxWidth: col.field === 'content' ? 500 : (col.field === 'created_time' ? 250 : 300),
      resizable: true,
      sortable: true,
      filter: true,
      wrapText: col.field !== 'created_time', // 時間欄位不換行
      autoHeight: false,
      cellStyle: cellStyle,
    headerClass: 'ag-header-cell',
      // 設置工具提示，顯示完整內容
      tooltipField: col.field,
      tooltipComponentParams: {
        color: "#000",
        backgroundColor: "#fff"
      }
    };
  }), [columns]);

  // 儲存 gridApi 參考
  const gridApiRef = React.useRef<GridApi | null>(null);

  // 下載表格數據為 CSV
  const onBtnExport = useCallback(() => {
    if (gridApiRef.current) {
      gridApiRef.current.exportDataAsCsv({
        fileName: `table_export_${new Date().toISOString().split('T')[0]}.csv`,
      });
    }
  }, []);

  // 手動匯出資料為 JSON
  const exportToJSON = useCallback(() => {
    if (rows && rows.length > 0) {
      const jsonString = JSON.stringify(rows, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `table_export_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  }, [rows]);

  // 設置 grid ready 事件處理器
  const onGridReady = useCallback((params: any) => {
    gridApiRef.current = params.api;

    // 延遲調整大小和刷新，確保表格已經完全初始化
    setTimeout(() => {
      if (gridApiRef.current) {
        // 自動調整所有欄位大小以適應內容
        gridApiRef.current.sizeColumnsToFit();
        gridApiRef.current.refreshCells({ force: true });

        console.log("Grid API 已初始化，表格已刷新");
      }
    }, 300);
  }, []);

  // 當資料變更時刷新表格
  useEffect(() => {
    if (gridApiRef.current && rows && rows.length > 0) {
      console.log("資料已更新，刷新表格");
      setTimeout(() => {
        gridApiRef.current?.refreshCells({ force: true });
      }, 100);
    }
  }, [rows]);

  const gridStyle = useMemo<GridStyleProps>(() => ({
    height: 400,
    width: '100%',
    maxWidth: '100%',
    minWidth: '900px',
    margin: '0 auto 16px auto', // 減少底部margin以便與AI回答區域更接近
    border: '1px solid #1e88e5',
    borderRadius: 8,
    background: '#fff',
    overflowX: "auto",
  }), []);

  // 渲染AI回答區域
  const renderAiResponse = () => {
    console.log("渲染AI回答區域", {
      hasQuery: !!safeQuery,
      rowCount: rows?.length || 0,
      aiResponseLength: aiResponse?.length || 0,
      isLoading: isAiLoading
    });

    // 只有當有query且表格有數據時才顯示AI回答區域
    if (!safeQuery || rows.length === 0) {
      console.log("不顯示AI回答區域: 無查詢或無數據");
      return null;
    }

    // 添加一些樣式來確保區域顯示，即使沒有內容
    const aiResponseAreaStyle = {
      width: '100%',
      maxWidth: '100%',
      minWidth: '900px',
      margin: '0 auto 32px auto',
      padding: '16px',
      minHeight: '100px', // 確保即使沒有內容也有高度
      border: '1px solid #1e88e5',
      borderRadius: 8,
      background: '#fff',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)' // 添加陰影使區域更明顯
    };

    return (
      <div style={aiResponseAreaStyle}>
        <div style={{
          borderBottom: '1px solid #eee',
          paddingBottom: '8px',
          marginBottom: '12px',
          fontWeight: 'bold',
          fontSize: '16px',
          color: '#1e88e5'
        }}>
          AI 分析
        </div>

        {isAiLoading ? (
          <div style={{
            padding: '16px 0',
            textAlign: 'center',
            color: '#666'
          }}>
            AI 正在分析數據...
          </div>
        ) : (
          <div style={{
            whiteSpace: 'pre-wrap',
            lineHeight: '1.6',
            fontSize: '15px',
            color: '#333',
          }}>
            {aiResponse ? aiResponse : "AI 尚未提供分析結果。如果您看到此消息但請求已完成，可能是API配置有誤。"}
          </div>
        )}
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: '100%', alignItems: 'center' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '10px',
        marginBottom: '10px',
        width: '100%'
      }}>
        <button
          onClick={onBtnExport}
          style={{
            background: '#1e88e5',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            padding: '8px 16px',
            cursor: 'pointer',
          }}
        >
          下載 CSV
        </button>
        <button
          onClick={exportToJSON}
          style={{
            background: '#1e88e5',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            padding: '8px 16px',
            cursor: 'pointer',
          }}
        >
          下載 JSON
        </button>
      </div>
    <div
      className="ag-theme-alpine"
        style={gridStyle}
      >
        {rows && rows.length > 0 ? (
      <AgGridReact
        rowData={rows}
            columnDefs={agColumns as any}
        pagination={true}
        paginationPageSize={10}
            domLayout="normal"
            onGridReady={onGridReady}
            enableCellTextSelection={true}
            ensureDomOrder={true}
            suppressRowClickSelection={true}
            suppressCellFocus={false}
        headerHeight={38}
            rowHeight={32}
            defaultColDef={{
              resizable: true,
              sortable: true,
              filter: true,
              floatingFilter: true,
              filterParams: {
                buttons: ['reset', 'apply'],
                closeOnApply: true,
              },
              tooltipComponent: 'customTooltip',
            }}
            tooltipShowDelay={300}
            getRowId={(params) => params.data.doc_id?.toString() || params.data.id?.toString() || Math.random().toString()}
          />
        ) : (
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100%',
            color: '#333'
          }}>
            資料載入中...
          </div>
        )}
      </div>

      {/* 渲染AI回答區域 */}
      {renderAiResponse()}
    </div>
  );
}
