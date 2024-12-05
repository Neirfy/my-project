import { ApiError, ApiResponse } from "@/types/api";
import { ProductsResponse } from "@/types/products";
import { Api } from ".";
import { Get } from "./types";

export const getProductsWithQuantity = async (search: string, page: number): Promise<ApiResponse<ProductsResponse> | ApiError> => {
  const query = {
    query: search,
    page: String(page),
    size: '100'
  }
  const params = new URLSearchParams(query).toString();
  return Api.get<ProductsResponse>(Get.productsSearchWithQuantity, params)
}
