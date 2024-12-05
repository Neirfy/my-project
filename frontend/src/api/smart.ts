import { ApiError, ApiResponse } from "@/types/api"
import { SmartRequest } from "@/types/smart"
import { Api } from "."
import { Post } from "./types"

export const createSmart = async (data: SmartRequest): Promise<ApiResponse<null> | ApiError> => {
  return Api.post<null>(Post.smart, JSON.stringify(data))
}
