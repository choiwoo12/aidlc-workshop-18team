/**
 * SSE Service - Unit 2: Customer Order Domain
 * 
 * Server-Sent Events 연결 관리 서비스
 */

class SSEService {
  constructor() {
    this.eventSource = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 3;
    this.reconnectDelays = [0, 5000, 10000]; // 즉시, 5초, 10초
    this.tableId = null;
  }

  /**
   * SSE 연결 설정
   * @param {number} tableId - 테이블 ID
   * @param {Function} onMessage - 메시지 수신 콜백
   * @param {Function} onError - 에러 콜백
   */
  connect(tableId, onMessage, onError) {
    this.tableId = tableId;
    this.eventSource = new EventSource(
      `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/sse/orders/${tableId}`
    );

    this.eventSource.onmessage = (event) => {
      // 연결 성공 시 재연결 카운터 리셋
      this.reconnectAttempts = 0;
      
      // Keep-alive 메시지는 무시
      if (event.data === ':') {
        return;
      }
      
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('Failed to parse SSE message:', error);
      }
    };

    this.eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      this.handleConnectionError(onMessage, onError);
    };
  }

  /**
   * 연결 에러 처리 및 재연결
   * @param {Function} onMessage - 메시지 수신 콜백
   * @param {Function} onError - 에러 콜백
   */
  handleConnectionError(onMessage, onError) {
    this.disconnect();

    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const delay = this.reconnectDelays[this.reconnectAttempts];
      this.reconnectAttempts++;

      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

      setTimeout(() => {
        this.connect(this.tableId, onMessage, onError);
      }, delay);
    } else {
      // 최대 재연결 시도 초과
      onError(new Error('SSE 연결에 실패했습니다. 페이지를 새로고침해주세요.'));
    }
  }

  /**
   * SSE 연결 종료
   */
  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }

  /**
   * 연결 상태 확인
   * @returns {boolean} 연결 여부
   */
  isConnected() {
    return this.eventSource !== null && this.eventSource.readyState === EventSource.OPEN;
  }

  /**
   * 재연결 시도 횟수 조회
   * @returns {number} 재연결 시도 횟수
   */
  getReconnectAttempts() {
    return this.reconnectAttempts;
  }
}

export default new SSEService();
