import { ApiError, ApiResponse } from "@/types/api";
import { Api } from ".";
import { BuildingResponse } from "@/types/buildings";
import { Get } from "./types";

export const getBuildings = async (search: string): Promise<ApiResponse<BuildingResponse> | ApiError> => {
  const query = {
    query: search,
    size: '100'
  }
  const params = new URLSearchParams(query).toString();
  return Api.get<BuildingResponse>(Get.builgingsSearch, params)
}
