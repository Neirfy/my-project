import { ProductRequest } from "./products"

export type SmartRequest = {
  name: string,
  date: string,
  urgency: boolean,
  object: number,
  address: string,
  products: ProductRequest[],
  comment: string
}
