// Интерфейс для успешного ответа от сервера
export interface ApiResponse<T> {
  success: true;
  data: T;
}

// Интерфейс для ошибок с сервера
export interface ApiError {
  success: false;
  error: string;
  details?: any
}

export interface Base<T> {
  code: number,
  msg: string,
  data: T
}
