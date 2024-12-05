import type { ApiError, ApiResponse } from '@/types/api'
import { Api } from '.'
import { Post } from './types'
import { LoginResponse } from '@/types/auth'
// import { RegisterBodyRequest, RegisterResponse } from '@/types/auth'
// import type { GenerateRequestBody, GenerateResponse } from "@/types/generation"

export const loginUser = async (username: string, password: string): Promise<ApiResponse<LoginResponse> | ApiError> => {
  const body = {
    username,
    password
  }
  return Api.post<LoginResponse>(Post.login, JSON.stringify(body))
}

export const logoutUser = async (): Promise<ApiResponse<null> | ApiError> => {
  return Api.post<null>(Post.logout)
}

// export const registerUser = async (body: RegisterBodyRequest): Promise<ApiResponse<RegisterResponse> | ApiError> =>
//   Api.post<RegisterResponse>(Post.register, JSON.stringify(body))
