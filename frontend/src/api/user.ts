import { ApiError, ApiResponse } from "@/types/api"
import { UserMeResponse } from "@/types/auth"
import { Api } from "."
import { Get } from "./types"

export const getUser = async (): Promise<ApiResponse<UserMeResponse> | ApiError> => {
  return Api.get<UserMeResponse>(Get.me)
}
