import { ApiError, ApiResponse } from '@/types/api'
import router from '@/router'
import { getToken } from '@/utils/getToken'
import { Delete, Get, Methods, Post, Put, Token } from './types'

const BASE_URL = import.meta.env.VITE_API_URL

export class Api {
  private static getHeaders (
    isFormData: boolean = false
  ): Record<string, string> {
    return {
      'Content-Type': isFormData
        ? 'application/x-www-form-urlencoded'
        : 'application/json',
      Authorization: `Bearer ${getToken()}`,
    }
  }

  private static error (error: unknown): ApiError {
    if (error instanceof Error) {
      return {
        success: false,
        error: error.message || 'Неизвестная ошибка',
      }
    }
    return {
      success: false,
      error: 'Неизвестная ошибка',
    }
  }

  // Доделать обработку ошибки авторизации
  private static async handleUnauthorized<T> (
    retry: () => Promise<ApiResponse<T> | ApiError>
  ): Promise<ApiResponse<T> | ApiError> {
    try {
      const refreshResponse = await this.get<Token>(Get.refresh)
      if (refreshResponse.success) {
        const newToken = refreshResponse.data.access_token // Получаем новый токен из ответа
        if (newToken) {
          localStorage.setItem('refresh', new Date().toString())
          localStorage.setItem('authToken', newToken) // Сохраняем новый токен
        }

        // Повторно выполняем исходный запрос
        return retry()
      } else {
        // Если реавторизация не удалась, возвращаем ошибку
        return {
          success: false,
          error: 'Failed to refresh token',
        }
      }
    } catch (error) {
      console.error('Error during token refresh:', error)
      return this.error(error)
    }
  }

  private static async response<T> (
    response: Response
  ): Promise<ApiResponse<T> | ApiError> {
    const data = await response.json()
    if (!response.ok) {
      const errorMessage =
        data?.message || `Ошибка ${response.status}: ${response.statusText}`
      return {
        success: false,
        error: errorMessage,
        // тут привести тип к типу ошибки
        details: data,
      }
    }

    return {
      success: true,
      data: data as T,
    }
  }

  private static async request<T> (
    url: string,
    method: Methods,
    body?: string,
    headers: Record<string, string> = {},
    query?: string,
  ): Promise<ApiResponse<T> | ApiError> {
    this.logRequest(method, url, body)
    try {
      const response = await fetch(`${BASE_URL}${url}?${query || ''}`, {
        method,
        headers,
        body,
      })

      if (response.status === 401) {
        return this.handleUnauthorized(() =>
          this.request<T>(url, method, body, this.getHeaders(), query)
        )
      }
      if (response.status === 403) {
        localStorage.setItem('unlogin', new Date().toString())
        localStorage.removeItem('authToken')
        router.push('/login')
      }

      return await this.response<T>(response)
    } catch (error) {
      console.error(`${method} request error:`, error)
      return this.error(error)
    }
  }

  static async get<T> (url: Get, query?: string): Promise<ApiResponse<T> | ApiError> {
    return this.request<T>(url, 'GET', undefined, this.getHeaders(), query)
  }

  static async delete<T> (url: Delete, id: string): Promise<ApiResponse<T> | ApiError> {
    return this.request<T>(`${url}/${id}`, 'DELETE', undefined, this.getHeaders())
  }

  static async post<T> (
    url: Post,
    body?: string
  ): Promise<ApiResponse<T> | ApiError> {
    return this.request<T>(url, 'POST', body, this.getHeaders())
  }

  static async put<T> (
    url: Put,
    body: string,
    id?: string
  ): Promise<ApiResponse<T> | ApiError> {
    return this.request<T>(
      `${url}/${id || ''}`,
      'PUT',
      body,
      this.getHeaders()
    )
  }

  private static logRequest (method: string, url: string, body?: string) {
    console.log(
      `%cRequest: ${method} ${url} ${body ? `Body: ${body}` : ''}`,
      'color:cyan;font-weight:300;font-size:10px'
    )
  }
}
