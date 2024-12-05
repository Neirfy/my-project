export type PaginationLinks = {
  first: string,
  last: string | null,
  self: string,
  next: string | null,
  prev: string | null
}
export interface Pagination<T> {
  items: T[],
  total: number,
  page: number,
  size: number,
  total_pages: number,
  links: PaginationLinks
}
