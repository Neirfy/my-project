import { ApiError, ApiResponse } from "@/types/api"
import { Api } from "."
import { Delete, Get, Post, Put } from "./types"
import { UsersResponse } from "@/types/users"
import { UserRegister, UserUpdate } from "@/types/auth"

export const getUsers = async (): Promise<ApiResponse<UsersResponse> | ApiError> => {
  return Api.get<UsersResponse>(Get.users)
}

export const deleteUserByUsername = (username: string): Promise<ApiResponse<null> | ApiError> => {
  return Api.delete<null>(Delete.user, username)
}

export const registerUser = async (data: UserRegister): Promise<ApiResponse<null> | ApiError> => {
  return Api.post<null>(Post.register, JSON.stringify(data))
}
export const updateUser = async (data: UserUpdate): Promise<ApiResponse<null> | ApiError> => {
  return Api.put<null>(Put.updateUser, JSON.stringify(data))
}
