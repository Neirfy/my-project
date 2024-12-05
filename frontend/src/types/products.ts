import { Base } from "./api";
import { Pagination } from "./pagination";

export type Product = {
  id: number,
  name: string,
  image: string,
  quantity: number
}

export type ProductRequest = {
  id: number,
  name: string,
  quantity: number
}

export type ProductsResponse = Base<Pagination<Product>>
