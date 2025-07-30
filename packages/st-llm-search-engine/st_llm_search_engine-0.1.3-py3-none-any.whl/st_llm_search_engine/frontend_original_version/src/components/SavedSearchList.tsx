// src/components/SavedSearchList.tsx
import React, { useState, useEffect, useCallback, useMemo } from "react";
import SearchListResult from "./SearchListResult";
import Modal from "./Modal";
import { SearchFormData } from "./Modal";
import { getApiUrl } from "../index";
import { calculateTimeRange } from "../utils/dateUtils";

// 為 window 添加 Streamlit 類型聲明
declare global {
  interface Window {
    Streamlit: any;
    REACT_APP_API_URL?: string;
  }
}

export type SavedSearchListProps = {
  // No props needed as we'll handle everything internally
};

// 保存的查詢條件數據
interface SavedSearch {
  id?: string | number;
  title: string;
  formData: SearchFormData;
  account?: string; // 添加帳號屬性
}

// 添加必要的類型定義
type SearchResult = {
  records: any[];
  start_time: string;
  end_time: string;
  source?: string;
  kol?: string;
};

type FormData = {
  query?: string;
  title?: string;
  source?: string;
  time?: number;
  range?: string;
  n?: string;
  tags?: string[];
};

// 添加格式化時間函數
const formatTime = (timestamp: string): string => {
  try {
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) {
      return timestamp; // 如果解析失敗，返回原始字符串
    }
    return date.toLocaleString('zh-TW', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).replace(/\//g, '/');
  } catch (error) {
    console.error('格式化時間錯誤:', error);
    return timestamp;
  }
};

export default function SavedSearchList({}: SavedSearchListProps) {
  const [open, setOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<SearchFormData | null>(null);
  const [readOnly, setReadOnly] = useState(false); // 添加唯讀模式狀態
  const [savedSearches, setSavedSearches] = useState<SavedSearch[]>([]);
  const [items, setItems] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 10; // Increase max retries
  const [account, setAccount] = useState<string>(""); // 空字符串表示不過濾帳號，顯示所有帳號
  const [selectedItem, setSelectedItem] = useState<string | undefined>(undefined);
  const [editMode, setEditMode] = useState<boolean>(false);
  const [isSearchProcessing, setIsSearchProcessing] = useState<boolean>(false);
  const apiUrl = (window.REACT_APP_API_URL || "http://localhost:8000");

  // 獲取會話ID
  const getSessionId = useCallback((): string => {
    const sessionId = sessionStorage.getItem('chat_session_id');
    if (sessionId) {
      console.log("[SavedSearchList] 使用現有的會話ID:", sessionId);
      return sessionId;
    }

    // 如果不存在，創建一個新的
    const newId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    sessionStorage.setItem('chat_session_id', newId);
    console.log("[SavedSearchList] 創建新的會話ID:", newId);
    return newId;
  }, []);

  // 獲取所有保存的查詢條件 - 使用 useCallback 確保函數引用穩定
  const fetchSavedSearches = useCallback(async (forceRefresh = false) => {
    try {
      console.log("SavedSearchList 開始獲取保存的查詢條件...");
      console.log("使用的 API URL:", apiUrl);
      console.log("當前重試次數:", retryCount);
      console.log("強制刷新:", forceRefresh);

      // 檢查 API URL 是否有效
      if (!apiUrl) {
        console.error("API URL 無效");
        setError("API URL 無效");
        setLoading(false);
        return;
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5秒超時

      try {
        // 移除帳號參數，獲取所有帳號的數據
        const response = await fetch(`${apiUrl}/api/saved_search?force_refresh=${forceRefresh}`, {
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        console.log("API 響應狀態:", response.status);

        if (!response.ok) {
          console.error("獲取保存的查詢條件失敗:", response.status);
          try {
            const errorText = await response.text();
            console.error("錯誤詳情:", errorText);
            setError(`API 錯誤 (${response.status}): ${errorText}`);
          } catch (e) {
            console.error("無法獲取錯誤詳情");
            setError(`API 錯誤 (${response.status})`);
          }

          // 如果還沒達到最大重試次數，則增加重試計數
          if (retryCount < maxRetries) {
            console.log(`將在1秒後進行第 ${retryCount + 1} 次重試`);
            setRetryCount(prev => prev + 1);
            return;
          }

          // 如果已達到最大重試次數，則標記為已初始化並停止加載
          console.log(`已達到最大重試次數 ${maxRetries}，停止重試`);
          setLoading(false);
          return;
        }

        const data = await response.json();
        console.log("API 返回的原始數據:", data);

        if (data.items && Array.isArray(data.items)) {
          setItems(data.items);
        } else {
          setItems([]);
        }

        if (data.records && Array.isArray(data.records)) {
          // 將記錄轉換為所需格式
          const formattedRecords = data.records.map((record: any) => ({
            title: record.title,
            formData: record.data,
            account: record.account || "系統" // 確保有帳號字段
          }));
          setSavedSearches(formattedRecords);
        } else {
          setSavedSearches([]);
        }

        // 成功獲取數據，重置重試計數並標記為已初始化
        setRetryCount(0);
        setError(null);
        setLoading(false); // 立即停止加載狀態
      } catch (error: any) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
          console.error("請求超時");
          setError("API 請求超時");
        } else {
          console.error("獲取保存的查詢條件失敗:", error);
          setError(error.message || "未知錯誤");
        }

        // 如果還沒達到最大重試次數，則增加重試計數
        if (retryCount < maxRetries) {
          console.log(`將在1秒後進行第 ${retryCount + 1} 次重試`);
          setRetryCount(prev => prev + 1);
          return;
        }

        // 如果已達到最大重試次數，則標記為已初始化
        console.log(`已達到最大重試次數 ${maxRetries}，停止重試`);
        setLoading(false); // 確保停止加載狀態
      }
    } catch (error: any) {
      console.error("獲取保存的查詢條件失敗 (外層錯誤):", error);
      setError(error.message || "未知錯誤");

      // 如果還沒達到最大重試次數，則增加重試計數
      if (retryCount < maxRetries) {
        console.log(`將在1秒後進行第 ${retryCount + 1} 次重試`);
        setRetryCount(prev => prev + 1);
        return;
      }

      // 如果已達到最大重試次數，則標記為已初始化
      console.log(`已達到最大重試次數 ${maxRetries}，停止重試`);
      setLoading(false); // 確保停止加載狀態
    }
  }, [apiUrl, retryCount, maxRetries]);

  // 加載保存的查詢條件 - 只在組件掛載時執行一次
  useEffect(() => {
    console.log("SavedSearchList 組件掛載，開始獲取保存的查詢條件");
    // 確保 API URL 已經初始化
    if (apiUrl && !loading) {
      fetchSavedSearches();
    }
  }, [apiUrl, loading, fetchSavedSearches]);

  // 重試機制
  useEffect(() => {
    // 如果已經初始化或已經達到最大重試次數，則不再重試
    if (loading || retryCount >= maxRetries) {
      return;
    }

    // 如果需要重試，設置一個定時器
    if (retryCount > 0) {
      console.log(`嘗試第 ${retryCount} 次重新獲取保存的查詢條件...`);
      const timer = setTimeout(() => {
        fetchSavedSearches();
      }, 1000); // 1秒後重試

      return () => clearTimeout(timer);
    }
  }, [retryCount, loading, fetchSavedSearches, maxRetries]);

  // Debug effect to monitor state changes
  useEffect(() => {
    console.log("DEBUG - State changes:");
    console.log("loading:", loading);
    console.log("items:", items);
    console.log("savedSearches:", savedSearches);
    console.log("error:", error);
  }, [loading, items, savedSearches, error]);

  // 處理編輯項目
  const handleEdit = async (item: {title: string, readOnly?: boolean}) => {
    try {
      setLoading(true);

      // 如果明確傳入了 readOnly 參數，則使用該值
      if (item.readOnly !== undefined) {
        setReadOnly(item.readOnly);
      } else {
        // 否則檢查是否為系統帳號項目
        const searchItem = savedSearches.find(search => search.title === item.title);
        const isSystemItem = searchItem?.account === "系統";
        // 設置唯讀模式狀態
        setReadOnly(isSystemItem);
      }

      // 從服務器獲取完整的查詢條件數據
      const response = await fetch(`${apiUrl}/api/saved_search/${encodeURIComponent(item.title)}`);

      if (response.ok) {
        const data = await response.json();
        setEditingItem(data);
      } else {
        // 如果沒有找到保存的數據，則只傳遞標題
        setEditingItem({ title: item.title });
      }
    } catch (error) {
      console.error("獲取查詢條件詳情失敗:", error);
      setEditingItem({ title: item.title });
    } finally {
      setLoading(false);
      setOpen(true);
    }
  };

  // 關閉 Modal
  const handleClose = () => {
    setOpen(false);
    setEditingItem(null);
    setReadOnly(false); // 重置唯讀狀態
  };

  // 保存表單數據
  const handleSave = async (formData: SearchFormData): Promise<void> => {
    console.log("handleSave 被調用，formData:", formData);
    try {
      // 使用 loading 而不是 loading
      setLoading(true);

      if (!formData.title) {
        console.error("標題不能為空");
        alert("標題不能為空");
        setLoading(false);
        return;
      }

      console.log("準備發送數據到服務器:", formData);

      // 發送數據到服務器
      const response = await fetch(`${apiUrl}/api/saved_search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      console.log("API 響應狀態:", response.status);

      if (response.ok) {
        const result = await response.json();
        console.log("保存查詢條件成功:", result);

        // 在本地更新狀態，避免重新獲取
        const title = formData.title;

        // 檢查是否已存在，更新 items 狀態
        if (!items.includes(title)) {
          setItems(prev => [...prev, title]);
        }

        // 更新 savedSearches 狀態
        setSavedSearches(prev => {
          // 檢查是否已存在相同標題的項目
          const existingIndex = prev.findIndex(item => item.title === title);

          if (existingIndex >= 0) {
            // 如果已存在，則更新
            const updated = [...prev];
            updated[existingIndex] = {
              id: updated[existingIndex].id, // 保留原有ID
              title: title,
              formData: formData
            };
            return updated;
          } else {
            // 如果不存在，則添加新項目
            return [...prev, {
              id: Date.now().toString(), // 臨時ID，服務器會分配真正的ID
              title: title,
              formData: formData
            }];
          }
        });

        // 關閉模態框
        setOpen(false);
        setEditingItem(null);
      } else {
        const errorData = await response.json();
        console.error("保存查詢條件失敗:", errorData);
        alert(`保存失敗: ${errorData.error || '未知錯誤'}`);
      }
    } catch (error: any) {
      console.error("保存查詢條件出錯:", error);
      alert(`保存出錯: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      // 使用 loading 而不是 loading
      setLoading(false);
    }
  };

  // 處理右鍵點擊
  const handleContextMenu = (
    e: React.MouseEvent,
    search: SavedSearch
  ) => {
    e.preventDefault();

    // 檢查是否為系統帳號項目，設置唯讀模式
    const isSystemItem = search.account === "系統";
    setReadOnly(isSystemItem);

    setEditingItem(search.formData);
    setOpen(true);
  };

  // 處理保存編輯後的查詢條件
  const handleSaveEdit = async (formData: SearchFormData): Promise<void> => {
    console.log("handleSaveEdit 被調用，formData:", formData);

    // 直接使用 handleSave 函數
    await handleSave(formData);
  };

  // 該函數位於獲取過濾數據後，用於發送消息到聊天界面
  const sendMessageWithResult = async (result: any, formData: SearchFormData, eventId: string) => {
    try {
      // 確保結果中包含數據
      if (!result || !result.records) {
        // 如果沒有記錄，發送一個消息表示沒有找到數據
        await fetch(`${apiUrl}/api/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            role: "bot",
            content: `嗨！我找到了「${formData.title}」的檢索資料啦！🎉✨\n\n這批資料的時間範圍是 ${formData.time === 3 ? `${formData.range ? formData.range[0]?.format('YYYY/M/D HH:mm:ss') : ''} ~ ${formData.range ? formData.range[1]?.format('YYYY/M/D HH:mm:ss') : ''}` : `${getTimeOptionText(formData.time, formData.n)}`} 📅⏰\n\n我已經為你整理好囉～這裡面包含了：\n• 資料來源：${getSourceText(formData.source)} 📊\n• 涵蓋KOL：${formData.tags?.length === 0 || formData.tags?.includes("All") ? "All" : formData.tags?.join(", ")} 🌟\n\n總共有 0 筆資料等著你來探索！🔍🧐\n\n有什麼想了解的嗎？我很樂意幫你找出有趣的洞見或分析這段時間的趨勢喔！💡🤔✌️`,
            metadata: { query: formData.query || "" }
          })
        });
        return;
      }

      // 發送描述性消息
      await fetch(`${apiUrl}/api/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          role: "bot",
          content: `嗨！我找到了「${formData.title}」的檢索資料啦！🎉✨\n\n這批資料的時間範圍是 ${formData.time === 3 ? `${formData.range ? formData.range[0]?.format('YYYY/M/D HH:mm:ss') : ''} ~ ${formData.range ? formData.range[1]?.format('YYYY/M/D HH:mm:ss') : ''}` : `${getTimeOptionText(formData.time, formData.n)}`} 📅⏰\n\n我已經為你整理好囉～這裡面包含了：\n• 資料來源：${getSourceText(formData.source)} 📊\n• 涵蓋KOL：${formData.tags?.length === 0 || formData.tags?.includes("All") ? "All" : formData.tags?.join(", ")} 🌟\n\n總共有 ${result.total_count} 筆資料等著你來探索！🔍🧐\n\n有什麼想了解的嗎？我很樂意幫你找出有趣的洞見或分析這段時間的趨勢喔！💡🤔✌️`,
          metadata: { query: formData.query || "" }
        })
      });

      // 等待一段時間，確保第一條消息已經被接收和處理
      await new Promise(resolve => setTimeout(resolve, 300));

      // 如果有記錄，發送JSON格式的數據
      if (result.records.length > 0) {
        const tableMsg = {
          role: "bot",
          content: `\`\`\`json\n${JSON.stringify(result.records, null, 2)}\n\`\`\``,
          metadata: { query: formData.query || "" }
        };
        await fetch(`${apiUrl}/api/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(tableMsg)
        });
      }
    } catch (error) {
      console.error("發送消息失敗:", error);
      throw error;
    }
  };

  // 處理選擇項目
  const handleSelect = async (title: string) => {
    try {
      console.log("選擇項目觸發，標題:", title);
      console.log("使用的 API URL:", apiUrl);
      setSelectedItem(title); // 設置選中項目
      setIsSearchProcessing(true); // 開始處理搜索，顯示Loading狀態

      // 獲取會話ID
      const sessionId = getSessionId();

      // 步驟1: 清除現有消息
      await clearMessages(title, true);

      // 添加延遲確保清空操作完成
      await new Promise(resolve => setTimeout(resolve, 300));
      console.log("清空消息操作完成，延遲後繼續");

      // 步驟3: 獲取保存的查詢條件
      console.log(`開始從 ${apiUrl}/api/saved_search/${encodeURIComponent(title)} 獲取查詢條件`);
      const response = await fetch(`${apiUrl}/api/saved_search/${encodeURIComponent(title)}`);

      console.log("獲取查詢條件響應狀態:", response.status);
      if (!response.ok) {
        const errorText = await response.text();
        console.error("獲取查詢條件時返回錯誤:", errorText);
        throw new Error(`無法獲取查詢條件: ${errorText}`);
      }

      const data = await response.json();
      console.log("獲取到的查詢條件:", data);

      if (!data || !data.form_data) {
        throw new Error("獲取的查詢條件無效");
      }

      const formData = data.form_data;
      console.log("要處理的表單數據:", formData);

      // 步驟4: 發送搜索查詢
      console.log("發送查詢到 KOL 數據API");
      const kolSearchResponse = await fetch(`${apiUrl}/api/sheet/kol/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          session_id: sessionId  // 添加會話ID
        }),
      });

      if (!kolSearchResponse.ok) {
        const errorText = await kolSearchResponse.text();
        console.error("搜索KOL時返回錯誤:", errorText);
        throw new Error(`搜索出錯: ${errorText}`);
      }

      const searchResult = await kolSearchResponse.json();
      console.log("搜索結果:", searchResult);

      if (!searchResult || !searchResult.records) {
        throw new Error("無效的搜索結果");
      }

      // 步驟5: 發送搜索結果消息
      console.log("發送搜索結果消息");
      const messageSent = await sendSearchResultMessages(title, searchResult, formData);
      if (!messageSent) {
        throw new Error("發送搜索結果消息失敗");
      }

      console.log("搜索完成，結果已展示");
    } catch (err) {
      console.error("處理搜索時出錯:", err);
      setError(`處理搜索時出錯: ${err instanceof Error ? err.message : String(err)}`);
      // 即使出錯，也發送事件通知處理完成
      window.dispatchEvent(new CustomEvent('searchProcessingCompleted', {
        detail: { error: true }
      }));
    } finally {
      // 無論成功或失敗，都重置處理狀態
      setIsSearchProcessing(false);
    }
  };

  // 輔助函數：獲取時間選項的文字描述
  const getTimeOptionText = (time?: number, n?: string): string => {
    switch(time) {
      case 0: return "昨日";
      case 1: return "今日";
      case 2: return `近${n || "N"}日`;
      case 3: return "自訂區間";
      default: return "今日";
    }
  };

  // 輔助函數：獲取資料源的文字描述
  const getSourceText = (source?: number): string => {
    switch(source) {
      case 0: return "全部";
      case 1: return "Facebook";
      case 2: return "Threads";
      default: return "全部";
    }
  };

  // 手動重試獲取數據
  const handleRetry = () => {
    console.log("手動重試獲取數據並強制刷新緩存");
    setRetryCount(0);
    setLoading(true);
    fetchSavedSearches(true); // 傳入 true 以強制刷新緩存
  };

  // 處理項目重新排序
  const handleReorder = async (newItems: string[]) => {
    try {
      console.log("處理項目重新排序:", newItems);

      // 檢查是否有系統項目位置被改變
      const systemItems = savedSearches.filter(item => item.account === "系統").map(item => item.title);
      const oldSystemItemsOrder = items.filter(item => systemItems.includes(item));
      const newSystemItemsOrder = newItems.filter(item => systemItems.includes(item));

      // 檢查系統項目的順序是否改變
      const systemItemsOrderChanged = oldSystemItemsOrder.join(',') !== newSystemItemsOrder.join(',');

      if (systemItemsOrderChanged) {
        console.error("系統項目不可拖曳，恢復原始順序");
        // 恢復原始順序
        return;
      }

      // 更新本地狀態，立即反映變化
      setItems(newItems);

      // 準備發送到服務器的數據
      const reorderData = {
        items: newItems.map((title, index) => ({
          title,
          order: index + 1  // 順序從1開始
        }))
        // 移除帳號參數，讓後端根據項目找到對應帳號進行更新
      };

      console.log("發送重排序數據到服務器:", reorderData);

      // 調用 API 更新順序
      const response = await fetch(`${apiUrl}/api/saved_search/reorder`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(reorderData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("重排序成功:", result);
      } else {
        console.error("重排序失敗:", response.status);
        // 如果失敗，可以考慮重新獲取數據恢復原狀
        // await fetchSavedSearches();
      }
    } catch (error) {
      console.error("重排序出錯:", error);
      // 如果出錯，可以考慮重新獲取數據恢復原狀
      // await fetchSavedSearches();
    }
  };

  // 處理刪除項目
  const handleDelete = async (title: string) => {
    try {
      console.log("刪除項目:", title);

      // 檢查是否為系統帳號項目
      const isSystemItem = savedSearches.find(item => item.title === title)?.account === "系統";

      if (isSystemItem) {
        console.error("系統項目不可刪除");
        alert("系統項目不可刪除");
        return;
      }

      // 先更新本地狀態，立即從UI移除項目
      const newItems = items.filter(item => item !== title);
      setItems(newItems);

      // 在後台發送刪除請求
      const response = await fetch(`${apiUrl}/api/saved_search/${encodeURIComponent(title)}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        console.log("刪除成功");
        // 不需要重新獲取，因為我們已經更新了本地狀態
      } else {
        console.error("刪除失敗:", response.status);
        // 如果刪除失敗，恢復原始列表
        setItems(items);
        // 可以選擇顯示錯誤消息
        alert("刪除失敗，請稍後再試");
      }
    } catch (error) {
      console.error("刪除出錯:", error);
      // 如果發生錯誤，恢復原始列表
      setItems(items);
      // 可以選擇顯示錯誤消息
      alert("刪除時發生錯誤，請稍後再試");
    }
  };

  // 清除聊天消息的函數
  const clearMessages = useCallback(async (title: string, isSwitchingSearch: boolean = true) => {
    console.log(`清除聊天消息 (標題: ${title}, 切換搜索: ${isSwitchingSearch})`);

    // 獲取會話ID
    const sessionId = getSessionId();

    // 步驟1: 觸發前端事件，通知清空聊天界面
    const resetEvent = new CustomEvent('clearChatMessages', {
      detail: {
        title: title,
        isSwitchingSearch: isSwitchingSearch
      }
    });
    window.dispatchEvent(resetEvent);

    // 步驟2: 調用API清空後端存儲的消息
    try {
      console.log("調用API清空聊天消息");
      const clearResponse = await fetch(`${apiUrl}/api/clear_messages?session_id=${sessionId}`, {
        method: 'POST',
      });

      if (!clearResponse.ok) {
        console.error("清空聊天消息API返回錯誤:", await clearResponse.text());
      } else {
        console.log("聊天消息已清空:", await clearResponse.json());
      }
    } catch (error) {
      console.error("清空聊天消息時出錯:", error);
    }
  }, [apiUrl, getSessionId]);

  // 發送搜索結果消息的函數
  const sendSearchResultMessages = useCallback(async (title: string, result: SearchResult, formData: FormData) => {
    try {
      console.log("準備發送搜索結果消息，記錄數:", result.records.length);

      // 獲取會話ID
      const sessionId = getSessionId();

      // 創建一條用戶消息和一條表格消息
      const userMsg = {
        role: "user",
        content: `我想查看「${title}」的搜索結果`,
        metadata: { query: formData.query || "" }
      };

      // 表格消息 - 使用JSON格式
      const tableMsg = {
        role: "bot",
        content: `\`\`\`json\n${JSON.stringify(result.records, null, 2)}\n\`\`\``,
        metadata: { query: formData.query || "" }
      };

      // 構建歡迎消息
      const welcomeMsg = {
        role: "bot",
        content: [
          `嗨！我找到了「${title}」的搜索資料啦！🎯✨`,
          `這批資料的時間範圍是 ${formatTime(result.start_time)} ~ ${formatTime(result.end_time)} 📅`,
          `我已經幫你整理好了：💁 資料來源：${result.source || '全部'} 📊 涵蓋KOL：${result.kol || 'All'} ⭐`,
          `總共有 ${result.records.length} 筆資料等著你來探索！👀`,
          `有什麼想過濾的嗎？我很樂意幫你找出這段時間的趨勢喔！`
        ].join('\n'),
        metadata: { query: formData.query || "" }
      };

      const messages = [userMsg, welcomeMsg, tableMsg];

      // 發送批量消息
      console.log("發送批量消息", messages);
      const response = await fetch(`${apiUrl}/api/chat_direct_batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: messages,
          session_id: sessionId  // 添加會話ID
        }),
      });

      if (!response.ok) {
        console.error("發送消息API返回錯誤:", await response.text());
        return false;
      }

      const data = await response.json();
      console.log("批量消息發送成功:", data);

      // 發送搜索處理完成事件
      const eventId = Date.now().toString();
      console.log(`觸發搜索處理完成事件，ID: ${eventId}`);
      const completeEvent = new CustomEvent('searchProcessingCompleted', {
        detail: {
          title,
          recordCount: result.records.length,
          eventId
        }
      });
      window.dispatchEvent(completeEvent);

      return true;
    } catch (error) {
      console.error("發送搜索結果消息時出錯:", error);
      return false;
    }
  }, [apiUrl, getSessionId]);

  console.log("Rendering SavedSearchList - loading:", loading, "items length:", items.length);

  return (
    <div style={{ width: "100%" }}>
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 20,     // 與清單距離拉大
        color: "#777777",
        width: "100%"
      }}>
        <div style={{ display: "flex", alignItems: "center" }}>
          <span style={{
            textAlign: "left",
            color: "#777777",
            fontSize: 12,
            paddingLeft: 8
          }}>Saved Search</span>

          {/* 刷新按鈕 */}
          <button onClick={handleRetry} style={{
            background: "none",
            border: "none",
            color: "#777777",
            cursor: "pointer",
            fontSize: 12,
            lineHeight: 1,
            padding: 0,
            margin: "0 0 0 8px"
          }} title="刷新列表">↻</button>
        </div>
        <button onClick={() => { setReadOnly(false); setOpen(true); }} style={{
          background: "none",
          border: "none",
          color: "#28c8c8",
          cursor: "pointer",
          fontSize: 12,
          lineHeight: 1,
          padding: 0,
          paddingRight: 8,
          margin: 0
        }}>＋</button>
      </div>
      <div className="search-list-container">
        <SearchListResult
          items={items}
          itemsData={savedSearches}
          onSelect={handleSelect}
          onEdit={handleEdit}
          onReorder={handleReorder}
          onDelete={handleDelete}
          isLoading={loading}
          selectedItem={selectedItem}
        />
      </div>
      {open && (
        <Modal
          open={open}
          onClose={handleClose}
          onSave={handleSaveEdit}
          initialData={editingItem}
          apiUrl={apiUrl}
          isSaving={loading}
          readOnly={readOnly}
        />
      )}
      {isSearchProcessing && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: "rgba(0,0,0,0.3)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 1000,
        }}>
          <div style={{
            background: "#222",
            padding: "20px 40px",
            borderRadius: "8px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
            color: "#fff",
            fontSize: "16px"
          }}>
            <div>機器人思考中...</div>
          </div>
        </div>
      )}
    </div>
  );
}
