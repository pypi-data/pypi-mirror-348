/**
 * 日期和時間工具函數
 */

/**
 * 獲取當日開始時間的時間戳 (UTC+0 00:00:00)
 */
export function getTodayStartTimestamp(): number {
  const now = new Date();
  const utcDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 0, 0, 0));
  return Math.floor(utcDate.getTime() / 1000);
}

/**
 * 獲取當日結束時間的時間戳 (UTC+0 23:59:59)
 */
export function getTodayEndTimestamp(): number {
  const now = new Date();
  const utcDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 23, 59, 59));
  return Math.floor(utcDate.getTime() / 1000);
}

/**
 * 獲取昨日開始時間的時間戳 (UTC+0 00:00:00)
 */
export function getYesterdayStartTimestamp(): number {
  const now = new Date();
  const utcDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() - 1, 0, 0, 0));
  return Math.floor(utcDate.getTime() / 1000);
}

/**
 * 獲取昨日結束時間的時間戳 (UTC+0 23:59:59)
 */
export function getYesterdayEndTimestamp(): number {
  const now = new Date();
  const utcDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() - 1, 23, 59, 59));
  return Math.floor(utcDate.getTime() / 1000);
}

/**
 * 獲取最近 N 天的開始時間時間戳 (UTC+0 00:00:00)
 * @param n 天數
 */
export function getLastNDaysStartTimestamp(n: number): number {
  const now = new Date();
  const utcDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() - (n - 1), 0, 0, 0));
  return Math.floor(utcDate.getTime() / 1000);
}

/**
 * 根據表單數據中的時間選擇計算時間範圍
 * @param timeOption 時間選項 (0: 昨日, 1: 今日, 2: 近N日, 3: 自訂區間)
 * @param n 近N日的N值
 * @param range 自訂區間的範圍 [開始時間, 結束時間]
 * @returns 時間範圍 {start_time, end_time} (都是時間戳)
 */
export function calculateTimeRange(timeOption: number, n?: string, range?: any): { start_time: number; end_time: number } {
  switch (timeOption) {
    case 0: // 昨日
      return {
        start_time: getYesterdayStartTimestamp(),
        end_time: getYesterdayEndTimestamp()
      };
    case 1: // 今日
      return {
        start_time: getTodayStartTimestamp(),
        end_time: getTodayEndTimestamp()
      };
    case 2: // 近N日
      const nValue = n ? parseInt(n) : 7; // 默認為7天
      return {
        start_time: getLastNDaysStartTimestamp(nValue),
        end_time: getTodayEndTimestamp()
      };
    case 3: // 自訂區間
      if (range && Array.isArray(range) && range.length === 2) {
        const startMoment = range[0];
        const endMoment = range[1];

        let start_time = getTodayStartTimestamp();
        let end_time = getTodayEndTimestamp();

        // 如果有效的開始時間
        if (startMoment && startMoment._d) {
          start_time = Math.floor(startMoment._d.getTime() / 1000);
        }

        // 如果有效的結束時間
        if (endMoment && endMoment._d) {
          // 設定為當天的23:59:59
          const endDate = new Date(endMoment._d);
          endDate.setHours(23, 59, 59);
          end_time = Math.floor(endDate.getTime() / 1000);
        }

        return { start_time, end_time };
      }
      // 沒有有效的範圍，默認使用今日
      return {
        start_time: getTodayStartTimestamp(),
        end_time: getTodayEndTimestamp()
      };
    default:
      // 默認使用今日
      return {
        start_time: getTodayStartTimestamp(),
        end_time: getTodayEndTimestamp()
      };
  }
}
