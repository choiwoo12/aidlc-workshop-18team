// Domain Models
export interface Menu {
  id: number;
  storeId: number;
  name: string;
  price: number;
  imageUrl: string | null;
  createdAt: string;
}

export interface CartItem {
  menuId: number;
  menuName: string;
  price: number;
  quantity: number;
  imageUrl: string | null;
}

export interface Order {
  id: number;
  orderNumber: string;
  tableId: number;
  sessionId: string;
  status: OrderStatus;
  totalAmount: number;
  items: OrderItem[];
  createdAt: string;
}

export type OrderStatus = 'PENDING' | 'CONFIRMED' | 'PREPARING' | 'READY' | 'COMPLETED' | 'CANCELLED';

export interface OrderItem {
  id: number;
  menuId: number;
  menuName: string;
  quantity: number;
  unitPrice: number;
  subtotal: number;
}

// API Models
export interface CreateOrderRequest {
  storeId: number;
  tableId: number;
  sessionId: string;
  items: OrderItemRequest[];
}

export interface OrderItemRequest {
  menuId: number;
  quantity: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  message: string | null;
  error: string | null;
  timestamp: string;
}
