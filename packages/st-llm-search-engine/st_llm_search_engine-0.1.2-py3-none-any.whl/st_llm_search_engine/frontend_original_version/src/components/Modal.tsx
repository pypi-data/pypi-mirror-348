import React, { useState, useRef, useEffect } from "react";
import { DatePicker } from 'antd';
import 'antd/dist/reset.css';
import TagSelector from "./TagSelector";
const { RangePicker } = DatePicker;

// 為 window 添加類型聲明
declare global {
  interface Window {
    REACT_APP_API_URL?: string;
  }
}

const fontFamily = "'Inter', 'Noto Sans TC', 'Microsoft JhengHei', Arial, sans-serif";
const timeOptions = ["昨日", "今日", "近N日", "自訂區間"];
const sourceOptions = ["全部", "Facebook", "Threads"];

interface ModalProps {
  open: boolean;
  onClose: () => void;
  apiUrl?: string;
  onSave?: (data: SearchFormData) => Promise<void>;
  initialData?: SearchFormData | null;
  isSaving?: boolean;
  readOnly?: boolean;
}

export interface SearchFormData {
  title: string;
  time?: number;
  source?: number;
  tags?: string[];
  query?: string;
  n?: string;
  range?: any;
}

export default function Modal({ open, onClose, apiUrl = window.REACT_APP_API_URL || "http://localhost:8000", onSave, initialData, isSaving = false, readOnly = false }: ModalProps) {
  const [title, setTitle] = useState("");
  const [tag, setTag] = useState("");
  const [query, setQuery] = useState("");
  const [time, setTime] = useState(0);
  const [source, setSource] = useState(0);
  const [n, setN] = useState("");
  const [nError, setNError] = useState(false);
  const [titleError, setTitleError] = useState(false);
  const nInputRef = useRef<HTMLInputElement>(null);
  const [range, setRange] = useState<any>(null);
  const [popupOpen, setPopupOpen] = useState(false);
  const tagRef = useRef<HTMLTextAreaElement>(null);
  const queryRef = useRef<HTMLTextAreaElement>(null);
  const [selectedTags, setSelectedTags] = useState<string[]>(["All"]);
  const [tagsList, setTagsList] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const validateN = (val: string) => {
    const num = Number(val);
    return /^[1-9]$|^1[0-9]$|^2[0-9]$|^30$/.test(val) && num >= 1 && num <= 30;
  };

  // 自動長高
  useEffect(() => {
    if (tagRef.current) {
      tagRef.current.style.height = '40px';
      tagRef.current.style.height = tagRef.current.scrollHeight + 'px';
    }
  }, [tag]);
  useEffect(() => {
    if (queryRef.current) {
      queryRef.current.style.height = '40px';
      queryRef.current.style.height = queryRef.current.scrollHeight + 'px';
    }
  }, [query]);

  useEffect(() => {
    if (open) {
      // 如果有初始數據，則填充表單
      if (initialData) {
        setTitle(initialData.title || "");
        setTime(initialData.time !== undefined ? initialData.time : 0);
        setSource(initialData.source !== undefined ? initialData.source : 0);
        setSelectedTags(initialData.tags || ["All"]);
        setQuery(initialData.query || "");
        setN(initialData.n || "");
        setRange(initialData.range || null);
      } else {
        // 否則重置表單
        setTitle("");
        setTime(0);
        setSource(0);
        setSelectedTags(["All"]);
        setQuery("");
        setN("");
        setRange(null);
      }
      fetchTags();
    }
  }, [open, initialData]);

  const fetchTags = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${apiUrl}/api/sheet/kol?col=KOL`);
      const data = await response.json();
      if (Array.isArray(data)) {
        setTagsList(data);
      }
    } catch (error) {
      console.error("Error fetching tags:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // 處理保存
  const handleSave = () => {
    console.log("儲存按鈕被點擊");

    // 檢查標題是否為空
    if (!title.trim()) {
      setTitleError(true);
      console.log("標題為空，不能儲存");
      return;
    }

    // 檢查是否選擇了「近N日」但N值無效
    if (time === 2 && !validateN(n)) {
      setNError(true);
      console.log("N值無效，不能儲存");
      return;
    }

    if (onSave) {
      const formData: SearchFormData = {
        title,
        time,
        source,
        tags: selectedTags,
        query,
        n,
        range
      };

      console.log("準備儲存表單數據:", formData);
      onSave(formData);
    } else {
      console.error("onSave 回調未定義");
    }
  };

  if (!open) return null;
  return (
    <div
      className="modal-backdrop"
      style={{
        position: "fixed",
        top: 0, left: 0, right: 0, bottom: 0,
        background: "rgba(0,0,0,0.7)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily,
      }}
      onClick={e => {
        if (e.target === e.currentTarget) {
          // 檢查是否有 popup 並且點擊在 popup 上
          const dropdown = document.querySelector('.ant-picker-dropdown');
          if (dropdown && dropdown.contains(document.activeElement)) {
            // 點擊在 popup 上，不做事
            return;
          }
          if (popupOpen) {
            setPopupOpen(false);
            document.activeElement && (document.activeElement as HTMLElement).blur();
          } else {
            onClose();
          }
        }
      }}
    >
      <div
        className="modal-content"
        style={{
          width: 616,
          minHeight: 634,
          height: "auto",
          maxHeight: "90vh",
          background: "#161616",
          borderRadius: 20,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          boxSizing: "border-box",
          padding: 0,
          position: "relative",
          paddingBottom: 24,
        }}
        onClick={e => e.stopPropagation()}
      >
        {/* 標題 */}
        <div
          style={{
            width: "100%",
            fontWeight: 400,
            fontSize: 24,
            lineHeight: "29px",
            color: "#fff",
            textAlign: "center",
            fontFamily,
            marginTop: 28,
            marginBottom: 28,
          }}
        >
          {readOnly ? "閱覽查詢條件" : "新增查詢條件"}
        </div>

        {/* 主要內容區塊 */}
        <div
          style={{
            width: 552,
            flex: 1,
            display: "flex",
            flexDirection: "column",
            alignItems: "flex-start",
            gap: 28,
            fontFamily,
            overflowY: "auto",
          }}
        >
          {/* 標題 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14, lineHeight: "17px" }}>
              標題 {!readOnly && <span style={{ color: "#FF4C4C" }}>*</span>}
              {titleError && !readOnly && (
                <span style={{ color: "#FF4C4C", marginLeft: 12 }}>此欄位為必填</span>
              )}
            </div>
            <input
              value={title}
              onChange={e => {
                if (!readOnly) {
                  setTitle(e.target.value);
                  if (e.target.value) setTitleError(false);
                }
              }}
              onBlur={() => !readOnly && setTitleError(!title.trim())}
              placeholder={readOnly ? "" : "請輸入查詢標題"}
              disabled={readOnly}
              style={{
                background: "#222",
                borderRadius: 12,
                border: titleError && !readOnly ? "1px solid #FF4C4C" : "none",
                padding: 12,
                width: "100%",
                color: "#fff",
                fontSize: 14,
                outline: "none",
                fontFamily,
                opacity: readOnly ? 0.7 : 1,
              }}
            />
          </div>
          {/* 時間 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>
              時間
              {nError && !readOnly && (
                <span style={{ color: "#FF4C4C", marginLeft: 12 }}>請輸入1-30內的數字</span>
              )}
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              {timeOptions.map((label, i) => (
                <button
                  key={label}
                  onClick={() => { if (!readOnly) { setTime(i); if (i !== 2) setNError(false); } }}
                  disabled={readOnly}
                  style={{
                    background: i === time ? "#222" : "#222",
                    border: i === time ? "1px solid #28C8C8" : "none",
                    color: "#fff",
                    borderRadius: 12,
                    padding: "12px 20px",
                    fontSize: 14,
                    cursor: readOnly ? "default" : "pointer",
                    opacity: i === time ? 1 : (readOnly ? 0.5 : 0.7),
                    fontFamily,
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  {label === "近N日"
                    ? (i === time
                      ? (
                        <>
                          近
                          <input
                            ref={nInputRef}
                            value={n}
                            onChange={e => {
                              if (!readOnly) {
                                setN(e.target.value);
                                setNError(false);
                              }
                            }}
                            onBlur={() => !readOnly && setNError(!validateN(n))}
                            disabled={readOnly}
                            style={{
                              width: 28,
                              margin: "0 2px",
                              background: "transparent",
                              border: "none",
                              color: "#fff",
                              fontSize: 14,
                              textAlign: "center",
                              outline: "none",
                              borderBottom: readOnly ? "none" : "1px solid #28C8C8",
                              opacity: readOnly ? 0.7 : 1,
                            }}
                            maxLength={2}
                            inputMode="numeric"
                            pattern="[0-9]*"
                            placeholder="N"
                          />
                          日
                        </>
                      )
                      : "近N日"
                    )
                    : label
                  }
                </button>
              ))}
            </div>
            {time === 3 && (
              <div style={{ display: "flex", justifyContent: "center", width: "100%", marginTop: 20 }}>
                <RangePicker
                  showTime
                  style={{ minWidth: 350, width: '70%' }}
                  getPopupContainer={trigger => document.body}
                  popupStyle={{ color: '#bbb', background: '#181818' }}
                  onChange={(val, strArr) => !readOnly && setRange(val)}
                  onOk={() => document.activeElement && (document.activeElement as HTMLElement).blur()}
                  open={!readOnly && popupOpen}
                  onOpenChange={open => !readOnly && setPopupOpen(open)}
                  disabled={readOnly}
                  value={range}
                />
              </div>
            )}
          </div>
          {/* 資料源 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>資料源</div>
            <div style={{ display: "flex", gap: 8 }}>
              {sourceOptions.map((label, i) => (
                <button
                  key={label}
                  onClick={() => !readOnly && setSource(i)}
                  disabled={readOnly}
                  style={{
                    background: i === source ? "#222" : "#222",
                    border: i === source ? "1px solid #28C8C8" : "none",
                    color: "#fff",
                    borderRadius: 12,
                    padding: "12px 20px",
                    fontSize: 14,
                    cursor: readOnly ? "default" : "pointer",
                    opacity: i === source ? 1 : (readOnly ? 0.5 : 0.7),
                    fontFamily,
                  }}
                >{label}</button>
              ))}
            </div>
          </div>
          {/* KOL */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>KOL</div>
            <TagSelector
              tagsList={tagsList}
              value={selectedTags}
              onChange={!readOnly ? setSelectedTags : () => {}}
              disabled={readOnly}
            />
          </div>
          {/* 檢索口令 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>檢索口令</div>
            <textarea
              ref={queryRef}
              value={query}
              onChange={e => !readOnly && setQuery(e.target.value)}
              placeholder={readOnly ? "" : "請輸入您想查詢的檢索口令"}
              disabled={readOnly}
              rows={1}
              style={{
                background: "#222",
                borderRadius: 12,
                border: "none",
                padding: 12,
                width: "100%",
                color: "#fff",
                fontSize: 14,
                outline: "none",
                fontFamily,
                wordBreak: "break-all",
                resize: "none",
                height: 40,
                minHeight: 40,
                lineHeight: 1.5,
                opacity: readOnly ? 0.7 : 1,
              }}
            />
          </div>
        </div>
        {/* 底部按鈕區 */}
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            gap: 8,
            width: "auto",
            height: 40,
            fontFamily,
            margin: "24px auto 0 auto",
            justifyContent: "center",
            paddingBottom: 40,
          }}
        >
          <button
            style={{
              flex: 1,
              background: "#333",
              borderRadius: 20,
              color: "#fff",
              fontWeight: 500,
              fontSize: 15,
              border: "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: 40,
              padding: "0 15px",
              cursor: "pointer",
              fontFamily,
              minWidth: "120px",
              maxWidth: "150px",
            }}
            onClick={onClose}
          >
            {readOnly ? "關閉" : "取消"}
          </button>
          {!readOnly && (
            <button
              id="save-button"
              style={{
                flex: 1,
                background: "#28D1D1",
                borderRadius: 20,
                color: "#222",
                fontWeight: 500,
                fontSize: 15,
                border: "none",
                height: 40,
                padding: "0 15px",
                cursor: isSaving ? "not-allowed" : "pointer",
                opacity: isSaving ? 0.7 : 1,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minWidth: "120px",
                maxWidth: "150px",
              }}
              onClick={(e) => {
                console.log("儲存按鈕被點擊", e);
                if (!isSaving) {
                  handleSave();
                }
              }}
              disabled={isSaving}
            >
              {isSaving ? "儲存中..." : "儲存"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
