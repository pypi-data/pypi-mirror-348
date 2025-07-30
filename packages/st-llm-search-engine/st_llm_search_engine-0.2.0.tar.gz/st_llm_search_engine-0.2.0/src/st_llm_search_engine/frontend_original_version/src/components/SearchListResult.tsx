import React, { useState, useRef, useEffect, useCallback } from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

export type SearchListResultProps = {
  items: string[];
  itemsData?: Array<{title: string, account?: string}>;  // 添加包含帳號信息的項目數據
  onSelect: (name: string) => void;
  onEdit?: (item: {title: string, readOnly?: boolean}) => void;
  onReorder?: (items: string[]) => void;
  onDelete?: (title: string) => void;
  isLoading?: boolean;
  selectedItem?: string;
};

// 拖曳項目類型
const ItemTypes = {
  CARD: 'card'
};

// 自定義確認對話框
const ConfirmDialog = ({
  isOpen,
  title,
  message,
  onConfirm,
  onCancel
}: {
  isOpen: boolean;
  title: string;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}) => {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
    }}>
      <div style={{
        backgroundColor: '#222',
        borderRadius: '8px',
        padding: '20px',
        width: '300px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
        border: '1px solid #444',
      }}>
        <h3 style={{
          margin: '0 0 15px 0',
          color: '#fff',
          fontSize: '18px',
        }}>{title}</h3>
        <p style={{
          margin: '0 0 20px 0',
          color: '#ccc',
          fontSize: '14px',
        }}>{message}</p>
        <div style={{
          display: 'flex',
          justifyContent: 'flex-end',
          gap: '10px'
        }}>
          <button
            onClick={onCancel}
            style={{
              padding: '8px 16px',
              background: 'transparent',
              border: '1px solid #666',
              borderRadius: '4px',
              color: '#ccc',
              cursor: 'pointer',
              fontSize: '14px',
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.background = '#333';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = 'transparent';
            }}
          >
            取消
          </button>
          <button
            onClick={onConfirm}
            style={{
              padding: '8px 16px',
              background: '#e53935',
              border: 'none',
              borderRadius: '4px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '14px',
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.background = '#f44336';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = '#e53935';
            }}
          >
            刪除
          </button>
        </div>
      </div>
    </div>
  );
};

// 可拖曳的列表項目
const DraggableItem = ({
  id,
  index,
  text,
  moveItem,
  onSelect,
  onContextMenu,
  isSelected,
  isSystemAccount
}: {
  id: string;
  index: number;
  text: string;
  moveItem: (dragIndex: number, hoverIndex: number) => void;
  onSelect: (name: string) => void;
  onContextMenu: (e: React.MouseEvent, item: string) => void;
  isSelected: boolean;
  isSystemAccount?: boolean; // 是否為系統帳號的項目
}) => {
  const ref = useRef<HTMLLIElement>(null);

  // 拖曳功能 - 系統帳號項目不可拖曳
  const [{ isDragging }, drag, preview] = useDrag({
    type: ItemTypes.CARD,
    item: () => ({ id, index }),
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
    canDrag: () => !isSystemAccount, // 系統帳號項目不可拖曳
  });

  // 放置功能 - 系統帳號項目不接受放置
  const [, drop] = useDrop({
    accept: ItemTypes.CARD,
    hover: (item: { id: string; index: number }, monitor) => {
      if (!ref.current || isSystemAccount) { // 系統帳號項目不接受放置
        return;
      }

      const dragIndex = item.index;
      const hoverIndex = index;

      // 不替換自己
      if (dragIndex === hoverIndex) {
        return;
      }

      // 確定鼠標位置
      const hoverBoundingRect = ref.current.getBoundingClientRect();
      const hoverMiddleY = (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      const clientOffset = monitor.getClientOffset();
      const hoverClientY = clientOffset!.y - hoverBoundingRect.top;

      // 只在跨過一半時執行移動
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) {
        return;
      }
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) {
        return;
      }

      // 執行移動
      moveItem(dragIndex, hoverIndex);

      // 注意：這裡我們修改了 item.index！這是為了避免閃爍
      item.index = hoverIndex;
    },
  });

  // 將拖曳和放置功能連接到元素
  drag(drop(ref));

  return (
    <li
      ref={ref}
      style={{
        width: "100%",
        background: isDragging ? "#444444" : isSelected ? "#444444" : "transparent",
        borderRadius: 4,
        padding: "8px 16px",
        marginBottom: 8,
        cursor: isSystemAccount ? "default" : "pointer", // 系統帳號項目使用默認游標
        color: "#FFFFFF",
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
        display: "flex",
        alignItems: "center",
        opacity: isDragging ? 0.5 : 1,
        boxShadow: isDragging ? "0 4px 8px rgba(0,0,0,0.3)" : "none",
        transition: "background-color 0.2s ease",
        border: isSelected ? "1px solid #666" : "1px solid transparent",
      }}
      onClick={() => onSelect(text)}
      onContextMenu={(e) => {
        // 無論是系統帳號還是普通帳號項目，都顯示右鍵選單
        e.preventDefault(); // 阻止默認右鍵菜單
        onContextMenu(e, text);
      }}
    >
      <span style={{
        marginRight: '8px',
        cursor: isSystemAccount ? 'not-allowed' : 'grab', // 系統帳號項目顯示禁止游標
        color: isSystemAccount ? '#555' : '#888', // 系統帳號項目的拖曳圖標顏色更暗
        fontSize: '14px',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: '16px',
        height: '16px',
      }}>
        ≡
      </span>
      <span style={{
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        flexGrow: 1
      }}>
        {text}
      </span>
    </li>
  );
};

export default function SearchListResult({
  items,
  itemsData = [],
  onSelect,
  onEdit,
  onReorder,
  onDelete,
  isLoading = false,
  selectedItem
}: SearchListResultProps) {
  const [contextMenu, setContextMenu] = useState<{
    visible: boolean;
    x: number;
    y: number;
    item: string;
  }>({
    visible: false,
    x: 0,
    y: 0,
    item: ""
  });

  // 本地狀態跟蹤項目
  const [localItems, setLocalItems] = useState<string[]>([]);

  // 確認對話框狀態
  const [confirmDialog, setConfirmDialog] = useState({
    isOpen: false,
    title: "",
    message: "",
    itemToDelete: ""
  });

  // 當外部 items 變化時更新本地狀態
  useEffect(() => {
    setLocalItems(items);
  }, [items]);

  const contextMenuRef = useRef<HTMLDivElement>(null);

  // 處理右鍵點擊
  const handleContextMenu = (e: React.MouseEvent, item: string) => {
    e.preventDefault();
    e.stopPropagation(); // 防止事件冒泡
    setContextMenu({
      visible: true,
      x: e.clientX,
      y: e.clientY,
      item
    });
  };

  // 處理點擊編輯
  const handleEdit = () => {
    if (onEdit && contextMenu.item) {
      onEdit({ title: contextMenu.item });
      setContextMenu({ ...contextMenu, visible: false });
    }
  };

  // 處理點擊閱覽
  const handleView = () => {
    if (onEdit && contextMenu.item) {
      // 傳遞標題和 readOnly=true 表示僅閱覽
      onEdit({
        title: contextMenu.item,
        readOnly: true
      });
      setContextMenu({ ...contextMenu, visible: false });
    }
  };

  // 處理點擊刪除
  const handleDelete = () => {
    if (onDelete && contextMenu.item) {
      // 檢查是否為系統帳號項目
      const isSystemItem = itemsData.find(item => item.title === contextMenu.item)?.account === "系統";

      if (isSystemItem) {
        // 如果是系統帳號項目，顯示提示並阻止刪除
        alert("系統項目不可刪除");
        setContextMenu({ ...contextMenu, visible: false });
        return;
      }

      // 顯示自定義確認對話框
      setConfirmDialog({
        isOpen: true,
        title: "確認刪除",
        message: `確定要刪除「${contextMenu.item}」嗎？`,
        itemToDelete: contextMenu.item
      });

      // 關閉右鍵菜單
      setContextMenu({ ...contextMenu, visible: false });
    }
  };

  // 確認刪除
  const handleConfirmDelete = () => {
    if (onDelete && confirmDialog.itemToDelete) {
      // 再次檢查是否為系統帳號項目
      const isSystemItem = itemsData.find(item => item.title === confirmDialog.itemToDelete)?.account === "系統";

      if (!isSystemItem) {
        onDelete(confirmDialog.itemToDelete);
      }
    }
    // 關閉確認對話框
    setConfirmDialog({...confirmDialog, isOpen: false});
  };

  // 取消刪除
  const handleCancelDelete = () => {
    setConfirmDialog({...confirmDialog, isOpen: false});
  };

  // 關閉右鍵菜單
  const closeContextMenu = () => {
    setContextMenu({ ...contextMenu, visible: false });
  };

  // 點擊頁面任何地方關閉右鍵菜單
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      // 檢查點擊是否在菜單外部
      if (
        contextMenu.visible &&
        contextMenuRef.current &&
        !contextMenuRef.current.contains(e.target as Node)
      ) {
        closeContextMenu();
      }
    };

    document.addEventListener("click", handleClick);
    return () => {
      document.removeEventListener("click", handleClick);
    };
  }, [contextMenu.visible]);

  // 處理項目移動
  const moveItem = useCallback((dragIndex: number, hoverIndex: number) => {
    setLocalItems((prevItems) => {
      const newItems = [...prevItems];
      const [removed] = newItems.splice(dragIndex, 1);
      newItems.splice(hoverIndex, 0, removed);

      // 通知父組件
      if (onReorder) {
        onReorder(newItems);
      }

      return newItems;
    });
  }, [onReorder]);

  // 渲染內容
  let content;
  if (isLoading) {
    content = (
      <div style={{
        width: "100%",
        textAlign: "center",
        color: "#777777",
        fontSize: "12px",
        padding: "10px 0"
      }}>
        載入中...
      </div>
    );
  } else if (localItems.length > 0) {
    content = (
      <DndProvider backend={HTML5Backend}>
        <ul
          style={{
            listStyle: "none",
            padding: 0,
            margin: 0,
            width: "100%"
          }}
        >
          {localItems.map((name, index) => {
            // 查找對應的項目數據
            const itemData = itemsData.find(item => item.title === name);
            // 判斷是否為系統帳號
            const isSystemAccount = itemData?.account === "系統";

            return (
              <DraggableItem
                key={name}
                id={name}
                index={index}
                text={name}
                moveItem={moveItem}
                onSelect={onSelect}
                onContextMenu={handleContextMenu}
                isSelected={selectedItem === name}
                isSystemAccount={isSystemAccount}
              />
            );
          })}
        </ul>
      </DndProvider>
    );
  } else {
    content = (
      <div style={{
        width: "100%",
        textAlign: "center",
        color: "#777777",
        fontSize: "12px",
        padding: "10px 0"
      }}>
        尚無保存的查詢
      </div>
    );
  }

  return (
    <>
      {content}

      {/* 右鍵菜單 */}
      {contextMenu.visible && (
        <div
          ref={contextMenuRef}
          style={{
            position: "fixed",
            top: contextMenu.y,
            left: contextMenu.x,
            background: "#222",
            border: "1px solid #444",
            borderRadius: 4,
            padding: 4,
            zIndex: 1000
          }}
        >
          {/* 閱覽選項 - 所有項目都可見 */}
          <button
            style={{
              background: "transparent",
              border: "none",
              color: "#fff",
              padding: "8px 16px",
              cursor: "pointer",
              width: "100%",
              textAlign: "left",
              borderRadius: 4
            }}
            onClick={handleView}
            onMouseOver={(e) => {
              e.currentTarget.style.background = "#444";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = "transparent";
            }}
          >
            閱覽
          </button>

          {/* 檢查是否為系統帳號項目 */}
          {!itemsData.find(item => item.title === contextMenu.item)?.account?.includes("系統") && (
            <>
              <button
                style={{
                  background: "transparent",
                  border: "none",
                  color: "#fff",
                  padding: "8px 16px",
                  cursor: "pointer",
                  width: "100%",
                  textAlign: "left",
                  borderRadius: 4
                }}
                onClick={handleEdit}
                onMouseOver={(e) => {
                  e.currentTarget.style.background = "#444";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.background = "transparent";
                }}
              >
                編輯
              </button>
              {onDelete && (
                <button
                  style={{
                    background: "transparent",
                    border: "none",
                    color: "#ff4d4f",
                    padding: "8px 16px",
                    cursor: "pointer",
                    width: "100%",
                    textAlign: "left",
                    borderRadius: 4
                  }}
                  onClick={handleDelete}
                  onMouseOver={(e) => {
                    e.currentTarget.style.background = "#444";
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.background = "transparent";
                  }}
                >
                  刪除
                </button>
              )}
            </>
          )}
          {itemsData.find(item => item.title === contextMenu.item)?.account?.includes("系統") && (
            <div style={{
              color: "#777",
              padding: "8px 16px",
              fontSize: "14px"
            }}>
              系統項目不可編輯或刪除
            </div>
          )}
        </div>
      )}

      {/* 確認刪除對話框 */}
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        title={confirmDialog.title}
        message={confirmDialog.message}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
      />
    </>
  );
}

